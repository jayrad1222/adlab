#!/usr/bin/env python3
"""progress.py: keep PROGRESS.md and changelog.md in the member's workspace.

Every skill calls this so a member can stop and resume across sessions.

  python -I progress.py --workspace DIR set --step pull --status done --note "8 advertisers, 212 ads" --count 212
  python -I progress.py --workspace DIR note "Pulled Meta ads for the roster"      (appends to changelog.md)
  python -I progress.py --workspace DIR show                                       (prints the table)
  python -I progress.py --workspace DIR init                                       (creates the workspace folders)

Statuses: pending, running, done, blocked, skipped.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

STEPS = ["setup", "intake", "competitors", "pull", "process", "analyze", "personas", "interrogate",
         "angles", "bank", "assets", "render", "plan", "readout", "refresh"]


def load(ws: Path) -> dict:
    p = ws / "progress.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"steps": {s: {"status": "pending", "updated": None, "note": "", "count": None} for s in STEPS}}


def save(ws: Path, data: dict) -> None:
    (ws / "progress.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
    render(ws, data)


def render(ws: Path, data: dict) -> None:
    lines = ["# Progress", "", "Updated " + C.now_iso() + ". Resume from the first step that is not done.", "",
             "| Step | Status | Updated | Count | Note |", "|---|---|---|---:|---|"]
    for s in STEPS:
        d = data["steps"].get(s, {})
        lines.append("| %s | %s | %s | %s | %s |" % (s, d.get("status", "pending"), d.get("updated") or "",
                                                   d.get("count") if d.get("count") is not None else "", d.get("note") or ""))
    lines += ["", "Statuses: pending, running, done, blocked, skipped. Counts are what was written, not a quality claim."]
    (ws / "PROGRESS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def note(ws: Path, text: str) -> None:
    p = ws / "changelog.md"
    if not p.exists():
        p.write_text("# Changelog\n\nOne line per event, newest last.\n\n", encoding="utf-8")
    with p.open("a", encoding="utf-8") as f:
        f.write("- %s: %s\n" % (C.now_iso(), text))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace", help="workspace folder (default: ./adlab-workspace)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("set")
    s.add_argument("--step", required=True, choices=STEPS)
    s.add_argument("--status", required=True, choices=["pending", "running", "done", "blocked", "skipped"])
    s.add_argument("--note", default="")
    s.add_argument("--count", type=int)
    n = sub.add_parser("note")
    n.add_argument("text")
    sub.add_parser("show")
    sub.add_parser("init")
    args = ap.parse_args(argv)
    ws = C.workspace(args.workspace)
    if args.cmd == "init":
        C.ensure_workspace(ws)
        data = load(ws)
        save(ws, data)
        note(ws, "workspace initialized at " + str(ws))
        print("workspace ready:", ws)
        return 0
    if not ws.exists():
        C.die("workspace not found: %s (run /adlab:start first)" % ws)
    data = load(ws)
    if args.cmd == "set":
        d = data["steps"].setdefault(args.step, {})
        d.update({"status": args.status, "updated": C.now_iso(), "note": args.note})
        if args.count is not None:
            d["count"] = args.count
        save(ws, data)
        note(ws, "%s -> %s%s" % (args.step, args.status, (" (" + args.note + ")") if args.note else ""))
        print("%s: %s" % (args.step, args.status))
    elif args.cmd == "note":
        note(ws, args.text)
        print("noted")
    elif args.cmd == "show":
        render(ws, data)
        print((ws / "PROGRESS.md").read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
