#!/usr/bin/env python3
"""setup.py: install Ad Lab's Python tooling. Standard library only; runs with any Python 3.9+.

  python3 -I setup.py                       installs the venv, Playwright and Chromium, then runs doctor
  python3 -I setup.py --with-transcription  also installs whisper (mlx-whisper on Apple Silicon, faster-whisper elsewhere)
  python3 -I setup.py --skip-browser        venv and packages only
  python3 -I setup.py --keys                prompt for optional keys (Higgsfield, Apify, SerpApi); values are never echoed
  python3 -I setup.py --home PATH           where to put the venv and config (default: $ADLAB_HOME, $CLAUDE_PLUGIN_DATA, or ~/.adlab)

Everything lands under the home folder: venv/, config.json (keys, chmod 600), setup.log.
Works on macOS, Linux and Windows (venv\\Scripts\\python.exe). Nothing is installed system-wide.
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

PACKAGES = ["playwright>=1.45", "imageio-ffmpeg>=0.5", "pillow>=10", "requests>=2.31", "pyyaml>=6"]
HIGGSFIELD = ["higgsfield-client"]


def run(cmd, log, check=True):
    log.write(" ".join(str(c) for c in cmd) + "\n")
    print("  $", " ".join(str(c) for c in cmd), flush=True)
    r = subprocess.run(cmd, text=True, capture_output=True)
    log.write(r.stdout + r.stderr + "\n")
    if r.returncode != 0:
        tail = (r.stderr or r.stdout).strip().splitlines()[-6:]
        print("    failed (%d): %s" % (r.returncode, " | ".join(tail)))
        if check:
            raise SystemExit("setup stopped; see " + str(log.name))
    return r


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--home")
    ap.add_argument("--with-transcription", action="store_true")
    ap.add_argument("--with-higgsfield", action="store_true", help="install the Higgsfield client (only useful with a key)")
    ap.add_argument("--skip-browser", action="store_true")
    ap.add_argument("--keys", action="store_true", help="prompt for optional API keys")
    ap.add_argument("--no-doctor", action="store_true")
    args = ap.parse_args(argv)
    if args.home:
        os.environ["ADLAB_HOME"] = args.home
    home = C.data_home()
    home.mkdir(parents=True, exist_ok=True)
    log = (home / "setup.log").open("a", encoding="utf-8")
    log.write("\n== setup %s on %s %s python %s\n" % (C.now_iso(), platform.system(), platform.machine(), sys.version.split()[0]))
    if sys.version_info < (3, 9):
        raise SystemExit("Python 3.9 or newer is required; this is %s" % sys.version.split()[0])
    print("Ad Lab setup: home =", home)
    vpy = C.venv_python()
    if not vpy.exists():
        print("creating venv")
        run([sys.executable, "-m", "venv", str(C.venv_dir())], log)
    else:
        print("venv exists:", vpy)
    run([str(vpy), "-m", "pip", "install", "--upgrade", "pip", "--quiet"], log, check=False)
    print("installing packages")
    run([str(vpy), "-m", "pip", "install", "--quiet"] + PACKAGES, log)
    if args.with_higgsfield:
        run([str(vpy), "-m", "pip", "install", "--quiet"] + HIGGSFIELD, log, check=False)
    if args.with_transcription:
        if platform.system() == "Darwin" and platform.machine() == "arm64":
            print("installing mlx-whisper (Apple Silicon)")
            run([str(vpy), "-m", "pip", "install", "--quiet", "mlx-whisper"], log, check=False)
        else:
            print("installing faster-whisper")
            run([str(vpy), "-m", "pip", "install", "--quiet", "faster-whisper"], log, check=False)
    if not args.skip_browser:
        print("installing Chromium for Playwright (one-time download)")
        run([str(vpy), "-m", "playwright", "install", "chromium"], log)
    cfg = C.load_config()
    cfg.setdefault("installed", C.now_iso())
    cfg["python"] = str(vpy)
    if args.keys:
        print("Optional keys. Press Enter to skip any. Nothing you type is shown or printed back.")
        for key, label in [("higgsfield_key_id", "Higgsfield API key id"), ("higgsfield_key_secret", "Higgsfield API key secret"),
                           ("apify_token", "Apify token"), ("serpapi_key", "SerpApi key")]:
            v = getpass.getpass(label + ": ")
            if v.strip():
                cfg[key] = v.strip()
    p = C.save_config(cfg)
    keys_present = [k for k in cfg if k.endswith(("_id", "_secret", "_token", "_key"))]
    print("config written: %s (%s)" % (p, ("keys present: " + ", ".join(keys_present)) if keys_present else "no keys"))
    log.close()
    if not args.no_doctor:
        print("running doctor")
        r = subprocess.run([str(vpy), "-I", str(Path(__file__).resolve().parent / "doctor.py"), "--quick"], text=True)
        return r.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
