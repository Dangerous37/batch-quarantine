import json
import subprocess
import sys
import unittest
from pathlib import Path

from engine import evaluate


def example():
    return json.loads(Path(__file__).with_name("example.json").read_text(encoding="utf-8"))


class AcceptanceTests(unittest.TestCase):
    def test_example_cli(self):
        proc = subprocess.run([sys.executable, "cli.py", "example.json"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), evaluate(example()))

    def test_all_causes_and_all_duplicate_owners(self):
        issues = evaluate(example())["issues"]
        self.assertEqual([(r["row"], r["reason"]) for r in issues],
                         [(1,"duplicate"),(2,"duplicate"),(2,"wrong_type"),(3,"unexpected"),(3,"missing")])

    def test_release_clean_batch(self):
        data = example()
        data["rows"] = [{"id": 1, "qty": 0}]
        self.assertEqual(evaluate(data)["verdict"], "release")

    def test_invalid_contract_is_not_a_clean_batch(self):
        data = example()
        data["schema"]["qty"] = "anything"
        with self.assertRaises(ValueError):
            evaluate(data)
