#!/usr/bin/env python3
"""Provider-agnostic Mindway /loop state/event backbone.

This module does not call an AI provider. It provides deterministic run-ledger,
event logging, checkpoint/resume primitives, redaction hooks, and transition
validation for orchestrators to build on.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TERMINAL = {"COMPLETE","NEED_USER","BLOCKED","PLATFORM_LIMIT","CYCLE_LIMIT","FAILED"}
ALLOWED = {
    "NEW": {"ORIENTING"},
    "ORIENTING": {"PLANNED","NEED_USER","BLOCKED"},
    "PLANNED": {"RUNNING","NEED_USER","BLOCKED"},
    "RUNNING": {"VERIFYING","CHECKPOINTED","NEED_USER","BLOCKED","PLATFORM_LIMIT","CYCLE_LIMIT","FAILED"},
    "VERIFYING": {"COMPLETE","FIXING","CHECKPOINTED","NEED_USER","BLOCKED","FAILED"},
    "FIXING": {"VERIFYING","RUNNING","CHECKPOINTED","NEED_USER","BLOCKED","FAILED"},
    "CHECKPOINTED": {"RUNNING","NEED_USER","BLOCKED","PLATFORM_LIMIT"},
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stable_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


def checksum_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

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

    def transition(self, new_state: str) -> None:
        if self.state in TERMINAL:
            raise ValueError(f"terminal state cannot transition: {self.state}")
        if new_state not in ALLOWED.get(self.state, set()):
            raise ValueError(f"invalid transition {self.state} -> {new_state}")
        self.state = new_state
        self.updated_at = now()

    def add_completed(self, item: str, evidence: Optional[List[str]] = None) -> None:
        self.completed.append({"item": item, "evidence": evidence or []})
        self.updated_at = now()

    def add_blocked_branch(self, item: str, reason: str, next_action: str, evidence: Optional[List[str]] = None) -> None:
        self.blocked_branches.append({"item": item, "reason": reason, "evidence": evidence or [], "next_action": next_action})
        self.updated_at = now()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class EventLog:
    def __init__(self, run_id: str):
        self.run_id = run_id
        self.events: List[Dict[str, Any]] = []

    def emit(self, event_type: str, *, cycle: int = 0, actor: Optional[str] = None,
             subject: Optional[str] = None, status: Optional[str] = None,
             evidence: Optional[List[str]] = None, payload: Optional[Dict[str, Any]] = None,
             redacted_fields: Optional[List[str]] = None) -> Dict[str, Any]:
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
        path.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in self.events), encoding="utf-8")


def save_checkpoint(ledger: RunLedger, events: EventLog, directory: Path) -> Dict[str, str]:
    directory.mkdir(parents=True, exist_ok=True)
    payload = {"ledger": ledger.to_dict(), "events": events.events}
    raw = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    digest = checksum_bytes(raw)
    path = directory / f"{ledger.run_id}.checkpoint.json"
    path.write_bytes(raw)
    ledger.checkpoint = {"uri": str(path), "checksum": digest, "saved_at": now()}
    ledger.updated_at = now()
    return ledger.checkpoint


def load_checkpoint(path: Path) -> Dict[str, Any]:
    raw = path.read_bytes()
    return {"checksum": checksum_bytes(raw), "data": json.loads(raw.decode("utf-8"))}

if __name__ == "__main__":
    ledger = RunLedger("Mindway /loop smoke test", requested_cycles=3, topology="SEQUENTIAL")
    events = EventLog(ledger.run_id)
    events.emit("run.created", status=ledger.state)
    ledger.transition("ORIENTING"); events.emit("orient.started", status=ledger.state)
    ledger.transition("PLANNED"); events.emit("plan.created", status=ledger.state)
    ledger.transition("RUNNING"); events.emit("work.started", cycle=1, status=ledger.state)
    ledger.add_completed("runtime backbone smoke path")
    ledger.transition("VERIFYING"); events.emit("verify.started", cycle=1, status=ledger.state)
    ledger.transition("COMPLETE"); events.emit("verify.pass", cycle=1, status=ledger.state); events.emit("run.completed", cycle=1, status=ledger.state)
    print(json.dumps(ledger.to_dict(), ensure_ascii=False, indent=2))
