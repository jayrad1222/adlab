#!/usr/bin/env python3
"""Shared helpers for Ad Lab tools. Standard library only, Python 3.9+.

Paths
  plugin_root()   the plugin folder (CLAUDE_PLUGIN_ROOT or two levels up from this file)
  data_home()     where the venv, browsers and config live (ADLAB_HOME, else CLAUDE_PLUGIN_DATA, else ~/.adlab)
  venv_python()   the venv interpreter inside data_home()
  workspace(p)    the member's workspace (argument, else ADLAB_WORKSPACE, else <project>/adlab-workspace)

Files
  read_jsonl / write_jsonl / append_jsonl, write_csv, read_frontmatter
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import unicodedata
import urllib.request
from datetime import datetime, timezone, date
from pathlib import Path

WORKSPACE_DIRS = ["business", "competitors", "ads", "analysis", "personas", "concepts",
                  "bank", "bank/briefs", "bank/renders", "assets", "plan", "plan/readouts"]


def plugin_root() -> Path:
    env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    return Path(env) if env else Path(__file__).resolve().parent.parent


def data_home() -> Path:
    for key in ("ADLAB_HOME", "CLAUDE_PLUGIN_DATA"):
        v = os.environ.get(key)
        if v:
            return Path(v).expanduser()
    return Path.home() / ".adlab"


def venv_dir() -> Path:
    return data_home() / "venv"


def venv_python() -> Path:
    if os.name == "nt":
        return venv_dir() / "Scripts" / "python.exe"
    return venv_dir() / "bin" / "python"


def workspace(arg: "str | None" = None) -> Path:
    if arg:
        return Path(arg).expanduser().resolve()
    env = os.environ.get("ADLAB_WORKSPACE")
    if env:
        return Path(env).expanduser().resolve()
    proj = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    return Path(proj).resolve() / "adlab-workspace"


def ensure_workspace(ws: Path) -> Path:
    for d in WORKSPACE_DIRS:
        (ws / d).mkdir(parents=True, exist_ok=True)
    return ws


def load_config() -> dict:
    cfg = {}
    p = data_home() / "config.json"
    if p.exists():
        try:
            cfg = json.loads(p.read_text())
        except Exception:
            cfg = {}
    env_map = {
        "HIGGSFIELD_KEY_ID": "higgsfield_key_id",
        "HIGGSFIELD_KEY_SECRET": "higgsfield_key_secret",
        "HF_KEY": "hf_key",
        "APIFY_TOKEN": "apify_token",
        "SERPAPI_KEY": "serpapi_key",
    }
    for env, key in env_map.items():
        if os.environ.get(env):
            cfg[key] = os.environ[env]
    return cfg


def save_config(cfg: dict) -> Path:
    data_home().mkdir(parents=True, exist_ok=True)
    p = data_home() / "config.json"
    p.write_text(json.dumps(cfg, indent=2))
    try:
        os.chmod(p, 0o600)
    except Exception:
        pass
    return p


def slugify(s: str, maxlen: int = 60) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return (s or "unnamed")[:maxlen].rstrip("-")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def today() -> str:
    return date.today().isoformat()


def days_between(start: "str | None", end: "str | None" = None) -> "int | None":
    if not start:
        return None
    try:
        s = date.fromisoformat(start[:10])
        e = date.fromisoformat(end[:10]) if end else date.today()
        return max(0, (e - s).days)
    except Exception:
        return None


def read_jsonl(p: Path) -> list:
    p = Path(p)
    if not p.exists():
        return []
    out = []
    with p.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    return out


def write_jsonl(p: Path, rows) -> None:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, p)


def append_jsonl(p: Path, row: dict) -> None:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_csv(p: Path, rows, cols) -> None:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(cols), extrasaction="ignore")
        w.writeheader()
        for r in rows:
            row = {}
            for c in cols:
                v = r.get(c)
                if isinstance(v, (list, dict)):
                    v = json.dumps(v, ensure_ascii=False)
                row[c] = v
            w.writerow(row)


def read_frontmatter(p: Path) -> "tuple[dict, str]":
    """Tiny YAML-ish frontmatter reader: `key: value` lines between --- markers.
    Values: numbers, true/false, quoted strings, plain strings, [a, b] lists."""
    text = Path(p).read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return {}, text
    head = parts[0][3:]
    body = parts[1].lstrip("\n")
    data = {}
    for line in head.splitlines():
        if not line.strip() or line.strip().startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = _coerce(_strip_comment(v.strip()))
    return data, body


def _strip_comment(v: str) -> str:
    """Drop a trailing ` # comment` unless the hash sits inside quotes."""
    if v.startswith(('"', "'")):
        q = v[0]
        end = v.find(q, 1)
        return v[: end + 1] if end > 0 else v
    i = v.find(" #")
    if v.startswith("#"):
        return ""
    return v[:i].rstrip() if i >= 0 else v


def _coerce(v: str):
    if v == "":
        return None
    if v.lower() in ("true", "yes"):
        return True
    if v.lower() in ("false", "no"):
        return False
    if v.lower() in ("null", "none", "~"):
        return None
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    if v.startswith("[") and v.endswith("]"):
        return [_coerce(x.strip()) for x in v[1:-1].split(",") if x.strip()]
    try:
        if re.fullmatch(r"-?\d+", v):
            return int(v)
        if re.fullmatch(r"-?\d*\.\d+", v):
            return float(v)
    except Exception:
        pass
    return v


def log(msg: str, logfile: "Path | None" = None) -> None:
    line = datetime.now().strftime("%H:%M:%S ") + msg
    print(line, flush=True)
    if logfile:
        Path(logfile).parent.mkdir(parents=True, exist_ok=True)
        with Path(logfile).open("a", encoding="utf-8") as f:
            f.write(line + "\n")


def http_download(url: str, dest: Path, timeout: int = 60, max_bytes: int = 80 * 1024 * 1024) -> "Path | None":
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r, dest.open("wb") as f:
            total = 0
            while True:
                chunk = r.read(1 << 16)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    f.close()
                    dest.unlink(missing_ok=True)
                    return None
                f.write(chunk)
        return dest
    except Exception:
        dest.unlink(missing_ok=True)
        return None


def die(msg: str, code: int = 2) -> None:
    print("error: " + msg, file=sys.stderr)
    sys.exit(code)


def need_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
        return True
    except Exception:
        die("Playwright is not installed in this interpreter. Run /adlab:setup, or run this tool with "
            + str(venv_python()))
