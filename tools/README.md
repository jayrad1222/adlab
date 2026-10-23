# tools/

Python 3.9+, standard library plus Playwright (venv). Every tool has `--help`. Run through `run.py` to use the venv interpreter:

```
python3 -I tools/run.py <tool> [args]
```

| Tool | Does | Spends |
|---|---|---|
| setup.py | venv, packages, Chromium, optional whisper and keys | no |
| doctor.py | checks the install and the libraries, prints fixes | no |
| meta_pull.py | Meta Ad Library pull, read-only, no login | no |
| google_pull.py | Google Ads Transparency Center pull | no |
| linkedin_pull.py | LinkedIn Ad Library pull | no |
| tiktok_ccl_pull.py | TikTok Commercial Content Library pull (EEA, CH, UK ads) | no |
| manual_pull.py | links and screenshots into ad records (Lite mode) | no |
| apify_pull.py | optional actor run, price shown first | yes, with --yes |
| media.py | frames, poster, contact sheet per video | no |
| transcribe.py | whisper transcript when installed | no |
| landing.py | landing page text and screenshots | no |
| rows.py | batches for analysts; validated merge into analysis/ads.csv | no |
| finance.py | economics from business/finance.md | no |
| export.py | the board and the CSV from bank/entries.jsonl | no |
| render.py | templates to PNG at three sizes; storyboards; simple video | no |
| higgsfield.py | generated mood media, price shown first, floor respected | yes, with --yes |
| readout.py | Ads Manager export to decision rules | no |
| progress.py | PROGRESS.md and changelog.md | no |

Tests: `python3 -I -m unittest discover -s tools/tests -p "test_*.py"`.

Record schema shared by the pull tools: see `meta_pull.normalize`. Member data never lives here; it lives in `./adlab-workspace/`.
