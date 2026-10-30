from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import torch
torch.set_num_threads(1)
import json
from unittest.mock import patch
from tasks import choose_device,probe_device
class Checks(unittest.TestCase):
    def test_cpu(self): self.assertEqual(str(choose_device('cpu')),'cpu')
    def test_auto_no_cuda(self):
        with patch('torch.cuda.is_available',return_value=False):self.assertEqual(str(choose_device('auto')),'cpu')
    def test_explicit_unavailable(self):
        with patch('torch.cuda.is_available',return_value=False):
            with self.assertRaises(RuntimeError):choose_device('cuda')
    def test_invalid(self):
        with self.assertRaises(ValueError):choose_device('gpu')
    def test_report(self):
        report=probe_device('cpu');json.dumps(report)
        self.assertEqual(report['result'],[2.,3.]);self.assertEqual(report['tensor_device'],'cpu')
    def test_rng_preserved(self):
        before=torch.get_rng_state().clone();probe_device('cpu');self.assertTrue(torch.equal(before,torch.get_rng_state()))
    @unittest.skipUnless(torch.cuda.is_available(),'실제 CUDA 장치 없음')
    def test_real_cuda(self):self.assertEqual(probe_device('cuda')['tensor_device'],'cuda:0')
