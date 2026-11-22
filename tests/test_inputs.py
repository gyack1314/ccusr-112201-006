"""Existing tests validate input integrity, not the undeveloped application."""
from pathlib import Path
import json
import unittest
from tools.inspect_inputs import inspect
ROOT=Path(__file__).resolve().parents[1]
class InputTest(unittest.TestCase):
    def test_integrity(self):
        counts=inspect(ROOT)
        self.assertTrue(counts)
        self.assertTrue(all(count>0 for count in counts.values()))
    def test_local_synthetic_catalog(self):
        catalog=json.loads((ROOT/"data/catalog.json").read_text(encoding="utf-8"))
        self.assertIs(catalog["synthetic"],True)
        self.assertTrue(all("/" not in name and ".." not in name for name in catalog["tables"]))
