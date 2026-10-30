from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import torch
torch.set_num_threads(1)
import csv,tempfile
from tasks import load_development,build_loaders,write_predictions
DATA=Path(__file__).resolve().parents[1]/'data/points.csv'
class Checks(unittest.TestCase):
    def test_split(self):
        data,ids=load_development(DATA);self.assertEqual(set(data),{'train','valid'});self.assertEqual([len(ids[s]) for s in ('train','valid','test')],[120,40,40]);self.assertEqual(len(set(sum(ids.values(),[]))),200)
    def test_test_not_parsed(self):
        with DATA.open(encoding='utf-8') as f:rows=list(csv.DictReader(f))
        for row in rows:
            if row['split']=='test':row.update(x1='unreadable',x2='unreadable',label='unreadable')
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'data.csv'
            with path.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
            changed,ids=load_development(path);normal,_=load_development(DATA)
            for s in normal:
                for a,b in zip(normal[s],changed[s]):self.assertTrue(torch.equal(a,b))
    def test_order_seed(self):
        data,ids=load_development(DATA);before=torch.get_rng_state().clone();a,v,g=build_loaders(data);self.assertTrue(torch.equal(before,torch.get_rng_state()))
        b,_,_=build_loaders(data);first=torch.cat([x for x,y in a]);second=torch.cat([x for x,y in b]);self.assertTrue(torch.equal(first,second));self.assertFalse(torch.equal(first,torch.cat([x for x,y in a])));self.assertTrue(torch.equal(torch.cat([x for x,y in v]),data['valid'][0]))
    def test_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'pred.csv';self.assertEqual(write_predictions(p,['b','a'],torch.tensor([1,0]),torch.tensor([[.2,.8],[.9,.1]])),2)
            with p.open(encoding='utf-8-sig') as f:r=list(csv.DictReader(f))
            self.assertEqual([x['id'] for x in r],['b','a']);self.assertEqual([x['predicted'] for x in r],['1','0'])
            before=p.read_bytes()
            with self.assertRaises(ValueError):write_predictions(p,['a'],torch.tensor([0]),torch.ones(2,2))
            self.assertEqual(before,p.read_bytes())
