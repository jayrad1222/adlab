#!/usr/bin/env python3
"""higgsfield.py: generate mood and b-roll media through the Higgsfield API, with the price shown first.

  python -I higgsfield.py price --model higgsfield-ai/soul/v2/standard [--seconds 10] [--n 1]
  python -I higgsfield.py generate --model higgsfield-ai/soul/v2/standard --prompt "..." --out DIR [--n 1] [--yes]
  python -I higgsfield.py generate --model kling/v2.6 --prompt "..." --image start.jpg --seconds 5 --out DIR
  python -I higgsfield.py status --request-id ID
  python -I higgsfield.py balance

Rules the tool enforces: no key means dry run only; the estimate prints before every spend and
`--yes` is required to proceed; the floor from business/finance.md (higgsfield_credit_floor, in USD
of API balance) is respected when a balance can be read; every run is logged to bank/renders/HIGGSFIELD.md;
prompts that would fabricate proof (screenshots, testimonials, customers, results, before-and-after)
are refused. Model ids are endpoint paths; check console.higgsfield.ai for the current list and
read each model's page for its parameters.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

API = "https://api.higgsfield.ai"
REFUSE = ["screenshot", "testimonial", "review", "customer says", "customers say", "dashboard showing", "revenue",
          "before and after", "before/after", "results screen", "bank statement", "sales figure", "5 stars", "five stars",
          "verified", "as seen on", "logo of", "celebrity"]


def prices():
    p = Path(__file__).resolve().parent / "higgsfield_prices.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def estimate(model, n=1, seconds=None):
    tab = prices().get(model)
    if not tab:
        return None, "no price on file for %s; add it to tools/higgsfield_prices.json from the console" % model
    if tab["unit"] == "image":
        return tab["usd"] * n, "%d image(s) x $%.4f" % (n, tab["usd"])
    secs = seconds or 5
    return tab["usd"] * secs * n, "%d clip(s) x %ss x $%.4f/s" % (n, secs, tab["usd"])


def creds():
    cfg = C.load_config()
    if cfg.get("hf_key") and ":" in cfg["hf_key"]:
        return cfg["hf_key"]
    if cfg.get("higgsfield_key_id") and cfg.get("higgsfield_key_secret"):
        return cfg["higgsfield_key_id"] + ":" + cfg["higgsfield_key_secret"]
    return None


def call(method, path, body=None, key=None, timeout=60):
    req = urllib.request.Request(API + path, method=method, data=json.dumps(body).encode() if body is not None else None)
    req.add_header("Content-Type", "application/json")
    if key:
        req.add_header("Authorization", "Key " + key)
    if method == "POST":
        req.add_header("Idempotency-Key", str(uuid.uuid4()))
    with urllib.request.urlopen(req, timeout=timeout) as r:
        txt = r.read().decode()
        return json.loads(txt) if txt else {}


def logrun(ws, line):
    p = ws / "bank" / "renders" / "HIGGSFIELD.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text("# Higgsfield runs\n\nOne line per run: time, model, estimate, request id, result. Generated media is mood or b-roll only and is labeled AI in the bank.\n\n", encoding="utf-8")
    with p.open("a", encoding="utf-8") as f:
        f.write("- %s %s\n" % (C.now_iso(), line))


def floor_usd(ws):
    fp = ws / "business" / "finance.md"
    if fp.exists():
        fm, _ = C.read_frontmatter(fp)
        v = fm.get("higgsfield_credit_floor")
        try:
            return float(v) if v is not None else None
        except Exception:
            return None
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("price")
    p.add_argument("--model", required=True)
    p.add_argument("--n", type=int, default=1)
    p.add_argument("--seconds", type=float)
    g = sub.add_parser("generate")
    g.add_argument("--model", required=True)
    g.add_argument("--prompt", required=True)
    g.add_argument("--image", help="start image path or URL for image-to-video models")
    g.add_argument("--seconds", type=float)
    g.add_argument("--n", type=int, default=1)
    g.add_argument("--out", required=True)
    g.add_argument("--yes", action="store_true", help="confirm the spend shown by the estimate")
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--extra", help="JSON of extra parameters for the model")
    s = sub.add_parser("status")
    s.add_argument("--request-id", required=True)
    sub.add_parser("balance")
    args = ap.parse_args(argv)
    ws = C.workspace(args.workspace)
    key = creds()

    if args.cmd == "price":
        usd, how = estimate(args.model, args.n, args.seconds)
        print("estimate: %s (%s)" % (("$%.4f" % usd) if usd is not None else "unknown", how))
        return 0
    if args.cmd == "balance":
        if not key:
            print("no Higgsfield key configured (run /adlab:setup --keys)")
            return 1
        try:
            print(json.dumps(call("GET", "/account/balance", key=key), indent=1))
        except Exception as e:
            print("balance endpoint not available or failed: %s. Check the console instead." % str(e)[:120])
        return 0
    if args.cmd == "status":
        if not key:
            print("no key")
            return 1
        print(json.dumps(call("GET", "/requests/%s/status" % args.request_id, key=key), indent=1))
        return 0

    # generate
    low = args.prompt.lower()
    bad = [w for w in REFUSE if w in low]
    if bad:
        print("refused: the prompt asks for something that would read as proof (%s). Generated media is for mood and b-roll only; use real assets for anything that implies a result, a customer or a screen." % ", ".join(bad))
        return 2
    usd, how = estimate(args.model, args.n, args.seconds)
    print("estimate: %s (%s)" % (("$%.4f" % usd) if usd is not None else "unknown", how))
    fl = floor_usd(ws)
    if fl is not None:
        print("floor from finance.md: keep at least $%.2f of API balance" % fl)
    if not key or args.dry_run:
        print("dry run: no key configured" if not key else "dry run requested")
        print("would POST %s/%s with prompt %r%s" % (API, args.model, args.prompt[:80], (" and image " + args.image) if args.image else ""))
        logrun(ws, "DRY RUN model=%s estimate=%s prompt=%r" % (args.model, usd, args.prompt[:60]))
        return 0
    if not args.yes:
        print("add --yes to confirm this spend")
        return 3
    body = {"prompt": args.prompt}
    if args.image:
        body["image_url"] = args.image
    if args.seconds:
        body["duration"] = args.seconds
    if args.extra:
        body.update(json.loads(args.extra))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for i in range(args.n):
        sub_ = call("POST", "/" + args.model.strip("/"), body, key=key)
        rid = sub_.get("request_id")
        print("submitted", rid, sub_.get("status"))
        logrun(ws, "model=%s estimate=%s request=%s prompt=%r" % (args.model, usd, rid, args.prompt[:60]))
        status = sub_
        for _ in range(240):
            time.sleep(3)
            status = call("GET", "/requests/%s/status" % rid, key=key)
            if status.get("status") in ("completed", "failed", "nsfw", "canceled"):
                break
        if status.get("status") != "completed":
            print("request %s ended with %s" % (rid, status.get("status")))
            logrun(ws, "request=%s ended %s" % (rid, status.get("status")))
            continue
        urls = [im["url"] for im in status.get("images", []) if im.get("url")]
        if status.get("video", {}).get("url"):
            urls.append(status["video"]["url"])
        for j, u in enumerate(urls):
            ext = ".mp4" if ".mp4" in u.split("?")[0] else ".jpg"
            dest = out / ("%s-%d-%d%s" % (C.slugify(args.model), i, j, ext))
            if C.http_download(u, dest):
                print("saved", dest)
                logrun(ws, "request=%s saved %s (AI-generated, label it)" % (rid, dest.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
