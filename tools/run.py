#!/usr/bin/env python3
"""run.py: launch an Ad Lab tool with the venv interpreter, whatever the OS.

  python3 -I run.py meta_pull --advertisers "Brand" --out adlab-workspace/ads
  python3 -I run.py doctor --quick
  python3 -I run.py which            prints the interpreter it would use

Looks for the venv in $ADLAB_HOME, then $CLAUDE_PLUGIN_DATA, then ~/.adlab. Falls back to the current
interpreter (standard-library tools such as finance, progress, export and readout still work there).
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import adlab_common as C  # noqa: E402

NEEDS_VENV = {"meta_pull", "google_pull", "linkedin_pull", "tiktok_ccl_pull", "landing", "render", "media", "transcribe", "doctor"}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    tool = sys.argv[1].replace(".py", "")
    vpy = C.venv_python()
    interp = str(vpy) if vpy.exists() else sys.executable
    if tool == "which":
        print(interp)
        return 0
    script = HERE / (tool + ".py")
    if not script.exists():
        print("no such tool:", tool, "\navailable:", ", ".join(sorted(p.stem for p in HERE.glob("*.py") if p.stem not in ("run", "adlab_common"))))
        return 2
    if tool in NEEDS_VENV and not vpy.exists() and tool != "doctor":
        print("warning: no venv found at %s; run /adlab:setup. Trying the current interpreter." % vpy, file=sys.stderr)
    env = dict(os.environ)
    env.setdefault("ADLAB_WORKSPACE", str(C.workspace()))
    r = subprocess.run([interp, "-I", str(script)] + sys.argv[2:], env=env)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
