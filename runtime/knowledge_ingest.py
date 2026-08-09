#!/usr/bin/env python3
"""Deterministic Mindway knowledge-stock ingestion primitives.
Network retrieval is intentionally injected by callers; this module never pretends a URL was read.
"""
from __future__ import annotations
import hashlib,json,re
from dataclasses import dataclass,asdict
from datetime import datetime,timezone
from pathlib import Path
from typing import Iterable
VALID_READ={"READ_FULL","READ_DEEP","INDEX_ONLY","NOT_YET_READ","READ_SUMMARY"}
VALID_LANE={"USE_NOW","KNOWLEDGE","STOCK","QUEUE"}
def now(): return datetime.now(timezone.utc).isoformat()
def sid(url:str): return hashlib.sha256(url.encode()).hexdigest()[:16]
@dataclass
class KnowledgeRecord:
    source_url:str; title:str; read_status:str; lane:str; summary:str=""; capabilities:list[str]=None; provenance:str="primary"; verified_at:str=""
    def validate(self):
        if self.read_status not in VALID_READ: raise ValueError("invalid read_status")
        if self.lane not in VALID_LANE: raise ValueError("invalid lane")
        if self.read_status in {"INDEX_ONLY","NOT_YET_READ"} and self.summary.strip(): raise ValueError("unread/index-only item cannot carry content summary")
        return self
    def to_dict(self):
        d=asdict(self);d["capabilities"]=self.capabilities or [];d["record_id"]=sid(self.source_url);d["verified_at"]=self.verified_at or now();return d
def dedupe(records:Iterable[KnowledgeRecord]):
    out={}
    rank={"NOT_YET_READ":0,"INDEX_ONLY":1,"READ_SUMMARY":2,"READ_DEEP":3,"READ_FULL":4}
    for r in records:
        r.validate(); k=sid(r.source_url)
        if k not in out or rank[r.read_status]>rank[out[k].read_status]: out[k]=r
    return list(out.values())
def write_inventory(records,path:Path):
    rows=[r.to_dict() for r in dedupe(records)];path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8");return rows
if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("input");p.add_argument("output");a=p.parse_args()
    raw=json.loads(Path(a.input).read_text(encoding="utf-8")); records=[KnowledgeRecord(**x) for x in raw];write_inventory(records,Path(a.output))
