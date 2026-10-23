#!/usr/bin/env python3
"""admd.py: write ad.md for every pulled ad from ad.json, media.json, transcript.md and landing/meta.json.

  python -I admd.py --workspace DIR            (every ad without an ad.md, or with --force all of them)
  python -I admd.py --ad-dir <ads>/<adv>/<id>

ad.md is the analyst's reading sheet: copy fields, dates, variant count, link and landing summary,
the frame files to look at, the transcript (or the note that there is none), and a coverage line the
analyst must keep honest. It never interprets; the rubric row does that.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402


def write_one(d: Path, force=False) -> bool:
    out = d / "ad.md"
    if out.exists() and not force:
        return False
    try:
        a = json.loads((d / "ad.json").read_text(encoding="utf-8"))
    except Exception:
        return False
    files = a.get("files") or {}
    lines = ["# %s · %s" % (a.get("advertiser"), a.get("ad_id")), "",
             "Source: %s · match: %s · library: %s" % (a.get("source"), a.get("match", ""), a.get("library_url") or ""), "",
             "## Facts (observed from the library)", "",
             "- Start date: %s · active: %s · days active at capture: %s" % (a.get("start_date"), a.get("is_active"), a.get("days_active")),
             "- Variant count (Meta collation): %s · format: %s · platforms: %s" % (a.get("variant_count"), a.get("format"), ", ".join(a.get("platforms") or [])),
             "- CTA: %s (%s) · link: %s · destination type: %s" % (a.get("cta_text"), a.get("cta_type"), a.get("link_url"), a.get("dest_type")),
             "- Page likes: %s · categories: %s" % (a.get("page_like_count"), a.get("page_categories")),
             ""]
    if a.get("eu"):
        lines += ["EU transparency block present (reach and audience breakdown): see ad.json `eu`.", ""]
    lines += ["## Copy", "", "**Title:** %s" % (a.get("title") or ""), "", "**Primary text:**", "", (a.get("body_text") or "(none)"), "",
              "**Link description:** %s · **Caption:** %s" % (a.get("link_description") or "", a.get("caption") or ""), ""]
    cards = a.get("cards") or []
    if len(cards) > 1:
        lines += ["## Carousel cards", ""]
        for i, c in enumerate(cards[:10]):
            lines.append("- Card %d: %s | %s | CTA %s" % (i + 1, (c.get("title") or "").strip(), (c.get("body") or "").strip()[:160], c.get("cta_text") or ""))
        lines.append("")
    lines += ["## Media to look at", ""]
    for k in ("card", "creative", "poster"):
        if files.get(k):
            lines.append("- %s: `%s`" % (k, files[k]))
    mj = d / "media.json"
    if mj.exists():
        try:
            m = json.loads(mj.read_text(encoding="utf-8"))
            lines.append("- video: %.1fs; frames every %ss: %d files under `frames/`; scene changes: %d; contact sheet: `frames/contact.jpg`" % (m.get("duration_s") or 0, m.get("every_s"), len(m.get("frames", [])), len(m.get("scene_frames", []))))
        except Exception:
            pass
    elif a.get("video_hd_url") or a.get("video_sd_url"):
        lines.append("- video: present in the library but not downloaded or not yet processed (see files.video)")
    lines.append("")
    tp = d / "transcript.md"
    if tp.exists():
        t = tp.read_text(encoding="utf-8")
        if "No transcription backend" in t:
            lines += ["## Transcript", "", "None available (no transcription backend installed). Read the frames and the on-screen text.", ""]
        else:
            lines += ["## Transcript", ""] + t.splitlines()[4:] + [""]
    lp = d / "landing" / "meta.json"
    if lp.exists():
        try:
            m = json.loads(lp.read_text(encoding="utf-8"))
            lines += ["## Landing page (captured %s)" % m.get("captured", "")[:10], "",
                      "- Title: %s · h1: %s" % (m.get("title"), " | ".join(m.get("h1") or [])),
                      "- Prices seen: %s" % ", ".join(m.get("prices") or []),
                      "- Buttons: %s" % ", ".join((m.get("buttons") or [])[:10]),
                      "- Forms: %s · words: %s · note: %s" % (m.get("forms"), m.get("word_count"), m.get("note") or ""), ""]
            txt = d / "landing" / "page.txt"
            if txt.exists():
                first = " ".join(txt.read_text(encoding="utf-8").split())[:600]
                lines += ["First 600 characters: " + first, ""]
        except Exception:
            pass
    has_frames = (d / "frames" / "contact.jpg").exists()
    has_t = tp.exists() and "No transcription backend" not in (tp.read_text(encoding="utf-8") if tp.exists() else "")
    cov = "video-watched possible" if (has_frames and has_t) else "still-reviewed possible (frames: %s, transcript: %s)" % (has_frames, has_t) if (files.get("card") or files.get("creative") or has_frames) else "copy-only"
    lines += ["## Coverage", "", "Best honest coverage for this ad: %s. The analyst sets `inspection_coverage` to what they actually read." % cov, ""]
    out.write_text("\n".join(lines), encoding="utf-8")
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace")
    ap.add_argument("--ad-dir")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)
    if args.ad_dir:
        print("written" if write_one(Path(args.ad_dir), True) else "skipped")
        return 0
    ws = C.workspace(args.workspace)
    n = 0
    for aj in (ws / "ads").glob("*/*/ad.json"):
        if write_one(aj.parent, args.force):
            n += 1
    print("ad.md written for %d ads" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
