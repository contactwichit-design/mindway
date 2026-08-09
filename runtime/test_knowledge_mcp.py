import json,tempfile,unittest
from pathlib import Path
from knowledge_ingest import KnowledgeRecord,dedupe,write_inventory
import mindway_mcp_server as mcp
class KnowledgeMCPTests(unittest.TestCase):
 def test_unread_cannot_claim_summary(self):
  with self.assertRaises(ValueError): KnowledgeRecord('https://x','x','INDEX_ONLY','QUEUE','claimed content').validate()
 def test_dedupe_prefers_deeper_read(self):
  a=KnowledgeRecord('https://x','x','INDEX_ONLY','QUEUE')
  b=KnowledgeRecord('https://x','x','READ_FULL','KNOWLEDGE','verified summary')
  self.assertEqual(dedupe([a,b])[0].read_status,'READ_FULL')
 def test_inventory_write(self):
  with tempfile.TemporaryDirectory() as td:
   rows=write_inventory([KnowledgeRecord('https://x','x','NOT_YET_READ','QUEUE')],Path(td)/'i.json')
   self.assertEqual(len(rows),1)
 def test_mcp_initialize(self):
  out=mcp.handle({'jsonrpc':'2.0','id':1,'method':'initialize','params':{}})
  self.assertEqual(out['result']['serverInfo']['name'],'mindway-local')
 def test_mcp_lists_skills(self):
  out=mcp.handle({'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'list_skills','arguments':{}}})
  self.assertIn('loop',out['result']['content'][0]['text'])
if __name__=='__main__':unittest.main()
