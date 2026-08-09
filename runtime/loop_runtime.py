#!/usr/bin/env python3
"""Provider-agnostic Mindway /loop state/event backbone.

Deterministic run-ledger, event logging, checkpoint/resume primitives,
redaction metadata, schema-aligned validation, and transition validation.
No AI provider or credential is embedded here.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TERMINAL = {"COMPLETE", "NEED_USER", "BLOCKED", "PLATFORM_LIMIT", "CYCLE_LIMIT", "FAILED"}
TOPOLOGIES = {"SEQUENTIAL", "PARALLEL", "HYBRID"}
EVENT_TYPES = {
    "run.created", "orient.started", "plan.created", "route.selected",
    "work.started", "work.completed", "tool.called", "tool.succeeded", "tool.failed",
    "verify.started", "verify.pass", "verify.fail", "fix.started", "fix.completed",
    "improvement.proposed", "approval.required", "checkpoint.saved", "run.resumed",
    "run.completed", "run.stopped",
}
ALLOWED = {
    "NEW": {"ORIENTING"},
    "ORIENTING": {"PLANNED", "NEED_USER", "BLOCKED"},
    "PLANNED": {"RUNNING", "NEED_USER", "BLOCKED"},
    "RUNNING": {"VERIFYING", "CHECKPOINTED", "NEED_USER", "BLOCKED", "PLATFORM_LIMIT", "CYCLE_LIMIT", "FAILED"},
    "VERIFYING": {"COMPLETE", "FIXING", "CHECKPOINTED", "NEED_USER", "BLOCKED", "FAILED"},
    "FIXING": {"VERIFYING", "RUNNING", "CHECKPOINTED", "NEED_USER", "BLOCKED", "FAILED"},
    "CHECKPOINTED": {"RUNNING", "NEED_USER", "BLOCKED", "PLATFORM_LIMIT"},
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_id(prefix: str) -> str:
    if not prefix:
        raise ValueError("id prefix must be non-empty")
    return f"{prefix}_{uuid.uuid4().hex}"


def checksum_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _validate_cycle_budget(value: Optional[int], field_name: str) -> None:
    if value is not None and (not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 99):
        raise ValueError(f"{field_name} must be an integer from 1 to 99 or None")


@dataclass
class RunLedger:
    mission: str
    requested_cycles: Optional[int] = None
    estimated_cycles: Optional[int] = None
    topology: Optional[str] = None
    run_id: str = field(default_factory=lambda: stable_id("run"))
    schema_version: str = "1.0"
    state: str = "NEW"
    completed_cycles: int = 0
    created_at: str = field(default_factory=now)
    updated_at: str = field(default_factory=now)
    completed: List[Dict[str, Any]] = field(default_factory=list)
    blocked_branches: List[Dict[str, Any]] = field(default_factory=list)
    next_action: Optional[str] = None
    risks: List[str] = field(default_factory=list)
    approval_gates: List[str] = field(default_factory=list)
    source_versions: Dict[str, str] = field(default_factory=dict)
    artifacts: List[str] = field(default_factory=list)
    checkpoint: Optional[Dict[str, str]] = None
    stop_reason: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.mission, str) or not self.mission.strip():
            raise ValueError("mission must be a non-empty string")
        if not isinstance(self.run_id, str) or not self.run_id:
            raise ValueError("run_id must be a non-empty string")
        if self.schema_version != "1.0":
            raise ValueError("unsupported schema_version")
        _validate_cycle_budget(self.requested_cycles, "requested_cycles")
        _validate_cycle_budget(self.estimated_cycles, "estimated_cycles")
        if self.topology is not None and self.topology not in TOPOLOGIES:
            raise ValueError(f"invalid topology: {self.topology}")
        if self.state not in set(ALLOWED) | TERMINAL:
            raise ValueError(f"invalid state: {self.state}")
        if not isinstance(self.completed_cycles, int) or isinstance(self.completed_cycles, bool) or self.completed_cycles < 0:
            raise ValueError("completed_cycles must be a non-negative integer")

    def transition(self, new_state: str) -> None:
        if self.state in TERMINAL:
            raise ValueError(f"terminal state cannot transition: {self.state}")
        if new_state not in ALLOWED.get(self.state, set()):
            raise ValueError(f"invalid transition {self.state} -> {new_state}")
        self.state = new_state
        self.updated_at = now()

    def add_completed(self, item: str, evidence: Optional[List[str]] = None) -> None:
        if not isinstance(item, str) or not item.strip():
            raise ValueError("completed item must be non-empty")
        self.completed.append({"item": item, "evidence": evidence or []})
        self.updated_at = now()

    def add_blocked_branch(self, item: str, reason: str, next_action: str,
                           evidence: Optional[List[str]] = None) -> None:
        if not all(isinstance(v, str) and v.strip() for v in (item, reason, next_action)):
            raise ValueError("blocked branch item, reason, and next_action must be non-empty")
        self.blocked_branches.append({
            "item": item, "reason": reason, "evidence": evidence or [], "next_action": next_action
        })
        self.updated_at = now()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RunLedger":
        if not isinstance(data, dict):
            raise ValueError("ledger checkpoint data must be an object")
        return cls(**data)


class EventLog:
    def __init__(self, run_id: str, events: Optional[List[Dict[str, Any]]] = None):
        if not isinstance(run_id, str) or not run_id:
            raise ValueError("run_id must be a non-empty string")
        self.run_id = run_id
        self.events: List[Dict[str, Any]] = list(events or [])
        for i, event in enumerate(self.events):
            self._validate_existing_event(event, i)

    def _validate_existing_event(self, event: Dict[str, Any], sequence: int) -> None:
        if not isinstance(event, dict):
            raise ValueError("event must be an object")
        if event.get("run_id") != self.run_id:
            raise ValueError("checkpoint event run_id mismatch")
        if event.get("type") not in EVENT_TYPES:
            raise ValueError(f"unknown event type: {event.get('type')}")
        if event.get("sequence") != sequence:
            raise ValueError("event sequence is not contiguous")
        cycle = event.get("cycle", 0)
        if not isinstance(cycle, int) or isinstance(cycle, bool) or cycle < 0:
            raise ValueError("event cycle must be a non-negative integer")

    def emit(self, event_type: str, *, cycle: int = 0, actor: Optional[str] = None,
             subject: Optional[str] = None, status: Optional[str] = None,
             evidence: Optional[List[str]] = None, payload: Optional[Dict[str, Any]] = None,
             redacted_fields: Optional[List[str]] = None) -> Dict[str, Any]:
        if event_type not in EVENT_TYPES:
            raise ValueError(f"unknown event type: {event_type}")
        if not isinstance(cycle, int) or isinstance(cycle, bool) or cycle < 0:
            raise ValueError("cycle must be a non-negative integer")
        if payload is not None and not isinstance(payload, dict):
            raise ValueError("payload must be an object")
        event = {
            "schema_version": "1.0",
            "event_id": stable_id("evt"),
            "run_id": self.run_id,
            "parent_event_id": self.events[-1]["event_id"] if self.events else None,
            "type": event_type,
            "timestamp": now(),
            "sequence": len(self.events),
            "cycle": cycle,
            "actor": actor,
            "subject": subject,
            "status": status,
            "evidence": evidence or [],
            "payload": payload or {},
            "redaction": {"applied": bool(redacted_fields), "fields": redacted_fields or []},
        }
        self.events.append(event)
        return event

    def write_jsonl(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in self.events),
            encoding="utf-8",
        )


def save_checkpoint(ledger: RunLedger, events: EventLog, directory: Path) -> Dict[str, str]:
    if events.run_id != ledger.run_id:
        raise ValueError("ledger/event run_id mismatch")
    directory.mkdir(parents=True, exist_ok=True)
    payload = {"ledger": ledger.to_dict(), "events": events.events}
    raw = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    digest = checksum_bytes(raw)
    path = directory / f"{ledger.run_id}.checkpoint.json"
    path.write_bytes(raw)
    checkpoint = {"uri": str(path), "checksum": digest, "saved_at": now()}
    ledger.checkpoint = checkpoint
    ledger.updated_at = now()
    return checkpoint


def load_checkpoint(path: Path, expected_checksum: Optional[str] = None) -> Dict[str, Any]:
    raw = path.read_bytes()
    digest = checksum_bytes(raw)
    if expected_checksum is not None and digest != expected_checksum:
        raise ValueError("checkpoint checksum mismatch")
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict) or "ledger" not in data or "events" not in data:
        raise ValueError("invalid checkpoint shape")
    return {"checksum": digest, "data": data}


def resume_checkpoint(path: Path, expected_checksum: Optional[str] = None) -> tuple[RunLedger, EventLog]:
    loaded = load_checkpoint(path, expected_checksum)
    ledger = RunLedger.from_dict(loaded["data"]["ledger"])
    events = EventLog(ledger.run_id, loaded["data"]["events"])
    return ledger, events


if __name__ == "__main__":
    ledger = RunLedger("Mindway /loop smoke test", requested_cycles=3, topology="SEQUENTIAL")
    events = EventLog(ledger.run_id)
    events.emit("run.created", status=ledger.state)
    ledger.transition("ORIENTING"); events.emit("orient.started", status=ledger.state)
    ledger.transition("PLANNED"); events.emit("plan.created", status=ledger.state)
    ledger.transition("RUNNING"); events.emit("work.started", cycle=1, status=ledger.state)
    ledger.add_completed("runtime backbone smoke path")
    ledger.transition("VERIFYING"); events.emit("verify.started", cycle=1, status=ledger.state)
    ledger.transition("COMPLETE"); events.emit("verify.pass", cycle=1, status=ledger.state)
    events.emit("run.completed", cycle=1, status=ledger.state)
    print(json.dumps(ledger.to_dict(), ensure_ascii=False, indent=2))
