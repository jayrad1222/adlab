#!/usr/bin/env python3
"""render.py: HTML templates to ad images and simple videos with Python Playwright (no node).

Port of the Operators Workshop pw.py renderer plus a template filler.

  python -I render.py still --template templates/problem-card.html --data fields.json --brand brand.json \
      --out <workspace>/bank/renders/c01 [--sizes 1x1,4x5,9x16] [--name c01-h1]
  python -I render.py video --html motion.html --out clip.mp4 [--fps 30]        (html defines window.DUR and window.render(t))
  python -I render.py check --html rendered.html [--phone-width 390]              (text sizes at phone scale, clipped or overflowing text, the 9:16 overlay zones)
  python -I render.py demo --out DIR                                              (renders every template with sample data)

Templates: plain HTML with {{field}} placeholders, a `.art` root, and CSS variables set by --brand:
  --brand-primary --brand-accent --brand-bg --brand-text --font-head --font-body plus --w and --h for the size.
Elements with data-optional="field" are removed when that field is empty. Image fields take a file path.
Sizes: 1x1 = 1080x1080, 4x5 = 1080x1350, 9x16 = 1080x1920.
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

SIZES = {"1x1": (1080, 1080), "4x5": (1080, 1350), "9x16": (1080, 1920)}
DEFAULT_BRAND = {"primary": "#17321f", "accent": "#b7e4c7", "bg": "#ffffff", "text": "#111111",
                 "font_head": "Inter Tight, Inter, Helvetica Neue, Arial, sans-serif",
                 "font_body": "Inter, Helvetica Neue, Arial, sans-serif", "wordmark": ""}

TEXT_JS = r"""() => {
  const runs = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (w.nextNode()) { const n = w.currentNode, t = n.textContent.trim(); if (!t) continue;
    const el = n.parentElement; if (el.closest('script,style')) continue;
    const r = el.getBoundingClientRect();
    runs.push({ t: t.slice(0, 80), fs: parseFloat(getComputedStyle(el).fontSize), x: r.left, y: r.top, w: r.width, h: r.height }); }
  const art = document.querySelector('.art'); const a = art ? art.getBoundingClientRect() : {width: innerWidth, height: innerHeight};
  return { runs, canvas: [Math.round(a.width), Math.round(a.height)] };
}"""


def ffmpeg_bin():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def data_uri(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    mt = mimetypes.guess_type(str(p))[0] or "image/jpeg"
    return "data:%s;base64,%s" % (mt, base64.b64encode(p.read_bytes()).decode())


def inline_css(template_html: str, template_dir: Path) -> str:
    """Replace <link rel="stylesheet" href="x.css"> with the file's contents so the filled HTML can live anywhere."""
    def repl(m):
        href = m.group(1)
        p = template_dir / href
        if p.exists():
            return "<style>\n%s\n</style>" % p.read_text(encoding="utf-8")
        return m.group(0)
    return re.sub(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"[^>]*>', repl, template_html)


def fill(template_html: str, data: dict, brand: dict, size: str) -> str:
    w, h = SIZES[size]
    b = dict(DEFAULT_BRAND)
    b.update({k: v for k, v in (brand or {}).items() if v})
    css = (":root{--w:%dpx;--h:%dpx;--brand-primary:%s;--brand-accent:%s;--brand-bg:%s;--brand-text:%s;"
           "--font-head:%s;--font-body:%s;}" % (w, h, b["primary"], b["accent"], b["bg"], b["text"], b["font_head"], b["font_body"]))
    html = template_html
    # remove optional blocks whose field is empty
    html = re.sub(r'<([a-z0-9]+)[^>]*data-optional="([^"]+)"[^>]*>.*?</\1>', lambda m: "" if not data.get(m.group(2)) else m.group(0), html, flags=re.S)
    merged = dict(data)
    merged.setdefault("wordmark", b.get("wordmark", ""))
    for k, v in list(merged.items()):
        if isinstance(v, str) and k.endswith("image") and v and os.path.exists(v):
            merged[k] = data_uri(v)
    def sub(m):
        key = m.group(1).strip()
        v = merged.get(key, "")
        return str(v) if v is not None else ""
    html = re.sub(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", sub, html)
    html = html.replace("</head>", "<style>%s</style></head>" % css, 1) if "</head>" in html else "<style>%s</style>" % css + html
    html = html.replace("<html", '<html data-size="%s"' % size, 1)
    return html


def browser():
    C.need_playwright()
    from playwright.sync_api import sync_playwright
    pw = sync_playwright().start()
    return pw, pw.chromium.launch()


def goto_html(page, html_path: Path, settle=250):
    page.goto("file://" + str(html_path.resolve()))
    try:
        page.evaluate("() => document.fonts.ready")
    except Exception:
        pass
    page.wait_for_timeout(settle)


def cmd_still(args):
    tpl = inline_css(Path(args.template).read_text(encoding="utf-8"), Path(args.template).resolve().parent)
    data = json.loads(Path(args.data).read_text(encoding="utf-8")) if args.data else {}
    stem = Path(args.template).stem
    if isinstance(data, dict) and stem in data and isinstance(data[stem], dict):
        data = data[stem]
    elif isinstance(data, dict) and "_default" in data and all(isinstance(v, dict) for v in data.values()):
        data = data["_default"]
    brand = json.loads(Path(args.brand).read_text(encoding="utf-8")) if args.brand and Path(args.brand).exists() else {}
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    name = args.name or Path(args.template).stem
    sizes = [s.strip() for s in args.sizes.split(",") if s.strip() in SIZES]
    pw, b = browser()
    results = []
    for size in sizes:
        w, h = SIZES[size]
        html = fill(tpl, data, brand, size)
        hp = out / ("%s-%s.html" % (name, size))
        hp.write_text(html, encoding="utf-8")
        page = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        goto_html(page, hp)
        png = out / ("%s-%s.png" % (name, size))
        try:
            r = page.evaluate("() => { const e = document.querySelector('.art').getBoundingClientRect(); return {x: e.left, y: e.top, width: e.width, height: e.height}; }")
            page.screenshot(path=str(png), clip=r)
        except Exception:
            page.screenshot(path=str(png))
        stats = page.evaluate(TEXT_JS)
        page.close()
        rep = legibility(stats, args.phone_width)
        rep.update({"size": size, "png": str(png), "html": str(hp)})
        results.append(rep)
        print("rendered %s %s (%dx%d) min text at phone %.1fpx%s" % (name, size, w, h, rep["min_phone_px"], "" if rep["ok"] else "  WARNING: " + "; ".join(rep["warnings"])))
    b.close()
    pw.stop()
    (out / ("%s-report.json" % name)).write_text(json.dumps(results, indent=1), encoding="utf-8")
    return 0


def legibility(stats: dict, phone_width: int) -> dict:
    cw = stats["canvas"][0] or 1080
    scale = phone_width / float(cw)
    runs = stats["runs"]
    mins = [r["fs"] * scale for r in runs] or [0]
    warnings = []
    small = [r for r in runs if r["fs"] * scale < 11]
    if small:
        warnings.append("%d text runs under 11px at phone width (e.g. %r)" % (len(small), small[0]["t"][:40]))
    ch = stats["canvas"][1] if len(stats["canvas"]) > 1 and stats["canvas"][1] else 0
    clipped = [r for r in runs if r["x"] < -2 or r["y"] < -2 or r["x"] + r["w"] > cw + 2 or (ch and r["y"] + r["h"] > ch + 2)]
    if clipped:
        warnings.append("%d text runs clipped at the edge" % len(clipped))
    if ch and ch / float(cw) > 1.7:
        # 9:16: the platform draws its own controls over the top, the bottom and the right edge
        # (library/platform/specs-and-safe-zones.md). Meta's bottom overlay is the floor; TikTok's is taller.
        top, bottom, right = 250 * ch / 1920.0, ch - 400 * ch / 1920.0, cw - 120 * cw / 1080.0
        covered = [r for r in runs if r["y"] < top or r["y"] + r["h"] > bottom or r["x"] + r["w"] > right]
        if covered:
            warnings.append("%d text runs inside the 9:16 platform overlay (e.g. %r)" % (len(covered), covered[0]["t"][:40]))
    return {"min_phone_px": min(mins), "text_runs": len(runs), "warnings": warnings, "ok": not warnings}


def cmd_video(args):
    pw, b = browser()
    page = b.new_page(viewport={"width": 1080, "height": 1920})
    goto_html(page, Path(args.html), 300)
    dur = page.evaluate("() => window.DUR")
    fps = int(args.fps)
    n = int(round(dur * fps))
    ff = subprocess.Popen([ffmpeg_bin(), "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-i", "-",
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium", "-movflags", "+faststart", args.out], stdin=subprocess.PIPE)
    for i in range(n):
        page.evaluate("t => window.render(t)", i / fps)
        ff.stdin.write(page.screenshot(type="jpeg", quality=92))
    ff.stdin.close()
    ff.wait()
    b.close()
    pw.stop()
    print("wrote", args.out, n, "frames")
    return 0


def cmd_check(args):
    pw, b = browser()
    page = b.new_page(viewport={"width": 1080, "height": 1920})
    goto_html(page, Path(args.html), 100)
    stats = page.evaluate(TEXT_JS)
    b.close()
    pw.stop()
    rep = legibility(stats, args.phone_width)
    print(json.dumps(rep, indent=1))
    return 0 if rep["ok"] else 1


def cmd_demo(args):
    tdir = C.plugin_root() / "templates"
    sample = json.loads((tdir / "sample-data.json").read_text(encoding="utf-8")) if (tdir / "sample-data.json").exists() else {}
    out = Path(args.out)
    for t in sorted(tdir.glob("*.html")):
        if t.name.startswith("_"):
            continue
        ns = argparse.Namespace(template=str(t), data=None, brand=None, out=str(out), name=t.stem, sizes="1x1,4x5,9x16", phone_width=390)
        data = sample.get(t.stem, sample.get("_default", {}))
        dp = out / (t.stem + "-data.json")
        out.mkdir(parents=True, exist_ok=True)
        dp.write_text(json.dumps(data), encoding="utf-8")
        ns.data = str(dp)
        cmd_still(ns)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("still")
    s.add_argument("--template", required=True)
    s.add_argument("--data")
    s.add_argument("--brand")
    s.add_argument("--out", required=True)
    s.add_argument("--name")
    s.add_argument("--sizes", default="1x1,4x5,9x16")
    s.add_argument("--phone-width", type=int, default=390)
    v = sub.add_parser("video")
    v.add_argument("--html", required=True)
    v.add_argument("--out", required=True)
    v.add_argument("--fps", default=30)
    c = sub.add_parser("check")
    c.add_argument("--html", required=True)
    c.add_argument("--phone-width", type=int, default=390)
    d = sub.add_parser("demo")
    d.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    return {"still": cmd_still, "video": cmd_video, "check": cmd_check, "demo": cmd_demo}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
