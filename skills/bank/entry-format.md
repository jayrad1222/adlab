# bank/entries.jsonl entry format

One JSON object per line. Fields from the bank-entry schema plus working fields.

```json
{
 "entry_id": "c01-e01",
 "concept_id": "c01",
 "persona": "p1",
 "format": "static-problem-card",
 "aspect_ratio": "4x5",
 "hook": "The invoice pile is still there at 11pm.",
 "primary_text_short": "under 125 characters",
 "primary_text_medium": "about 300 characters",
 "primary_text_long": "the long version, line breaks allowed",
 "headline": "under 40 characters",
 "description": "one line",
 "cta": "Learn more",
 "script_or_layout_ref": "templates/problem-card.html",
 "layout_template": "problem-card.html",
 "layout_fields": {"kicker": "...", "hook": "...", "offer_line": "...", "photo_image": "assets/x.jpg"},
 "script": "for video entries: the table of time, frame, on-screen text, spoken line",
 "hooks": ["six hook options, tagged (hook-type)"],
 "asset_refs": ["catalog row ids"],
 "why_it_should_work": "mechanism (library file), persona, the evidence ids",
 "competitor_refs": ["ad ids this answers"],
 "risk_flags": [],
 "critic_note": "pass | revise: ... | block: ...",
 "editorial_score": 10,
 "status": "draft | ready | rendered | testing | retired",
 "version": 1,
 "changelog": "",
 "renders": [],
 "cpa_to_beat": null,
 "ai_media": false
}
```

`primary_text_medium` is a working field (the CSV keeps short and long). `export.py` reads `hooks`, `risk_flags`, `competitor_refs`, `renders` as lists.
