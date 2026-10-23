#!/usr/bin/env python3
"""export.py: build the Ad Bank board (one static HTML file) and the CSV from the workspace.

  python -I export.py --workspace DIR                 writes bank/ad-bank.html and bank/ad-bank.csv
  python -I export.py --workspace DIR --open          also opens the board in the default browser

Reads bank/entries.jsonl (one JSON object per bank entry; fields per library/rubrics/bank-entry-schema.md,
plus optional lists: hooks, risk_flags, competitor_refs, renders), concepts/*.md and personas/*.md
frontmatter for names, analysis/ads.csv for competitor references, and ads/ for card images.
The board has no external dependencies and works offline.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import sys
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import adlab_common as C  # noqa: E402

CSV_COLS = ["entry_id", "concept_id", "persona", "format", "aspect_ratio", "hook", "primary_text_short", "primary_text_long",
            "headline", "description", "cta", "script_or_layout_ref", "asset_refs", "why_it_should_work", "competitor_refs",
            "risk_flags", "critic_note", "editorial_score", "status", "version", "changelog"]

CSS = """
*{box-sizing:border-box}body{margin:0;background:#fff;color:#111;font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
header{padding:20px 24px;border-bottom:1px solid #ddd;display:flex;flex-wrap:wrap;gap:16px;align-items:baseline}
h1{font-size:20px;margin:0}.meta{color:#555;font-size:13px}
.filters{display:flex;flex-wrap:wrap;gap:10px;padding:14px 24px;border-bottom:1px solid #eee;position:sticky;top:0;background:#fff}
.filters label{font-size:13px;color:#333;display:flex;gap:6px;align-items:center}
select,input[type=search]{font:inherit;padding:6px 8px;border:1px solid #bbb;border-radius:3px;background:#fff}
main{padding:20px 24px;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:18px}
article{border:1px solid #ddd;border-radius:4px;padding:16px;display:flex;flex-direction:column;gap:10px;background:#fff}
article.hidden{display:none}
.id{font-size:12px;color:#666;display:flex;justify-content:space-between;gap:8px}
.hook{font-weight:700;font-size:18px;line-height:1.25}
.tags{display:flex;flex-wrap:wrap;gap:6px}.tag{font-size:12px;border:1px solid #ccc;border-radius:3px;padding:2px 7px;color:#333}
.tag.status-ready{border-color:#2a7a3b;color:#2a7a3b}.tag.status-draft{border-color:#999}.tag.status-retired{border-color:#b33;color:#b33}
.tag.risk{border-color:#b36b00;color:#b36b00}
.text{white-space:pre-wrap;color:#222}.small{font-size:13px;color:#444}
details summary{cursor:pointer;color:#333;font-size:13px}
.refs a{color:#0b57d0;text-decoration:none}.refs a:hover{text-decoration:underline}
.renders{display:flex;gap:8px;flex-wrap:wrap}.renders img{width:100px;border:1px solid #ddd}
.critic{border-left:3px solid #888;padding:6px 10px;background:#f7f7f7;font-size:13px}
.critic.block{border-left-color:#b33}.critic.revise{border-left-color:#b36b00}.critic.pass{border-left-color:#2a7a3b}
footer{padding:20px 24px;border-top:1px solid #ddd;color:#555;font-size:13px}
"""

JS = """
const sel=['persona','concept','format','status'].map(k=>document.getElementById('f-'+k));const q=document.getElementById('q');
function apply(){const v=sel.map(s=>s.value);const t=q.value.toLowerCase();
 document.querySelectorAll('article').forEach(a=>{const ok=['persona','concept','format','status'].every((k,i)=>!v[i]||a.dataset[k]===v[i])&&(!t||a.textContent.toLowerCase().includes(t));a.classList.toggle('hidden',!ok)});
 document.getElementById('count').textContent=document.querySelectorAll('article:not(.hidden)').length;}
sel.forEach(s=>s.addEventListener('change',apply));q.addEventListener('input',apply);apply();
"""


def esc(s):
    return html.escape("" if s is None else str(s))


def load_names(ws: Path, folder: str, idkey: str, namekey: str) -> dict:
    out = {}
    for f in sorted((ws / folder).glob("*.md")):
        fm, _ = C.read_frontmatter(f)
        i = fm.get(idkey) or f.stem
        out[str(i)] = str(fm.get(namekey) or f.stem)
    return out


def load_ads(ws: Path) -> dict:
    out = {}
    p = ws / "analysis" / "ads.csv"
    if p.exists():
        with p.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                out[r.get("ad_id", "")] = r
    for ad_json in (ws / "ads").glob("*/*/ad.json"):
        try:
            rec = json.loads(ad_json.read_text(encoding="utf-8"))
        except Exception:
            continue
        row = out.setdefault(rec["ad_id"], {})
        row.setdefault("advertiser", rec.get("advertiser"))
        row.setdefault("hook_text", (rec.get("body_text") or "")[:90])
        row["library_url"] = rec.get("library_url")
        card = rec.get("files", {}).get("card") or rec.get("files", {}).get("creative")
        if card:
            row["card"] = "../ads/" + card
    return out


def card_html(e: dict, personas: dict, concepts: dict, ads: dict) -> str:
    pid = str(e.get("persona", ""))
    cid = str(e.get("concept_id", ""))
    status = str(e.get("status", "draft"))
    tags = ["<span class='tag'>%s</span>" % esc(e.get("format", ""))]
    if e.get("aspect_ratio"):
        tags.append("<span class='tag'>%s</span>" % esc(e["aspect_ratio"]))
    tags.append("<span class='tag status-%s'>%s</span>" % (esc(status), esc(status)))
    for r in (e.get("risk_flags") or ([] if not e.get("risk_flags_text") else [e["risk_flags_text"]])):
        tags.append("<span class='tag risk'>risk: %s</span>" % esc(r))
    refs = []
    for ref in (e.get("competitor_refs") or []):
        a = ads.get(str(ref), {})
        label = "%s %s" % (esc(a.get("advertiser", "")), esc(ref))
        if a.get("library_url"):
            refs.append("<a href='%s' target='_blank' rel='noopener'>%s</a>" % (esc(a["library_url"]), label))
        else:
            refs.append(label)
    renders = "".join("<a href='%s' target='_blank'><img src='%s' alt='render'></a>" % (esc(r), esc(r)) for r in (e.get("renders") or []))
    hooks = "".join("<li>%s</li>" % esc(h) for h in (e.get("hooks") or []))
    critic = e.get("critic_note") or ""
    cclass = "pass" if critic.lower().startswith("pass") else "block" if critic.lower().startswith("block") else "revise" if critic else ""
    return """<article data-persona="%s" data-concept="%s" data-format="%s" data-status="%s">
<div class="id"><span>%s</span><span>%s · %s · score %s</span></div>
<div class="hook">%s</div>
<div class="tags">%s</div>
<div class="text">%s</div>
%s
<div class="small"><b>Headline:</b> %s · <b>CTA:</b> %s</div>
<details><summary>Why it should work</summary><div class="text small">%s</div></details>
%s
%s
%s
%s
</article>""" % (
        esc(pid), esc(cid), esc(e.get("format", "")), esc(status),
        esc(e.get("entry_id", "")), esc(personas.get(pid, pid)), esc(concepts.get(cid, cid)), esc(e.get("editorial_score", "")),
        esc(e.get("hook", "")), "".join(tags), esc(e.get("primary_text_short", "")),
        ("<details><summary>Long text</summary><div class='text small'>%s</div></details>" % esc(e["primary_text_long"])) if e.get("primary_text_long") else "",
        esc(e.get("headline", "")), esc(e.get("cta", "")),
        esc(e.get("why_it_should_work", "")),
        ("<details><summary>Hook options (%d)</summary><ul class='small'>%s</ul></details>" % (len(e.get("hooks") or []), hooks)) if hooks else "",
        ("<div class='refs small'><b>Competitor refs:</b> %s</div>" % ", ".join(refs)) if refs else "",
        ("<div class='renders'>%s</div>" % renders) if renders else "",
        ("<div class='critic %s'><b>Critic:</b> %s</div>" % (cclass, esc(critic))) if critic else "<div class='critic'>Critic has not reviewed this entry.</div>",
    )


def build(ws: Path) -> "tuple[Path, Path]":
    entries = C.read_jsonl(ws / "bank" / "entries.jsonl")
    personas = load_names(ws, "personas", "id", "name")
    concepts = load_names(ws, "concepts", "concept_id", "name")
    ads = load_ads(ws)
    brief = ""
    bp = ws / "business" / "brief.md"
    if bp.exists():
        fm, _ = C.read_frontmatter(bp)
        brief = str(fm.get("name") or fm.get("business") or "")
    opts = lambda vals: "".join("<option value='%s'>%s</option>" % (esc(v), esc(label)) for v, label in vals)  # noqa: E731
    pvals = sorted({str(e.get("persona", "")) for e in entries if e.get("persona")})
    cvals = sorted({str(e.get("concept_id", "")) for e in entries if e.get("concept_id")})
    fvals = sorted({str(e.get("format", "")) for e in entries if e.get("format")})
    svals = sorted({str(e.get("status", "draft")) for e in entries})
    cards = "\n".join(card_html(e, personas, concepts, ads) for e in entries)
    page = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ad Bank%s</title><style>%s</style></head><body>
<header><h1>Ad Bank%s</h1><span class="meta">%d entries · built %s · every entry is a hypothesis until tested; editorial scores are priorities, not performance</span></header>
<div class="filters">
<label>Persona <select id="f-persona"><option value="">all</option>%s</select></label>
<label>Concept <select id="f-concept"><option value="">all</option>%s</select></label>
<label>Format <select id="f-format"><option value="">all</option>%s</select></label>
<label>Status <select id="f-status"><option value="">all</option>%s</select></label>
<label>Search <input type="search" id="q" placeholder="hook, text, ref"></label>
<span class="meta"><span id="count">0</span> shown</span>
</div>
<main>%s</main>
<footer>Built by Ad Lab from bank/entries.jsonl. Competitor references point to the public ad libraries; competitor creatives are research references and are not republished.</footer>
<script>%s</script></body></html>""" % (
        (" · " + esc(brief)) if brief else "", CSS, (" · " + esc(brief)) if brief else "", len(entries), C.today(),
        opts([(v, personas.get(v, v)) for v in pvals]), opts([(v, concepts.get(v, v)) for v in cvals]),
        opts([(v, v) for v in fvals]), opts([(v, v) for v in svals]), cards, JS)
    out_html = ws / "bank" / "ad-bank.html"
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(page, encoding="utf-8")
    rows = []
    for e in entries:
        r = dict(e)
        for k in ("risk_flags", "competitor_refs", "asset_refs"):
            if isinstance(r.get(k), list):
                r[k] = "; ".join(str(x) for x in r[k])
        rows.append(r)
    out_csv = ws / "bank" / "ad-bank.csv"
    C.write_csv(out_csv, rows, CSV_COLS)
    return out_html, out_csv


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace")
    ap.add_argument("--open", action="store_true")
    args = ap.parse_args(argv)
    ws = C.workspace(args.workspace)
    h, c = build(ws)
    print("wrote", h)
    print("wrote", c)
    if args.open:
        webbrowser.open(h.as_uri())
    return 0


if __name__ == "__main__":
    sys.exit(main())
