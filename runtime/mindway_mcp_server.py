#!/usr/bin/env python3
"""Minimal dependency-free, read-first Mindway MCP stdio server.
Implements initialize, tools/list, tools/call and resources/list/read for local grounding.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RES={"mindway://canonical/my":"my.md","mindway://runtime/loop":"skills/loop/SKILL.md","mindway://schemas/event":"runtime/schemas/mindway_event.schema.json","mindway://schemas/run":"runtime/schemas/mindway_run.schema.json","mindway://schemas/skill":"runtime/schemas/mindway_skill.schema.json"}
def safe_read(rel):
 p=(ROOT/rel).resolve()
 if ROOT not in p.parents and p!=ROOT: raise ValueError("path outside repository")
 return p.read_text(encoding="utf-8")
def skills():
 base=ROOT/'skills';return sorted([p.parent.name for p in base.glob('*/SKILL.md')]) if base.exists() else []
def result(i,x): return {"jsonrpc":"2.0","id":i,"result":x}
def error(i,msg): return {"jsonrpc":"2.0","id":i,"error":{"code":-32602,"message":msg}}
def handle(r):
 i=r.get('id');m=r.get('method');p=r.get('params') or {}
 if m=='initialize': return result(i,{"protocolVersion":"2025-03-26","capabilities":{"resources":{},"tools":{}},"serverInfo":{"name":"mindway-local","version":"0.1.0"}})
 if m=='notifications/initialized': return None
 if m=='resources/list': return result(i,{"resources":[{"uri":u,"name":u.split('/')[-1],"mimeType":"text/markdown" if f.endswith('.md') else 'application/json'} for u,f in RES.items()]})
 if m=='resources/read':
  u=p.get('uri');
  if u not in RES:return error(i,'unknown resource')
  return result(i,{"contents":[{"uri":u,"text":safe_read(RES[u])}]})
 if m=='tools/list': return result(i,{"tools":[{"name":"list_skills","description":"List installed Mindway skill IDs","inputSchema":{"type":"object","properties":{}}},{"name":"get_skill","description":"Read one installed Mindway SKILL.md","inputSchema":{"type":"object","properties":{"skill_id":{"type":"string"}},"required":["skill_id"]}}]})
 if m=='tools/call':
  name=p.get('name');a=p.get('arguments') or {}
  if name=='list_skills': data=skills()
  elif name=='get_skill':
   sid=a.get('skill_id','');
   if sid not in skills(): return error(i,'unknown skill')
   data=safe_read(f'skills/{sid}/SKILL.md')
  else:return error(i,'unknown tool')
  return result(i,{"content":[{"type":"text","text":json.dumps(data,ensure_ascii=False) if not isinstance(data,str) else data}]})
 return error(i,'method not supported')
def main():
 for line in sys.stdin:
  try:
   r=json.loads(line);out=handle(r)
   if out is not None: print(json.dumps(out,ensure_ascii=False),flush=True)
  except Exception as e: print(json.dumps(error(None,str(e))),flush=True)
if __name__=='__main__':main()
