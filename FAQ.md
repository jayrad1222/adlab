# FAQ

**Is this allowed?** You are reading public ad libraries that the platforms publish for transparency, on your own machine, without logging in, one page at a time. Platform terms may still restrict automated access; read [LEGAL-AND-ETHICS.md](LEGAL-AND-ETHICS.md). If you prefer not to automate, Lite mode uses links and screenshots you gather yourself, and the Apify route uses a paid third party.

**How long does a full run take?** Intake ten minutes with you. Pull 20 to 60 minutes unattended. Process 10 to 30. Analyze is the longest step, often an hour for two hundred ads. Personas and the rest are minutes each plus your reviews. Plan for an evening.

**How much does it cost?** The pulls cost nothing. Claude usage is the main cost; the per-ad analysis runs on a cheaper model in batches to keep it down, and the default caps (40 ads per advertiser, 8 advertisers) are there for that reason. Apify and Higgsfield are optional and show their price before every call.

**My competitor's Page shows zero ads. Are they not advertising?** Maybe, or their ads run under a platform's Page. Skool runs "X with Skool" ads for creators; marketplaces and platforms do similar things. The pull searches for this; the market map says when it found co-branded ads.

**Why does the market map keep saying "clue, not a verdict"?** Because an ad that has run 200 days tells you it has run 200 days. It does not tell you it is profitable, and an active-only sample cannot tell you how many ads were launched and stopped. The tool prints these caveats on purpose.

**The tool refused to generate an image.** Generated media is for mood and b-roll only. Anything that would read as proof (a screenshot, a review, a result, a customer) must come from your own assets, with consent recorded in the catalog.

**Can I use it for clients?** Yes: `/adlab:start --client <name>` makes a separate workspace per client under `adlab-workspace/clients/`. The library is shared; the workspaces are not.

**I have no website yet.** Run `/adlab:intake "two sentences about the offer"`. Competitor discovery leans on category searches instead of your site.

**Something broke.** `/adlab:doctor`. It prints the fix in plain words. If Meta shows a login or checkpoint page, wait an hour or switch to Lite mode; never log in.

**Where is my data?** In `./adlab-workspace/` in the folder you opened. Nothing is uploaded anywhere by the tool.
