#!/usr/bin/env python3
"""media.py: frames, poster, duration and a contact sheet for a video, using imageio-ffmpeg (no system ffmpeg).

  python -I media.py --video path/to/video.mp4 --out path/to/ad_dir [--every 2] [--scene 0.3] [--max-frames 24]
  python -I media.py --ad-dir <workspace>/ads/<advertiser>/<ad_id>        (finds media/video.mp4 itself)
  python -I media.py --all <workspace>/ads                                 (every ad folder with a video and no frames yet)

Writes <out>/frames/f-NNN.jpg (every N seconds plus scene changes), <out>/frames/poster.jpg,
<out>/frames/contact.jpg (a tiled sheet) and <out>/media.json (duration, frame list).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402


def ffmpeg_bin() -> str:
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def duration_s(video: Path) -> "float | None":
    try:
        r = subprocess.run([ffmpeg_bin(), "-i", str(video)], capture_output=True, text=True)
        m = re.search(r"Duration: (\d+):(\d+):(\d+\.?\d*)", r.stderr)
        if m:
            h, mi, s = m.groups()
            return int(h) * 3600 + int(mi) * 60 + float(s)
    except Exception:
        pass
    return None


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def process(video: Path, out: Path, every: float, scene: float, max_frames: int) -> dict:
    fr = out / "frames"
    fr.mkdir(parents=True, exist_ok=True)
    ff = ffmpeg_bin()
    dur = duration_s(video)
    run([ff, "-y", "-loglevel", "error", "-i", str(video), "-vf", "fps=1/%s,scale=540:-2" % every,
         "-frames:v", str(max_frames), str(fr / "f-%03d.jpg")])
    run([ff, "-y", "-loglevel", "error", "-i", str(video), "-vf", "select='gt(scene,%s)',scale=540:-2" % scene,
         "-vsync", "vfr", "-frames:v", str(max_frames), str(fr / "s-%03d.jpg")])
    run([ff, "-y", "-loglevel", "error", "-ss", "0", "-i", str(video), "-frames:v", "1", "-vf", "scale=720:-2", str(fr / "poster.jpg")])
    run([ff, "-y", "-loglevel", "error", "-i", str(video), "-vf", "fps=1/%s,scale=270:-2,tile=4x4" % every,
         "-frames:v", "1", str(fr / "contact.jpg")])
    frames = sorted(p.name for p in fr.glob("f-*.jpg"))
    scenes = sorted(p.name for p in fr.glob("s-*.jpg"))
    info = {"video": str(video), "duration_s": dur, "every_s": every, "frames": frames, "scene_frames": scenes,
            "poster": "frames/poster.jpg" if (fr / "poster.jpg").exists() else None,
            "contact": "frames/contact.jpg" if (fr / "contact.jpg").exists() else None, "made": C.now_iso()}
    (out / "media.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    return info


def find_video(ad_dir: Path) -> "Path | None":
    for name in ("media/video.mp4", "video.mp4"):
        p = ad_dir / name
        if p.exists():
            return p
    vids = list((ad_dir / "media").glob("*.mp4")) if (ad_dir / "media").exists() else []
    return vids[0] if vids else None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video")
    ap.add_argument("--out")
    ap.add_argument("--ad-dir")
    ap.add_argument("--all", help="ads folder; process every ad with a video and no frames yet")
    ap.add_argument("--every", type=float, default=2.0)
    ap.add_argument("--scene", type=float, default=0.3)
    ap.add_argument("--max-frames", type=int, default=24)
    args = ap.parse_args(argv)
    jobs = []
    if args.video:
        jobs.append((Path(args.video), Path(args.out or Path(args.video).parent.parent)))
    if args.ad_dir:
        v = find_video(Path(args.ad_dir))
        if v:
            jobs.append((v, Path(args.ad_dir)))
        else:
            print("no video in", args.ad_dir)
    if args.all:
        for ad_json in Path(args.all).glob("*/*/ad.json"):
            d = ad_json.parent
            v = find_video(d)
            if v and not (d / "media.json").exists():
                jobs.append((v, d))
    if not jobs:
        ap.error("nothing to do: give --video, --ad-dir or --all")
    for v, o in jobs:
        info = process(v, o, args.every, args.scene, args.max_frames)
        print("%s: %.1fs, %d frames, %d scene changes" % (o, info["duration_s"] or 0, len(info["frames"]), len(info["scene_frames"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
