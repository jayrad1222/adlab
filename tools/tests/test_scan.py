"""Tests for scan.py: risky lines in a small bank are found, grouped across entries, and written.
No network. Run: python3 -I -m unittest discover -s tools/tests -p "test_*.py"
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
sys.path.insert(0, str(TOOLS))
import scan  # noqa: E402


def workspace(with_roster=True):
    ws = Path(tempfile.mkdtemp())
    (ws / "bank").mkdir()
    (ws / "competitors").mkdir()
    shared = "Guaranteed results. 50% off today only."
    rows = [
        {"entry_id": "c01-e01", "status": "ready", "hook": "The quote is still in drafts at 10pm.", "primary_text_short": shared,
         "hooks": ["Better than Acme Widgets [comparison]"], "layout_fields": {"hook": "Join 4,000 members", "photo_image": "x.png"}},
        {"entry_id": "c01-e02", "status": "draft", "hook": "A plain line with nothing to flag.", "primary_text_short": shared,
         "layout_fields": {"cards": [{"step": "1", "hook": "Free for 7 days", "body": "Cancel anytime."}]}},
    ]
    (ws / "bank" / "entries.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    if with_roster:
        (ws / "competitors" / "roster.json").write_text(json.dumps({"advertisers": [{"name": "Acme Widgets", "page_names": []}]}), encoding="utf-8")
    return ws


class Scan(unittest.TestCase):
    def test_categories_and_grouping(self):
        ws = workspace()
        entries, hits, per_cat = scan.scan(ws)
        cats = {h["category"] for h in hits}
        for c in ("number", "guarantee", "income or results", "scarcity or urgency", "free or discount", "counts and ratings", "competitor name"):
            self.assertIn(c, cats, c)
        rows = scan.group(hits)
        shared = [r for r in rows if r["category"] == "guarantee"]
        self.assertEqual(len(shared), 1)                       # one line carried by two entries
        self.assertEqual(len(shared[0]["where"]), 2)
        self.assertFalse(any("x.png" in h["text"] for h in hits))   # image paths are not ad text

    def test_cli_writes_markdown(self):
        ws = workspace(with_roster=False)
        r = subprocess.run([sys.executable, "-I", str(TOOLS / "scan.py"), "--workspace", str(ws)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        md = (ws / "analysis" / "scan.md").read_text(encoding="utf-8")
        self.assertIn("Lines in ready, rendered or testing entries", md)
        self.assertIn("Lines only in draft or held entries", md)
        self.assertNotIn("competitor name", md)               # no roster, no competitor names
        self.assertIn("distinct lines to check", r.stdout)

    def test_missing_bank(self):
        ws = Path(tempfile.mkdtemp())
        r = subprocess.run([sys.executable, "-I", str(TOOLS / "scan.py"), "--workspace", str(ws)], capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
