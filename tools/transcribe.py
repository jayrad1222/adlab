#!/usr/bin/env python3
"""transcribe.py: timestamped transcript for a video, with whisper when it is installed.

Tries mlx-whisper (Apple Silicon), then faster-whisper. If neither is installed it writes a
transcript.md that says so, exits 0, and the analysis proceeds on frames and on-screen text.

  python -I transcribe.py --video path/to/video.mp4 --out path/to/ad_dir [--model small]
  python -I transcribe.py --all <workspace>/ads            (every ad folder with a video and no transcript yet)
  python -I transcribe.py --check                          (prints which backend is available)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

MLX_MODELS = {"tiny": "mlx-community/whisper-tiny-mlx", "base": "mlx-community/whisper-base-mlx",
              "small": "mlx-community/whisper-small-mlx", "medium": "mlx-community/whisper-medium-mlx"}


def backend():
    try:
        import mlx_whisper  # noqa: F401
        return "mlx-whisper"
    except Exception:
        pass
    try:
        import faster_whisper  # noqa: F401
        return "faster-whisper"
    except Exception:
        pass
    return None


def transcribe(video: Path, model: str):
    b = backend()
    if b == "mlx-whisper":
        import mlx_whisper
        res = mlx_whisper.transcribe(str(video), path_or_hf_repo=MLX_MODELS.get(model, model))
        segs = [{"start": s["start"], "end": s["end"], "text": s["text"].strip()} for s in res.get("segments", [])]
        return b, res.get("language"), segs
    if b == "faster-whisper":
        from faster_whisper import WhisperModel
        m = WhisperModel(model, compute_type="int8")
        segments, info = m.transcribe(str(video))
        segs = [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segments]
        return b, getattr(info, "language", None), segs
    return None, None, []


def fmt(t):
    m, s = divmod(int(t), 60)
    return "%d:%02d" % (m, s)


def write(out: Path, video: Path, b, lang, segs):
    if b is None:
        md = ("# Transcript\n\nNo transcription backend is installed (mlx-whisper or faster-whisper). "
              "Run /adlab:setup with transcription, or read the frames and on-screen text instead.\n")
        (out / "transcript.md").write_text(md, encoding="utf-8")
        (out / "transcript.json").write_text(json.dumps({"backend": None, "segments": []}), encoding="utf-8")
        return False
    lines = ["# Transcript", "", "Source: %s. Backend: %s. Language: %s. Made %s." % (video.name, b, lang, C.now_iso()), "",
             "Spoken words only; on-screen text is read from frames. Timestamps are approximate.", ""]
    for s in segs:
        lines.append("- [%s] %s" % (fmt(s["start"]), s["text"]))
    (out / "transcript.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "transcript.json").write_text(json.dumps({"backend": b, "language": lang, "segments": segs}, ensure_ascii=False, indent=1), encoding="utf-8")
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video")
    ap.add_argument("--out")
    ap.add_argument("--all")
    ap.add_argument("--model", default="small")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        print("backend:", backend() or "none installed")
        return 0
    jobs = []
    if args.video:
        jobs.append((Path(args.video), Path(args.out or Path(args.video).parent.parent)))
    if args.all:
        for ad_json in Path(args.all).glob("*/*/ad.json"):
            d = ad_json.parent
            v = d / "media" / "video.mp4"
            if v.exists() and not (d / "transcript.md").exists():
                jobs.append((v, d))
    if not jobs:
        ap.error("give --video or --all")
    for v, o in jobs:
        try:
            b, lang, segs = transcribe(v, args.model)
        except Exception as e:
            print("transcription failed for %s: %s" % (v, str(e)[:120]))
            b, lang, segs = None, None, []
        ok = write(o, v, b, lang, segs)
        print("%s: %s" % (o, ("%d segments via %s" % (len(segs), b)) if ok else "no transcript (backend missing)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
