"""Tests for tiktok_ccl_pull.py: search/detail parsing and normalization on live-captured fixtures, plus --dry-run.
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
FIX = HERE / "fixtures"
sys.path.insert(0, str(TOOLS))
import tiktok_ccl_pull as T  # noqa: E402


def load(name):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


class TestParsing(unittest.TestCase):
    def test_search(self):
        items, total, has_more = T.parse_search(load("tiktok_search.json"))
        self.assertEqual(len(items), 2)
        self.assertEqual(total, 2523)
        self.assertTrue(has_more)
        it = items[0]
        self.assertEqual(it["id"], "1872062858846226")
        self.assertEqual(it["name"], "Duolingo, Inc.")
        self.assertEqual(it["title"], "New on Duolingo: Chess")
        self.assertIn("cover_img", it["videos"][0])
        self.assertEqual(T.parse_search({"code": 0}), ([], None, None))
        self.assertEqual(T.parse_search("nope"), ([], None, None))

    def test_detail(self):
        d = T.parse_detail(load("tiktok_detail.json"))
        self.assertEqual(d["ad"]["id"], "1872062858846226")
        self.assertEqual(d["ad"]["download_url"], "https://play.google.com/store/apps/details?id=com.duolingo&hl=en_US")
        self.assertEqual(d["advertiser"]["adv_biz_ids"], "6876458959876653825")
        self.assertEqual(d["advertiser"]["registry_location"], "United States")
        self.assertEqual(d["advertiser"]["tt_user"]["username"], "duolingo")
        self.assertEqual(d["sponsor"], "Duolingo, Inc.")
        self.assertEqual(d["targeting"]["target_audience_size"], "103.7M-126.7M")
        self.assertEqual(d["display_mode"], "standard")
        self.assertEqual(T.parse_detail({}), {"ad": {}, "advertiser": {}, "sponsor": None, "targeting": None, "display_mode": None})

    def test_dates(self):
        self.assertEqual(T.ms_to_date(1785283200000), "2026-07-29")
        self.assertEqual(T.ms_to_date(1792540800000), "2026-10-21")
        self.assertIsNone(T.ms_to_date(None))
        s, e = T.window_ms(365)
        self.assertGreater(e, s)
        self.assertAlmostEqual((e - s) / 86400000.0, 366, delta=0.01)


class TestNormalize(unittest.TestCase):
    def test_video_record_with_detail(self):
        items, _, _ = T.parse_search(load("tiktok_search.json"))
        detail = T.parse_detail(load("tiktok_detail.json"))
        rec = T.normalize(items[0], detail, ["chess", "zebra"])
        self.assertEqual(rec["source"], "tiktok-ccl")
        self.assertEqual(rec["ad_id"], "tt-1872062858846226")
        self.assertEqual(rec["advertiser"], "Duolingo, Inc.")
        self.assertEqual(rec["advertiser_id"], "6876458959876653825")
        self.assertEqual(rec["advertiser_slug"], "duolingo-inc")
        self.assertEqual(rec["platforms"], ["tiktok"])
        self.assertEqual(rec["start_date"], "2026-07-29")
        self.assertEqual(rec["end_date"], "2026-10-21")
        self.assertEqual(rec["days_active"], 84)
        self.assertEqual(rec["format"], "video")
        self.assertEqual(rec["title"], "New on Duolingo: Chess")
        self.assertIsNone(rec["image_url"])
        self.assertIn("tiktokcdn.com", rec["video_preview_image_url"])
        self.assertTrue(rec["video_hd_url"].startswith("https://library.tiktok.com/api/v1/cdn/"))
        self.assertEqual(rec["link_url"], "https://play.google.com/store/apps/details?id=com.duolingo&hl=en_US")
        self.assertEqual(rec["dest_type"], "app-store")
        self.assertEqual(rec["byline"], "Duolingo, Inc.")
        self.assertEqual(rec["page_categories"], ["Apps"])
        self.assertEqual(rec["page_profile_uri"], "https://www.tiktok.com/share/user/6917704832925746181?source=ad_review")
        self.assertEqual(rec["tiktok_username"], "duolingo")
        self.assertEqual(rec["eu"]["target_audience_size"], "103.7M-126.7M")
        self.assertIn("targeting", rec["eu"])
        self.assertNotIn("estimated_audience", rec["eu"])  # the library showed "-" so it is not invented
        self.assertEqual(rec["library_url"], "https://library.tiktok.com/ads/detail/?ad_id=1872062858846226")
        self.assertEqual(rec["term_hits"], ["chess"])
        self.assertIsNone(rec["is_active"])
        self.assertIsNone(rec["variant_count"])
        self.assertEqual(rec["raw_snapshot"]["search_item"]["id"], "1872062858846226")
        for k in T.blank_record():
            self.assertIn(k, rec)

    def test_record_without_detail(self):
        items, _, _ = T.parse_search(load("tiktok_search.json"))
        rec = T.normalize(items[1], {}, [])
        self.assertEqual(rec["advertiser_id"], "")
        self.assertIsNone(rec["eu"])
        self.assertIsNone(rec["link_url"])
        self.assertIsNone(rec["byline"])
        self.assertEqual(rec["format"], "video")


class TestDryRun(unittest.TestCase):
    def test_dry_run_prints_urls(self):
        with tempfile.TemporaryDirectory() as td:
            out = subprocess.run([sys.executable, "-I", str(TOOLS / "tiktok_ccl_pull.py"), "--advertisers", "Duolingo",
                                  "--keywords", "language learning", "--out", td, "--dry-run"],
                                 capture_output=True, text=True, timeout=60)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("https://library.tiktok.com/ads?region=all&start_time=", out.stdout)
        self.assertIn("adv_name=Duolingo&adv_biz_ids=&query_type=1", out.stdout)
        self.assertIn("adv_name=language%20learning&adv_biz_ids=&query_type=2", out.stdout)
        self.assertIn("https://library.tiktok.com/ads/detail/?ad_id=<id>", out.stdout)
        self.assertNotIn("Traceback", out.stderr)


if __name__ == "__main__":
    unittest.main()
