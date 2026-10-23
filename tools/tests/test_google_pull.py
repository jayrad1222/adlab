"""Tests for google_pull.py: parsing and normalization on live-captured fixtures, plus --dry-run.
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
import google_pull as G  # noqa: E402


def load(name):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


class TestParsing(unittest.TestCase):
    def test_search_creatives(self):
        items = G.parse_search_creatives(load("google_search_creatives.json"))
        self.assertEqual(len(items), 2)
        by_id = {i["creative_id"]: i for i in items}
        vid = by_id["CR14928184037351620609"]
        self.assertEqual(vid["advertiser_id"], "AR10942234166510485505")
        self.assertEqual(vid["advertiser"], "BlueVision Interactive Limited")
        self.assertEqual(vid["format"], "video")
        self.assertEqual(vid["first_shown"], "2026-10-21")
        self.assertEqual(vid["last_shown"], "2026-10-23")
        self.assertTrue(vid["preview_url"].startswith("https://displayads-formats.googleusercontent.com/ads/preview/content.js"))
        self.assertEqual(by_id["CR09413704852606812161"]["format"], "image")
        self.assertEqual(by_id["CR09413704852606812161"]["first_shown"], "2023-06-16")

    def test_suggestions(self):
        advs, doms = G.parse_suggestions(load("google_suggestions.json"))
        names = {a["name"]: a for a in advs}
        self.assertIn("Notion Limited", names)
        self.assertEqual(names["Notion Limited"]["advertiser_id"], "AR01024198173649797121")
        self.assertEqual(names["Notion Limited"]["country"], "GB")
        self.assertEqual(names["Notion Limited"]["ad_count"], 75)
        self.assertIn("notion.com", doms)

    def test_creative_detail(self):
        d = G.parse_creative_detail(load("google_creative_detail_video.json"))
        self.assertEqual(d["creative_id"], "CR14928184037351620609")
        self.assertEqual(d["format"], "video")
        self.assertEqual(len(d["variants"]), 2)
        self.assertEqual(d["regions"], [{"region_code": 2764, "last_shown": "2026-10-22"}])
        self.assertEqual(d["advertiser"], "BlueVision Interactive Limited")
        t = G.parse_creative_detail(load("google_creative_detail_text.json"))
        self.assertEqual(t["format"], "text")
        self.assertIn("simgad", t["variants"][0]["html"])

    def test_preview_script_video(self):
        p = G.parse_preview_script((FIX / "google_preview_video.js").read_text(encoding="utf-8"))
        self.assertEqual(p["youtube_id"], "tSvdKFeBvD0")
        self.assertEqual(p["kind"], "image")
        self.assertEqual((p["width"], p["height"]), (480, 360))

    def test_preview_script_image(self):
        p = G.parse_preview_script((FIX / "google_preview_image.js").read_text(encoding="utf-8"))
        self.assertIsNone(p["youtube_id"])
        self.assertEqual(p["kind"], "html")
        self.assertEqual(p["image_urls"], ["https://tpc.googlesyndication.com/simgad/12345678901234567890"])
        self.assertEqual(p["dest_url"], "https://example.com/products/topper?variant=1")
        self.assertEqual((p["width"], p["height"]), (300, 250))

    def test_creative_dom(self):
        d = G.parse_creative_dom((FIX / "google_creative_dom.txt").read_text(encoding="utf-8"))
        self.assertEqual(d["last_shown"], "2026-10-22")
        self.assertEqual(d["format"], "video")
        self.assertEqual(d["region_text"], "Shown anywhere")
        self.assertEqual((d["variant_index"], d["variant_count"]), (1, 2))
        self.assertEqual(G.parse_creative_dom(""), {"last_shown": None, "format": None, "region_text": None,
                                                    "variant_index": None, "variant_count": None})


class TestNormalize(unittest.TestCase):
    def test_video_record(self):
        items = {i["creative_id"]: i for i in G.parse_search_creatives(load("google_search_creatives.json"))}
        detail = G.parse_creative_detail(load("google_creative_detail_video.json"))
        preview = G.parse_preview_script((FIX / "google_preview_video.js").read_text(encoding="utf-8"))
        dom = G.parse_creative_dom((FIX / "google_creative_dom.txt").read_text(encoding="utf-8"))
        rec = G.normalize(items["CR14928184037351620609"], detail, preview, dom, ["bluevision", "nothing"])
        self.assertEqual(rec["source"], "google")
        self.assertEqual(rec["ad_id"], "g-CR14928184037351620609")
        self.assertEqual(rec["advertiser_slug"], "bluevision-interactive-limited")
        self.assertEqual(rec["format"], "video")
        self.assertEqual(rec["platforms"], ["youtube"])
        self.assertEqual(rec["start_date"], "2026-10-21")
        self.assertEqual(rec["end_date"], "2026-10-22")
        self.assertEqual(rec["days_active"], 1)
        self.assertEqual(rec["variant_count"], 2)
        self.assertEqual(rec["video_hd_url"], "https://www.youtube.com/watch?v=tSvdKFeBvD0")
        self.assertEqual(rec["video_preview_image_url"], "https://i.ytimg.com/vi/tSvdKFeBvD0/hqdefault.jpg")
        self.assertEqual(rec["library_url"], "https://adstransparency.google.com/advertiser/AR10942234166510485505/creative/CR14928184037351620609?region=anywhere")
        self.assertEqual(rec["term_hits"], ["bluevision"])
        self.assertIsNone(rec["is_active"])
        self.assertIsNone(rec["link_url"])
        self.assertEqual(rec["dest_type"], "none")
        self.assertEqual(rec["raw_snapshot"]["search_item"]["2"], "CR14928184037351620609")
        # every meta_pull key is present
        for k in G.blank_record():
            self.assertIn(k, rec)

    def test_inline_preview_html_item(self):
        # Notion Limited's creatives carry an <img> snippet instead of a preview-script URL (live, Oct 2026)
        obj = {"1": [{"1": "AR01024198173649797121", "2": "CR00618348339980664833",
                      "3": {"3": {"2": "<img src=\"https://tpc.googlesyndication.com/archive/simgad/1759736663096250972\" height=\"250\" width=\"300\">"}},
                      "4": 2, "6": {"1": "1790000000"}, "7": {"1": "1792000000"}, "12": "Notion Limited"}]}
        it = G.parse_search_creatives(obj)[0]
        self.assertIsNone(it["preview_url"])
        self.assertIn("archive/simgad", it["preview_html"])
        rec = G.normalize(it, {}, {}, {"frame_text": "Notion AI | Try it free"}, ["notion"])
        self.assertEqual(rec["image_url"], "https://tpc.googlesyndication.com/archive/simgad/1759736663096250972")
        self.assertEqual(rec["body_text"], "Notion AI | Try it free")
        self.assertEqual(rec["advertiser_slug"], "notion-limited")
        self.assertEqual(rec["term_hits"], ["notion"])

    def test_image_record_without_detail(self):
        items = {i["creative_id"]: i for i in G.parse_search_creatives(load("google_search_creatives.json"))}
        preview = G.parse_preview_script((FIX / "google_preview_image.js").read_text(encoding="utf-8"))
        rec = G.normalize(items["CR09413704852606812161"], {}, preview, {}, [])
        self.assertEqual(rec["format"], "image")
        self.assertEqual(rec["platforms"], ["google"])
        self.assertEqual(rec["image_url"], "https://tpc.googlesyndication.com/simgad/12345678901234567890")
        self.assertEqual(rec["link_url"], "https://example.com/products/topper?variant=1")
        self.assertEqual(rec["link_domain"], "example.com")
        self.assertEqual(rec["dest_type"], "product-page")
        self.assertIsNone(rec["variant_count"])
        self.assertIsNone(rec["video_hd_url"])


class TestDryRun(unittest.TestCase):
    def test_dry_run_prints_urls(self):
        with tempfile.TemporaryDirectory() as td:
            out = subprocess.run([sys.executable, "-I", str(TOOLS / "google_pull.py"), "--advertisers", "Notion",
                                  "--domains", "notion.so", "--advertiser-ids", "AR01024198173649797121",
                                  "--out", td, "--dry-run"], capture_output=True, text=True, timeout=60)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("https://adstransparency.google.com/?region=anywhere&domain=notion.so", out.stdout)
        self.assertIn("https://adstransparency.google.com/advertiser/AR01024198173649797121?region=anywhere", out.stdout)
        self.assertIn("type 'Notion' in the search box", out.stdout)
        self.assertNotIn("Traceback", out.stderr)


if __name__ == "__main__":
    unittest.main()
