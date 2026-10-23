"""Tests for linkedin_pull.py: HTML parsing and normalization on live-captured fixtures, plus --dry-run.
No network. Run: python3 -I -m unittest discover -s tools/tests -p "test_*.py"
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
FIX = HERE / "fixtures"
sys.path.insert(0, str(TOOLS))
import linkedin_pull as L  # noqa: E402


def read(name):
    return (FIX / name).read_text(encoding="utf-8")


class TestSearchPage(unittest.TestCase):
    def setUp(self):
        self.html = read("linkedin_search.html")

    def test_result_count_and_pagination(self):
        self.assertEqual(L.parse_result_count(self.html), 5333)
        meta = L.parse_pagination(self.html)
        self.assertFalse(meta["isLastPage"])
        self.assertEqual(meta["paginationToken"], "1620070786-1789313137421")
        self.assertEqual(L.parse_pagination("<html></html>"), {})

    def test_cards(self):
        cards = L.parse_search_cards(self.html)
        self.assertEqual(len(cards), 3)
        types = [c["creative_type"] for c in cards]
        self.assertEqual(types, ["SPONSORED_VIDEO", "SPONSORED_STATUS_UPDATE", "SPONSORED_UPDATE_NATIVE_DOCUMENT"])
        video = cards[0]
        self.assertEqual(video["ad_id"], "1640238106")
        self.assertEqual(video["advertiser"], "Notion")
        self.assertEqual(video["ad_type_label"], "Video Ad")
        self.assertTrue(video["body_text"].startswith("When Rakuten France set out"))
        self.assertEqual(video["headline"], "Learn more")
        self.assertIn("videocover", video["image_url"])
        self.assertIn("company-logo", video["logo_url"])
        self.assertEqual(video["detail_url"], "https://www.linkedin.com/ad-library/detail/1640238106")
        image = cards[1]
        self.assertEqual(image["advertiser"], "Notion Korea")
        self.assertEqual(image["ad_type_label"], "Single Image Ad")
        self.assertIn("image-shrink_1280", image["image_url"])

    def test_login_wall_detection(self):
        self.assertFalse(L.is_login_wall("https://www.linkedin.com/ad-library/search?accountOwner=Notion", self.html))
        self.assertTrue(L.is_login_wall("https://www.linkedin.com/uas/login?session_redirect=...", ""))
        self.assertTrue(L.is_login_wall("https://www.linkedin.com/authwall?trk=...", ""))


class TestDetailPage(unittest.TestCase):
    def test_detail(self):
        d = L.parse_detail(read("linkedin_detail.html"))
        self.assertEqual(d["creative_type"], "SPONSORED_VIDEO")
        self.assertEqual(d["advertiser"], "Notion")
        self.assertEqual(d["company_id"], "30898036")
        self.assertEqual(d["company_url"], "https://www.linkedin.com/company/30898036")
        self.assertIn("more than 80 agents run across the company", d["body_text"])
        self.assertEqual(d["headline"], "Learn more")
        self.assertEqual(d["cta_text"], "Learn more")
        self.assertIn("videocover-high", d["poster_url"])
        self.assertGreaterEqual(len(d["video_sources"]), 2)
        self.assertTrue(all(s["src"].startswith("https://dms.licdn.com/") for s in d["video_sources"]))
        self.assertEqual(d["ad_type_label"], "Video Ad")
        self.assertEqual(d["paid_for_by"], "Notion Labs, Inc.")
        self.assertIsNone(d["start_date"])
        self.assertIsNone(d["end_date"])
        self.assertIsNone(d["link_url"])

    def test_empty(self):
        d = L.parse_detail("")
        self.assertIsNone(d["advertiser"])
        self.assertEqual(d["video_sources"], [])


class TestNormalize(unittest.TestCase):
    def test_video_record(self):
        card = L.parse_search_cards(read("linkedin_search.html"))[0]
        detail = L.parse_detail(read("linkedin_detail.html"))
        rec = L.normalize(card, detail, ["agents", "zebra"])
        self.assertEqual(rec["source"], "linkedin")
        self.assertEqual(rec["ad_id"], "li-1640238106")
        self.assertEqual(rec["advertiser"], "Notion")
        self.assertEqual(rec["advertiser_id"], "30898036")
        self.assertEqual(rec["advertiser_slug"], "notion")
        self.assertEqual(rec["platforms"], ["linkedin"])
        self.assertEqual(rec["format"], "video")
        self.assertEqual(rec["title"], "Learn more")
        self.assertEqual(rec["cta_text"], "Learn more")
        self.assertEqual(rec["byline"], "Notion Labs, Inc.")
        self.assertIsNone(rec["image_url"])
        self.assertIn("videocover", rec["video_preview_image_url"])
        self.assertTrue(rec["video_hd_url"].startswith("https://dms.licdn.com/"))
        self.assertNotEqual(rec["video_hd_url"], rec["video_sd_url"])
        self.assertIsNone(rec["start_date"])
        self.assertIsNone(rec["days_active"])
        self.assertIsNone(rec["variant_count"])
        self.assertEqual(rec["library_url"], "https://www.linkedin.com/ad-library/detail/1640238106")
        self.assertEqual(rec["term_hits"], ["agents"])
        self.assertEqual(rec["dest_type"], "none")
        self.assertEqual(rec["raw_snapshot"]["card"]["ad_id"], "1640238106")
        for k in L.blank_record():
            self.assertIn(k, rec)

    def test_image_record_from_card_only(self):
        card = L.parse_search_cards(read("linkedin_search.html"))[1]
        rec = L.normalize(card, {}, [])
        self.assertEqual(rec["format"], "image")
        self.assertEqual(rec["advertiser"], "Notion Korea")
        self.assertEqual(rec["advertiser_id"], "")
        self.assertIn("image-shrink_1280", rec["image_url"])
        self.assertIsNone(rec["video_hd_url"])

    def test_format_map(self):
        self.assertEqual(L.map_format("SPONSORED_UPDATE_CAROUSEL", None), "carousel")
        self.assertEqual(L.map_format(None, "Text Ad"), "text")
        self.assertEqual(L.map_format("SPONSORED_UPDATE_NATIVE_DOCUMENT", "Document Ad"), "unknown")
        self.assertEqual(L.map_format("SOMETHING_NEW_VIDEO", None), "video")


class TestDryRun(unittest.TestCase):
    def test_dry_run_prints_urls(self):
        with tempfile.TemporaryDirectory() as td:
            out = subprocess.run([sys.executable, "-I", str(TOOLS / "linkedin_pull.py"), "--advertisers", "Notion",
                                  "--keywords", "project management", "--out", td, "--dry-run"],
                                 capture_output=True, text=True, timeout=60)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("https://www.linkedin.com/ad-library/search?accountOwner=Notion", out.stdout)
        self.assertIn("https://www.linkedin.com/ad-library/search?keyword=project%20management", out.stdout)
        self.assertIn("/ad-library/detail/<id>", out.stdout)
        self.assertNotIn("Traceback", out.stderr)


if __name__ == "__main__":
    unittest.main()
