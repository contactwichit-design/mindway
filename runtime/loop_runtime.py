#!/usr/bin/env python3
"""Provider-agnostic Mindway /loop runtime v2.
Enforces scoped failure closure, real payload redaction, explicit trace causality,
semantic checkpoint snapshots, and approval-aware completion.
"""
from __future__ import annotations
import hashlib, json, uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

TERMINAL={"COMPLETE","NEED_USER","BLOCKED","PLATFORM_LIMIT","CYCLE_LIMIT","FAILED"}
TOPOLOGIES={"SEQUENTIAL","PARALLEL","HYBRID"}
EVENT_TYPES={"run.created","orient.started","plan.created","route.selected","work.started","work.completed","tool.called","tool.succeeded","tool.failed","verify.started","verify.pass","verify.fail","fix.started","fix.completed","failure.detected","failure.diagnosed","failure.patched","failure.verified","failure.closed","failure.reopened","improvement.proposed","approval.required","approval.validated","checkpoint.saved","run.resumed","run.completed","run.stopped"}
ALLOWED={"NEW":{"ORIENTING"},"ORIENTING":{"PLANNED","NEED_USER","BLOCKED"},"PLANNED":{"RUNNING","NEED_USER","BLOCKED"},"RUNNING":{"VERIFYING","CHECKPOINTED","NEED_USER","BLOCKED","PLATFORM_LIMIT","CYCLE_LIMIT","FAILED"},"VERIFYING":{"COMPLETE","FIXING","CHECKPOINTED","NEED_USER","BLOCKED","FAILED"},"FIXING":{"VERIFYING","RUNNING","CHECKPOINTED","NEED_USER","BLOCKED","FAILED"},"CHECKPOINTED":{"RUNNING","NEED_USER","BLOCKED","PLATFORM_LIMIT"}}

def now(): return datetime.now(timezone.utc).isoformat()
def stable_id(prefix):
    if not prefix: raise ValueError("id prefix must be non-empty")
    return f"{prefix}_{uuid.uuid4().hex}"
def checksum_bytes(data): return hashlib.sha256(data).hexdigest()
def _budget(v,n):
    if v is not None and (not isinstance(v,int) or isinstance(v,bool) or not 1<=v<=99): raise ValueError(f"{n} must be 1..99 or None")

def _redact(payload: Dict[str,Any], fields: List[str]) -> Dict[str,Any]:
    """Redact dotted paths before persistence; never retain the original value."""
    clean=json.loads(json.dumps(payload,ensure_ascii=False))
    for path in fields:
        parts=path.split("."); cur=clean
        for part in parts[:-1]:
            if not isinstance(cur,dict) or part not in cur: cur=None; break
            cur=cur[part]
        if isinstance(cur,dict) and parts[-1] in cur: cur[parts[-1]]="[REDACTED]"
    return clean

@dataclass
class RunLedger:
    mission:str
    requested_cycles:Optional[int]=None; estimated_cycles:Optional[int]=None; topology:Optional[str]=None
    run_id:str=field(default_factory=lambda:stable_id("run")); schema_version:str="2.0"; state:str="NEW"; completed_cycles:int=0
    created_at:str=field(default_factory=now); updated_at:str=field(default_factory=now)
    completed:List[Dict[str,Any]]=field(default_factory=list); blocked_branches:List[Dict[str,Any]]=field(default_factory=list)
    next_action:Optional[str]=None; risks:List[str]=field(default_factory=list); approval_gates:List[str]=field(default_factory=list)
    validated_approvals:List[str]=field(default_factory=list); source_versions:Dict[str,str]=field(default_factory=dict)
    semantic_snapshot:Dict[str,str]=field(default_factory=dict); open_failures:List[Dict[str,Any]]=field(default_factory=list)
    artifacts:List[str]=field(default_factory=list); checkpoint:Optional[Dict[str,str]]=None; stop_reason:Optional[str]=None
    def __post_init__(self):
        if not isinstance(self.mission,str) or not self.mission.strip(): raise ValueError("mission required")
        if self.schema_version!="2.0": raise ValueError("unsupported schema_version")
        _budget(self.requested_cycles,"requested_cycles"); _budget(self.estimated_cycles,"estimated_cycles")
        if self.topology is not None and self.topology not in TOPOLOGIES: raise ValueError("invalid topology")
        if self.state not in set(ALLOWED)|TERMINAL: raise ValueError("invalid state")
    def consequential_open_failures(self):
        terminal={"CLOSED","DEFERRED"}
        return [f for f in self.open_failures if f.get("mission_relevant",True) and f.get("state") not in terminal]
    def can_complete(self):
        approvals_ok=set(self.approval_gates).issubset(set(self.validated_approvals))
        return not self.consequential_open_failures() and approvals_ok
    def transition(self,new_state):
        if self.state in TERMINAL: raise ValueError("terminal state cannot transition")
        if new_state not in ALLOWED.get(self.state,set()): raise ValueError(f"invalid transition {self.state} -> {new_state}")
        if new_state=="COMPLETE" and not self.can_complete(): raise ValueError("completion gate failed: unresolved failure or approval")
        self.state=new_state; self.updated_at=now()
    def add_failure(self,failure_class,scope,severity="S2",mission_relevant=True,state="DETECTED"):
        item={"id":stable_id("fail"),"failure_class":failure_class,"scope":scope,"severity":severity,"mission_relevant":mission_relevant,"state":state}
        self.open_failures.append(item); self.updated_at=now(); return item
    def add_completed(self,item,evidence=None): self.completed.append({"item":item,"evidence":evidence or []}); self.updated_at=now()
    def to_dict(self): return asdict(self)
    @classmethod
    def from_dict(cls,data): return cls(**data)

class EventLog:
    def __init__(self,run_id,events=None): self.run_id=run_id; self.events=list(events or [])
    def emit(self,event_type,*,cycle=0,actor=None,subject=None,status=None,evidence=None,payload=None,redacted_fields=None,trace_id=None,span_id=None,parent_span_id=None,links=None,branch_id=None):
        if event_type not in EVENT_TYPES: raise ValueError("unknown event type")
        fields=redacted_fields or []; safe=_redact(payload or {},fields)
        event={"schema_version":"2.0","event_id":stable_id("evt"),"run_id":self.run_id,"type":event_type,"timestamp":now(),"sequence":len(self.events),"cycle":cycle,"actor":actor,"subject":subject,"status":status,"evidence":evidence or [],"payload":safe,"trace_id":trace_id or self.run_id,"span_id":span_id or stable_id("span"),"parent_span_id":parent_span_id,"links":links or [],"branch_id":branch_id,"redaction":{"applied":bool(fields),"fields":fields}}
        self.events.append(event); return event
    def write_jsonl(self,path): path.parent.mkdir(parents=True,exist_ok=True); path.write_text("".join(json.dumps(e,ensure_ascii=False)+"\n" for e in self.events),encoding="utf-8")

def save_checkpoint(ledger,events,directory):
    if events.run_id!=ledger.run_id: raise ValueError("run_id mismatch")
    if not ledger.semantic_snapshot: raise ValueError("semantic_snapshot required before checkpoint")
    directory.mkdir(parents=True,exist_ok=True); payload={"ledger":ledger.to_dict(),"events":events.events}; raw=json.dumps(payload,ensure_ascii=False,indent=2).encode(); digest=checksum_bytes(raw); path=directory/f"{ledger.run_id}.checkpoint.json"; path.write_bytes(raw); ledger.checkpoint={"uri":str(path),"checksum":digest,"saved_at":now()}; return ledger.checkpoint

def load_checkpoint(path,expected_checksum=None):
    raw=path.read_bytes(); digest=checksum_bytes(raw)
    if expected_checksum and digest!=expected_checksum: raise ValueError("checkpoint checksum mismatch")
    return {"checksum":digest,"data":json.loads(raw.decode())}

def resume_checkpoint(path,expected_checksum=None,current_semantic_snapshot=None):
    loaded=load_checkpoint(path,expected_checksum); ledger=RunLedger.from_dict(loaded["data"]["ledger"])
    if current_semantic_snapshot is not None and ledger.semantic_snapshot!=current_semantic_snapshot: raise ValueError("semantic snapshot incompatible; re-orient required")
    return ledger,EventLog(ledger.run_id,loaded["data"]["events"])
