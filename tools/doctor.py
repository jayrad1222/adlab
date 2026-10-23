#!/usr/bin/env python3
"""doctor.py: check the Ad Lab install and say what to fix, in plain words.

  python -I doctor.py            full check, including a live load of the Meta Ad Library and Google's transparency center
  python -I doctor.py --quick    skip the live browser checks
  python -I doctor.py --json     machine-readable output
  python -I doctor.py --workspace DIR   also check the member's workspace folders

Exit code 0 when everything needed for Full mode works, 1 when something needs fixing. Lite mode
(paste links or screenshots) needs none of this.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

PROBE_META = "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ALL&media_type=all&search_type=keyword_unordered&q=coffee"
PROBE_GOOGLE = "https://adstransparency.google.com/?region=anywhere"


def check(name, ok, detail, fix=""):
    return {"check": name, "ok": bool(ok), "detail": detail, "fix": fix}


def venv_run(code: str, timeout=120):
    vpy = C.venv_python()
    try:
        r = subprocess.run([str(vpy), "-I", "-c", code], capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e:
        return 1, str(e)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--workspace")
    args = ap.parse_args(argv)
    results = []
    results.append(check("python", sys.version_info >= (3, 9), "running %s" % sys.version.split()[0],
                         "install Python 3.9 or newer from python.org"))
    vpy = C.venv_python()
    results.append(check("venv", vpy.exists(), str(vpy), "run /adlab:setup"))
    if vpy.exists():
        rc, out = venv_run("import playwright, imageio_ffmpeg; print('ok')")
        results.append(check("packages", rc == 0 and "ok" in out, out[-200:], "run /adlab:setup again; see setup.log in " + str(C.data_home())))
        rc, out = venv_run("import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
        results.append(check("ffmpeg", rc == 0, out[-200:], "pip install imageio-ffmpeg inside the venv"))
        rc, out = venv_run("from playwright.sync_api import sync_playwright\nwith sync_playwright() as p:\n    b = p.chromium.launch(); b.close(); print('ok')", timeout=90)
        results.append(check("chromium", rc == 0 and "ok" in out, out[-200:], "run: " + str(vpy) + " -m playwright install chromium"))
        rc, out = venv_run("import mlx_whisper; print('mlx-whisper')")
        if rc != 0:
            rc, out = venv_run("import faster_whisper; print('faster-whisper')")
        results.append(check("transcription", rc == 0, out[-80:] if rc == 0 else "not installed (optional)", "optional: /adlab:setup --with-transcription"))
        if not args.quick:
            code = (
                "import time\nfrom playwright.sync_api import sync_playwright\n"
                "with sync_playwright() as p:\n"
                "    b = p.chromium.launch(); ctx = b.new_context(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', viewport={'width':1440,'height':1000})\n"
                "    pg = ctx.new_page(); pg.goto(%r, wait_until='domcontentloaded', timeout=60000); time.sleep(5)\n"
                "    html = pg.content(); n = html.count('ad_archive_id'); print('meta', n, pg.url[:60])\n"
                "    pg.goto(%r, wait_until='domcontentloaded', timeout=60000); time.sleep(4); print('google', len(pg.content()), pg.url[:60])\n"
                "    b.close()\n" % (PROBE_META, PROBE_GOOGLE))
            rc, out = venv_run(code, timeout=180)
            meta_ok = rc == 0 and "meta" in out and not any(w in out for w in ("login", "checkpoint"))
            try:
                n = int([l for l in out.splitlines() if l.startswith("meta")][0].split()[1])
            except Exception:
                n = 0
            results.append(check("meta ad library loads", meta_ok and n > 0, out[-200:],
                                 "check your network; if Meta shows a login or checkpoint page, wait and retry later, or use --mode manual"))
            results.append(check("google transparency loads", rc == 0 and "google" in out, out[-120:], "check your network"))
    free_gb = shutil.disk_usage(str(Path.home())).free / 1e9
    results.append(check("disk space", free_gb > 2, "%.1f GB free" % free_gb, "free up disk space; a full pull with videos can take a few GB"))
    cfg = C.load_config()
    keys = [k for k in ("higgsfield_key_id", "apify_token", "serpapi_key") if cfg.get(k)]
    results.append(check("optional keys", True, ", ".join(keys) if keys else "none (free paths only)", ""))
    if args.workspace or os.environ.get("ADLAB_WORKSPACE"):
        ws = C.workspace(args.workspace)
        missing = [d for d in C.WORKSPACE_DIRS if not (ws / d).exists()]
        results.append(check("workspace", not missing, str(ws) + ("" if not missing else " missing " + ", ".join(missing)), "run /adlab:start"))
    needed = [r for r in results if r["check"] not in ("transcription", "optional keys")]
    ok = all(r["ok"] for r in needed)
    if args.json:
        print(json.dumps({"ok": ok, "results": results}, indent=1))
    else:
        optional = ("transcription", "optional keys")
        for r in results:
            tag = "ok " if r["ok"] else ("opt" if r["check"] in optional else "FIX")
            print("%s %-28s %s" % (tag, r["check"], r["detail"]))
            if not r["ok"] and r["fix"]:
                print("    -> " + r["fix"])
        print("\nFull mode: %s. Lite mode works regardless." % ("ready" if ok else "not ready"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
