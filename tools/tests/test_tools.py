import json
import os
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
FX = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(TOOLS))

import adlab_common as C  # noqa: E402
import meta_pull  # noqa: E402
import finance  # noqa: E402
import readout  # noqa: E402
import export  # noqa: E402
import render  # noqa: E402
import higgsfield  # noqa: E402
import manual_pull  # noqa: E402


def run(args, env=None):
    e = dict(os.environ)
    e.update(env or {})
    return subprocess.run([sys.executable, "-I"] + args, capture_output=True, text=True, env=e)


class Common(unittest.TestCase):
    def test_slugify_and_dates(self):
        self.assertEqual(C.slugify("Meta Ads Mastery!"), "meta-ads-mastery")
        self.assertEqual(C.days_between("2026-01-01", "2026-01-11"), 10)
        self.assertIsNone(C.days_between(None))

    def test_frontmatter(self):
        fm, body = C.read_frontmatter(FX / "finance.md")
        self.assertEqual(fm["model"], "membership")
        self.assertEqual(fm["price"], 97)
        self.assertAlmostEqual(fm["trial_to_paid"], 0.6)
        self.assertIn("Placeholder", body)

    def test_frontmatter_inline_comments(self):
        p = Path(tempfile.mkdtemp()) / "f.md"
        p.write_text('---\nprice: 97   # placeholder\nname: "a # b"\nflag: true # yes\n---\nbody\n')
        fm, _ = C.read_frontmatter(p)
        self.assertEqual(fm["price"], 97)
        self.assertEqual(fm["name"], "a # b")
        self.assertIs(fm["flag"], True)


class MetaPull(unittest.TestCase):
    def setUp(self):
        self.fx = json.loads((FX / "meta_search_result.json").read_text())

    def test_walk_and_normalize(self):
        found = []
        meta_pull.walk_ads(self.fx, found)
        self.assertEqual(len(found), 2)
        rec = meta_pull.normalize(found[0], ["skool"])
        self.assertEqual(rec["source"], "meta")
        self.assertEqual(rec["advertiser"], "Skool")
        self.assertTrue(rec["ad_id"].isdigit())
        self.assertEqual(rec["start_date"], "2025-09-04")
        self.assertIn("facebook", rec["platforms"])
        self.assertIn("skool", [t.lower() for t in rec["term_hits"]])
        self.assertTrue(rec["library_url"].endswith(rec["ad_id"]))
        rec2 = meta_pull.normalize(found[1], [])
        self.assertEqual(rec2["format"], "video")
        self.assertTrue(rec2["video_hd_url"] or rec2["video_sd_url"])

    def test_classify_link(self):
        self.assertEqual(meta_pull.classify_link("https://www.skool.com/claude-code-club/about")["dest_type"], "skool")
        self.assertEqual(meta_pull.classify_link("https://shop.example.com/products/x")["dest_type"], "product-page")
        self.assertEqual(meta_pull.classify_link("https://calendly.com/x")["dest_type"], "booking")
        self.assertEqual(meta_pull.classify_link(None)["dest_type"], "none")

    def test_match_kind(self):
        args = Namespace(cobrand_pages=["Skool"], out="/tmp/x")
        p = meta_pull.Puller.__new__(meta_pull.Puller)
        p.args = args
        found = []
        meta_pull.walk_ads(self.fx, found)
        skool = meta_pull.normalize(found[0], [])
        self.assertEqual(p.match_kind(skool, "keyword", "Claude Code Club"), "cobrand")
        self.assertEqual(p.match_kind(skool, "page", "Anything"), "advertiser-page")
        other = meta_pull.normalize(found[1], [])
        self.assertEqual(p.match_kind(other, "keyword", "Claude Code Club"), "keyword-neighbor")

    def test_dry_run(self):
        r = run([str(TOOLS / "meta_pull.py"), "--advertisers", "Acme Co", "--out", tempfile.mkdtemp(), "--dry-run"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("keyword_unordered&q=Acme%20Co", r.stdout)
        self.assertIn("Acme%20Co%20Skool", r.stdout)


class Finance(unittest.TestCase):
    def test_membership_example(self):
        r, lines = finance.compute(finance.EXAMPLES["membership"])
        self.assertAlmostEqual(r["breakeven_cpa"], 97 * 0.95 * 4 * 0.98, places=2)
        self.assertAlmostEqual(r["breakeven_cost_per_trial"], r["breakeven_cpa"] * 0.6, places=2)
        self.assertEqual(r["primary_event"], "trial start")
        self.assertTrue(any("breakeven CPA" in l for l in lines))

    def test_product_example(self):
        r, _ = finance.compute(finance.EXAMPLES["product"])
        self.assertAlmostEqual(r["breakeven_cpa"], 78 * 0.55 * 0.96, places=2)
        self.assertEqual(r["concepts_affordable_per_month"], 3)

    def test_cli_from_file(self):
        out = Path(tempfile.mkdtemp()) / "economics.md"
        r = run([str(TOOLS / "finance.py"), "--file", str(FX / "finance.md"), "--out", str(out)])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("breakeven", out.read_text())


class Readout(unittest.TestCase):
    def test_rules(self):
        ws = Path(tempfile.mkdtemp())
        (ws / "plan").mkdir()
        (ws / "plan" / "thresholds.json").write_text(json.dumps({"target_cpa": 30}))
        r = run([str(TOOLS / "readout.py"), "--workspace", str(ws), "--csv", str(FX / "ads_manager_export.csv")])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("too early", r.stdout)          # c02: 1200 impressions
        self.assertIn("scale", r.stdout)              # c03: CPA 23 < 30, 28 results
        self.assertIn("upstream only", r.stdout)      # c01: 9 results
        self.assertIn("kill or new hook", r.stdout)   # c04: hook 14%
        self.assertTrue(list((ws / "plan" / "readouts").glob("*.md")))

    def test_unset_thresholds_and_aliases(self):
        t = readout.load_thresholds({"ctr_min": None, "hook_rate_min": 0.3, "target_cpa": 30})
        self.assertIsNone(t["min_ctr"])
        self.assertEqual(t["min_hook_rate"], 0.3)
        row = {"impressions": 5000, "clicks": 1, "plays3": 2000, "thruplays": 900, "results": 2, "spend": 50}
        rule, why, m = readout.judge(row, t)                      # CTR 0.02% would fail any floor, but none is set
        self.assertEqual(rule, "upstream only")
        ws = Path(tempfile.mkdtemp())
        (ws / "plan").mkdir()
        (ws / "plan" / "thresholds.json").write_text(json.dumps({"target_cpa": 30, "min_ctr": None, "min_hook_rate": None}))
        r = run([str(TOOLS / "readout.py"), "--workspace", str(ws), "--csv", str(FX / "ads_manager_export.csv")])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("rules are skipped", r.stdout)
        good = {"impressions": 9000, "clicks": 200, "plays3": 4000, "thruplays": 2000, "results": 30, "spend": 600, "frequency": 1.4}
        rule, why, m = readout.judge(good, readout.load_thresholds({"target_cpa": 30, "max_frequency": None}))
        self.assertEqual(rule, "hold")                            # no scaling without a frequency ceiling
        self.assertIn("max_frequency", why)
        rule, why, m = readout.judge(good, readout.load_thresholds({"target_cpa": 30}))
        self.assertEqual(rule, "scale")                           # the default ceiling applies when the key is absent


class Export(unittest.TestCase):
    def test_board_and_csv(self):
        ws = Path(tempfile.mkdtemp())
        for d in C.WORKSPACE_DIRS:
            (ws / d).mkdir(parents=True, exist_ok=True)
        (ws / "bank" / "entries.jsonl").write_text((FX / "entries.jsonl").read_text())
        (ws / "personas" / "p1-buried-owner.md").write_text("---\nid: p1\nname: The buried owner\n---\n")
        (ws / "concepts" / "c01-invoice-pile.md").write_text("---\nconcept_id: c01\nname: The invoice pile\n---\n")
        h, c = export.build(ws)
        html = h.read_text()
        self.assertIn("The invoice pile is still there", html)
        self.assertIn("The buried owner", html)
        self.assertIn("risk: income-claim", html)
        self.assertNotIn("<script src=", html)
        import csv
        with c.open() as f:
            rows = list(csv.reader(f))
        self.assertEqual(rows[0], export.CSV_COLS)
        self.assertEqual(len(rows), 3)


class Render(unittest.TestCase):
    def test_fill(self):
        tpl = (TOOLS.parent / "templates" / "problem-card.html").read_text()
        tpl = render.inline_css(tpl, TOOLS.parent / "templates")
        html = render.fill(tpl, {"hook": "Hello", "offer_line": "", "wordmark": "OW."}, {"primary": "#123456"}, "9x16")
        self.assertIn("--w:1080px;--h:1920px", html)
        self.assertIn("#123456", html)
        self.assertIn("Hello", html)
        self.assertNotIn('class="offer"', html)       # optional block removed when empty
        self.assertNotIn("{{", html)
        self.assertIn("<style>", html)
        self.assertNotIn('rel="stylesheet"', html)

    def test_legibility(self):
        rep = render.legibility({"canvas": [1080, 1350], "runs": [{"t": "x", "fs": 20, "x": 0, "y": 0, "w": 10, "h": 10}]}, 390)
        self.assertFalse(rep["ok"])
        rep = render.legibility({"canvas": [1080, 1350], "runs": [{"t": "x", "fs": 40, "x": 0, "y": 0, "w": 10, "h": 10}]}, 390)
        self.assertTrue(rep["ok"])

    def test_safe_zone_and_bottom_overflow(self):
        ok = {"t": "hook", "fs": 80, "x": 72, "y": 400, "w": 800, "h": 200}
        self.assertTrue(render.legibility({"canvas": [1080, 1920], "runs": [ok]}, 390)["ok"])
        low = dict(ok, t="offer", y=1600, h=50)                        # inside the bottom overlay
        rep = render.legibility({"canvas": [1080, 1920], "runs": [ok, low]}, 390)
        self.assertFalse(rep["ok"])
        self.assertIn("overlay", rep["warnings"][0])
        self.assertTrue(render.legibility({"canvas": [1080, 1350], "runs": [dict(low, y=1200)]}, 390)["ok"])   # 4:5 has no overlay
        over = dict(ok, y=1300, h=100)                                 # runs past the bottom of a 4:5 canvas
        self.assertFalse(render.legibility({"canvas": [1080, 1350], "runs": [over]}, 390)["ok"])


class Higgsfield(unittest.TestCase):
    def test_estimate_and_refusal(self):
        usd, how = higgsfield.estimate("kling/v2.6", 1, 10)
        self.assertAlmostEqual(usd, 0.7)
        usd, how = higgsfield.estimate("nope/model")
        self.assertIsNone(usd)
        ws = tempfile.mkdtemp()
        r = run([str(TOOLS / "higgsfield.py"), "--workspace", ws, "generate", "--model", "higgsfield-ai/soul/v2/standard", "--prompt", "a testimonial from a customer", "--out", ws], env={"ADLAB_HOME": tempfile.mkdtemp()})
        self.assertEqual(r.returncode, 2)
        r = run([str(TOOLS / "higgsfield.py"), "--workspace", ws, "generate", "--model", "higgsfield-ai/soul/v2/standard", "--prompt", "a workshop at dawn", "--out", ws], env={"ADLAB_HOME": tempfile.mkdtemp()})
        self.assertEqual(r.returncode, 0)
        self.assertIn("dry run", r.stdout)


class Manual(unittest.TestCase):
    def test_dry_run_and_stubs(self):
        out = tempfile.mkdtemp()
        r = run([str(TOOLS / "manual_pull.py"), "--urls", "https://www.facebook.com/ads/library/?id=123", "https://adstransparency.google.com/advertiser/AR1/creative/CR9", "--out", out, "--dry-run"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("'123'", r.stdout)
        self.assertIn("g-cr9", r.stdout)
        shots = Path(tempfile.mkdtemp())
        (shots / "ad one.png").write_bytes(b"\x89PNG\r\n\x1a\n")
        r = run([str(TOOLS / "manual_pull.py"), "--screenshots", str(shots), "--advertiser", "Acme", "--out", out])
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = C.read_jsonl(Path(out) / "ads.jsonl")
        self.assertEqual(rows[0]["source"], "manual-screenshot")
        self.assertTrue((Path(out) / "acme" / "shot-ad-one" / "card.png").exists())


class Progress(unittest.TestCase):
    def test_init_set_show(self):
        ws = tempfile.mkdtemp()
        r = run([str(TOOLS / "progress.py"), "--workspace", ws, "init"])
        self.assertEqual(r.returncode, 0, r.stderr)
        r = run([str(TOOLS / "progress.py"), "--workspace", ws, "set", "--step", "pull", "--status", "done", "--count", "12", "--note", "ok"])
        self.assertEqual(r.returncode, 0, r.stderr)
        md = (Path(ws) / "PROGRESS.md").read_text()
        self.assertIn("| pull | done |", md)
        self.assertIn("pull -> done", (Path(ws) / "changelog.md").read_text())


if __name__ == "__main__":
    unittest.main()


class BoardFilters(unittest.TestCase):
    def test_filters_offline(self):
        try:
            from playwright.sync_api import sync_playwright
        except Exception:
            self.skipTest("playwright not installed in this interpreter")
        ws = Path(tempfile.mkdtemp())
        for d in C.WORKSPACE_DIRS:
            (ws / d).mkdir(parents=True, exist_ok=True)
        (ws / "bank" / "entries.jsonl").write_text((FX / "entries.jsonl").read_text())
        h, _ = export.build(ws)
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.goto(h.as_uri())
            self.assertEqual(pg.locator("article:not(.hidden)").count(), 2)
            pg.select_option("#f-persona", "p2")
            self.assertEqual(pg.locator("article:not(.hidden)").count(), 1)
            pg.select_option("#f-persona", "")
            pg.fill("#q", "invoice")
            self.assertEqual(pg.locator("article:not(.hidden)").count(), 1)
            self.assertEqual(pg.inner_text("#count"), "1")
            b.close()
