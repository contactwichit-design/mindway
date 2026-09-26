#!/usr/bin/env python3
"""Executable Recursive Improvement Loop (RIL) primitives for Mindway.

The graph makes reusable failure debt explicit, blocks false completion for
mission-relevant failures, and permits unrelated safe work to continue.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional
import uuid

LIFECYCLE={"DETECTED","DIAGNOSED","PATCHED_NOT_VERIFIED","TESTED","VERIFIED","CLOSED","DEFERRED","BLOCKED","REOPENED"}
SEVERITIES={"S0","S1","S2","S3","S4"}

@dataclass
class FailureNode:
    failure_class: str
    scope: str
    severity: str="S2"
    mission_relevant: bool=True
    id: str=field(default_factory=lambda: "fail_"+uuid.uuid4().hex)
    state: str="DETECTED"
    root_cause: Optional[str]=None
    fix_radius: List[str]=field(default_factory=list)
    risk_radius: List[str]=field(default_factory=list)
    test_radius: List[str]=field(default_factory=list)
    analogs_checked: List[str]=field(default_factory=list)
    evidence: List[str]=field(default_factory=list)
    children: List[str]=field(default_factory=list)
    deferred_reason: Optional[str]=None
    next_action: Optional[str]=None

    def __post_init__(self):
        if self.state not in LIFECYCLE: raise ValueError("invalid failure state")
        if self.severity not in SEVERITIES: raise ValueError("invalid severity")
        if not self.failure_class or not self.scope: raise ValueError("failure_class and scope required")

    def closable(self) -> bool:
        return bool(self.root_cause and self.evidence and self.test_radius and self.state in {"VERIFIED","CLOSED"})

    def transition(self, state: str):
        if state not in LIFECYCLE: raise ValueError("invalid failure state")
        if state=="CLOSED" and not self.closable(): raise ValueError("failure is not closable")
        self.state=state

@dataclass
class FailureGraph:
    nodes: Dict[str,FailureNode]=field(default_factory=dict)

    def add(self,node:FailureNode,parent_id:Optional[str]=None):
        self.nodes[node.id]=node
        if parent_id:
            if parent_id not in self.nodes: raise KeyError(parent_id)
            self.nodes[parent_id].children.append(node.id)
        return node.id

    def consequential_open(self, scope:Optional[str]=None):
        terminal={"CLOSED","DEFERRED"}
        return [n for n in self.nodes.values() if n.state not in terminal and n.mission_relevant and (scope is None or n.scope==scope)]

    def can_complete(self) -> bool:
        return not self.consequential_open()

    def to_dict(self):
        return {k:asdict(v) for k,v in self.nodes.items()}
