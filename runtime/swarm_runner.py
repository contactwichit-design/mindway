#!/usr/bin/env python3
"""Mindway Swarm Runtime reference runner.

Provider-agnostic orchestration for CLI-capable AI agents.
- parallel worker fan-out
- persistent shared run board
- critic -> synthesizer -> fixer -> verifier
- resumable stage outputs
- no shell interpolation

The runner does not contain credentials and does not assume an AI vendor.
Each configured agent is an argv array. Prompts are sent over stdin.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RUNTIME_VERSION = "mindway-swarm-v1"


@dataclass
class AgentSpec:
    name: str
    role: str
    command: list[str]
    timeout_seconds: int = 900


def utc_stamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def stable_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temp, path)


def parse_agent(item: dict[str, Any]) -> AgentSpec:
    cmd = item.get("command")
    if not isinstance(cmd, list) or not cmd or not all(isinstance(x, str) for x in cmd):
        raise ValueError(f"Agent {item.get('name')} command must be a non-empty string array")
    return AgentSpec(
        name=str(item["name"]),
        role=str(item.get("role", item["name"])),
        command=cmd,
        timeout_seconds=int(item.get("timeout_seconds", 900)),
    )


async def run_agent(agent: AgentSpec, prompt: str, env_extra: dict[str, str] | None = None) -> dict[str, Any]:
    started = utc_stamp()
    env = os.environ.copy()
    if env_extra:
        env.update({k: str(v) for k, v in env_extra.items()})

    proc = await asyncio.create_subprocess_exec(
        *agent.command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
    )

    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(prompt.encode("utf-8")),
            timeout=agent.timeout_seconds,
        )
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
        return {
            "agent": agent.name,
            "role": agent.role,
            "status": "TIMEOUT",
            "started_at": started,
            "finished_at": utc_stamp(),
            "returncode": None,
            "stdout": "",
            "stderr": f"Timed out after {agent.timeout_seconds}s",
        }

    return {
        "agent": agent.name,
        "role": agent.role,
        "status": "DONE" if proc.returncode == 0 else "ERROR",
        "started_at": started,
        "finished_at": utc_stamp(),
        "returncode": proc.returncode,
        "stdout": stdout.decode("utf-8", errors="replace"),
        "stderr": stderr.decode("utf-8", errors="replace"),
    }


def worker_prompt(mission: str, constraints: list[str], workstream: dict[str, Any]) -> str:
    return f"""You are a Mindway specialist worker.

ORIGINAL MISSION:
{mission}

HARD CONSTRAINTS:
{json.dumps(constraints, ensure_ascii=False, indent=2)}

YOUR WORKSTREAM:
ID: {workstream['id']}
ROLE: {workstream.get('role', '')}
GOAL: {workstream['goal']}
EXPECTED OUTPUT: {workstream.get('expected_output', '')}

Rules:
- Work only this workstream unless a dependency must be flagged.
- Distinguish evidence, inference, proposal, and uncertainty.
- Preserve provenance/source references when available.
- Do not claim tool/source access you did not perform.
- Return a concise but complete result, risks, conflicts, and next action.
"""


def stage_prompt(stage: str, mission: str, constraints: list[str], inputs: list[dict[str, Any]]) -> str:
    compact = [
        {
            "agent": x.get("agent"),
            "role": x.get("role"),
            "status": x.get("status"),
            "output": x.get("stdout", ""),
        }
        for x in inputs
    ]
    stage_rules = {
        "critic": "Find substantive gaps, unsupported claims, conflicts, edge cases, and requirement misses. Return actionable issues ranked by severity.",
        "synthesizer": "Integrate unique evidence, deduplicate overlap, expose conflicts, preserve minority findings with stronger evidence, and produce one coherent candidate.",
        "fixer": "Repair the candidate using the critique. Do not introduce unsupported claims. Preserve traceability of important decisions.",
        "verifier": "Independently verify the final candidate against the original mission and constraints. Return exactly one leading verdict: PASS, PASS_WITH_WARNINGS, FAIL_REPAIRABLE, BLOCKED, or NEED_USER, followed by evidence.",
    }
    return f"""You are the Mindway {stage} stage.

ORIGINAL MISSION:
{mission}

HARD CONSTRAINTS:
{json.dumps(constraints, ensure_ascii=False, indent=2)}

STAGE RULE:
{stage_rules[stage]}

INPUTS:
{json.dumps(compact, ensure_ascii=False, indent=2)}

Mindway rules:
- Evidence outranks majority vote.
- Separate fact, inference, proposal, and uncertainty.
- Do not hide unresolved conflicts.
- Do not claim access or verification you did not perform.
"""


def build_board(config: dict[str, Any], run_dir: Path) -> dict[str, Any]:
    return {
        "runtime": RUNTIME_VERSION,
        "run_id": config.get("run_id") or f"RUN-{time.strftime('%Y%m%d-%H%M%S')}",
        "created_at": utc_stamp(),
        "updated_at": utc_stamp(),
        "mission": config["mission"],
        "mission_hash": stable_hash(config["mission"]),
        "status": "IN_PROGRESS",
        "requested_cycles": int(config.get("requested_cycles", 20)),
        "used_cycles": 0,
        "topology": config.get("topology", "HYBRID"),
        "workstreams": {},
        "stages": {},
        "conflicts": [],
        "open_gaps": [],
        "run_dir": str(run_dir),
        "stop_reason": None,
    }


def result_to_file(run_dir: Path, name: str, result: dict[str, Any]) -> None:
    save_json(run_dir / "results" / f"{name}.json", result)


async def main_async(config_path: Path, resume_dir: Path | None) -> int:
    config = load_json(config_path)
    mission = str(config["mission"])
    constraints = [str(x) for x in config.get("constraints", [])]

    if resume_dir:
        run_dir = resume_dir
        board_path = run_dir / "board.json"
        board = load_json(board_path)
        if board.get("mission_hash") != stable_hash(mission):
            raise RuntimeError("Resume config mission does not match existing run mission")
    else:
        base = Path(config.get("runs_dir", "runs"))
        run_dir = base / (config.get("run_id") or f"RUN-{time.strftime('%Y%m%d-%H%M%S')}")
        run_dir.mkdir(parents=True, exist_ok=True)
        board_path = run_dir / "board.json"
        board = build_board(config, run_dir)
        save_json(board_path, board)

    agents_by_name = {x["name"]: parse_agent(x) for x in config["agents"]}
    max_cycles = int(board["requested_cycles"])

    async def consume_cycle() -> None:
        board["used_cycles"] += 1
        board["updated_at"] = utc_stamp()
        save_json(board_path, board)
        if board["used_cycles"] > max_cycles:
            raise RuntimeError("Cycle budget exceeded")

    # FAN-OUT workers
    pending = []
    pending_meta = []
    for ws in config.get("workstreams", []):
        wid = str(ws["id"])
        prior = board["workstreams"].get(wid)
        if prior and prior.get("status") == "DONE":
            continue
        agent_name = str(ws["agent"])
        agent = agents_by_name[agent_name]
        if board["used_cycles"] + len(pending) >= max_cycles:
            break
        pending.append(run_agent(agent, worker_prompt(mission, constraints, ws)))
        pending_meta.append((wid, ws, agent_name))

    if pending:
        results = await asyncio.gather(*pending)
        for (wid, ws, _), result in zip(pending_meta, results):
            await consume_cycle()
            result_to_file(run_dir, f"worker-{wid}", result)
            board["workstreams"][wid] = {
                "role": ws.get("role"),
                "goal": ws.get("goal"),
                "agent": result.get("agent"),
                "status": result.get("status"),
                "result_file": f"results/worker-{wid}.json",
            }
            save_json(board_path, board)

    worker_results = []
    for wid, ws_state in board["workstreams"].items():
        path = run_dir / ws_state["result_file"]
        if path.exists():
            worker_results.append(load_json(path))

    if not worker_results:
        board["status"] = "BLOCKED"
        board["stop_reason"] = "No completed worker results"
        save_json(board_path, board)
        return 2

    # Structured stages; each is resumable.
    stage_inputs: list[dict[str, Any]] = worker_results
    for stage in ("critic", "synthesizer", "fixer", "verifier"):
        existing = board["stages"].get(stage)
        if existing and existing.get("status") == "DONE":
            stage_result = load_json(run_dir / existing["result_file"])
            if stage in ("synthesizer", "fixer"):
                stage_inputs = [stage_result]
            continue

        if board["used_cycles"] >= max_cycles:
            board["status"] = "CYCLE_LIMIT"
            board["stop_reason"] = f"Cycle budget exhausted before {stage}"
            save_json(board_path, board)
            return 3

        agent_name = str(config["stages"][stage])
        agent = agents_by_name[agent_name]

        # Critic sees workers. Synthesizer sees workers + critique.
        # Fixer sees synthesis + critique. Verifier sees repaired result + critique.
        if stage == "critic":
            inputs = worker_results
        elif stage == "synthesizer":
            critic_result = load_json(run_dir / board["stages"]["critic"]["result_file"])
            inputs = worker_results + [critic_result]
        elif stage == "fixer":
            critic_result = load_json(run_dir / board["stages"]["critic"]["result_file"])
            synth_result = load_json(run_dir / board["stages"]["synthesizer"]["result_file"])
            inputs = [synth_result, critic_result]
        else:
            fixer_result = load_json(run_dir / board["stages"]["fixer"]["result_file"])
            critic_result = load_json(run_dir / board["stages"]["critic"]["result_file"])
            inputs = [fixer_result, critic_result]

        result = await run_agent(agent, stage_prompt(stage, mission, constraints, inputs))
        await consume_cycle()
        result_to_file(run_dir, stage, result)
        board["stages"][stage] = {
            "agent": result.get("agent"),
            "status": result.get("status"),
            "result_file": f"results/{stage}.json",
        }
        save_json(board_path, board)
        if result.get("status") != "DONE":
            board["status"] = "BLOCKED"
            board["stop_reason"] = f"{stage} stage failed"
            save_json(board_path, board)
            return 4

        if stage in ("synthesizer", "fixer"):
            stage_inputs = [result]

    verifier = load_json(run_dir / board["stages"]["verifier"]["result_file"])
    verdict_line = verifier.get("stdout", "").strip().splitlines()
    verdict = verdict_line[0].strip().upper() if verdict_line else ""
    if verdict.startswith("PASS"):
        board["status"] = "COMPLETE"
        board["stop_reason"] = verdict
        final = load_json(run_dir / board["stages"]["fixer"]["result_file"])
        (run_dir / "FINAL.md").write_text(final.get("stdout", ""), encoding="utf-8")
        save_json(board_path, board)
        return 0

    board["status"] = "REVIEW_NEEDED"
    board["stop_reason"] = verdict or "Verifier did not return PASS"
    save_json(board_path, board)
    return 5


def main() -> int:
    parser = argparse.ArgumentParser(description="Mindway Swarm Runtime")
    parser.add_argument("config", type=Path, help="Path to swarm config JSON")
    parser.add_argument("--resume", type=Path, default=None, help="Existing run directory to resume")
    args = parser.parse_args()
    try:
        return asyncio.run(main_async(args.config, args.resume))
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
