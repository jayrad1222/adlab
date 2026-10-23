# Legal and ethics

Ad Lab is research tooling for your own marketing. It is built around these rules.

**Read-only, on your machine, no login.** The pull tools load public ad library pages the way a browser does, one page at a time with pauses, never sign in, never like, follow, message or submit anything, and save what the page shows into your private workspace. Platform terms of service may restrict automated access to these pages, and they change. You are responsible for how you use the tool. If you would rather not automate, use Lite mode (links and screenshots you gather yourself) or the Apify route (a paid third-party service with its own terms).

**Competitor creatives are references, not assets.** Images, videos and card screenshots pulled into `adlab-workspace/ads/` are for your analysis. Do not republish them, post them in a community, or use them in your own ads. The ad bank board links to the public library pages instead of embedding competitor media. The example runs shipped with the plugin contain no competitor media for the same reason.

**No fabricated proof.** The tool will not write a testimonial, a result, a count, a screenshot or a scarcity claim that your asset catalog cannot support, and it refuses image prompts that would read as proof. Endorsements must be real and disclosed where the law requires it; "results not typical" does not excuse a made-up result.

**Consent.** Any person other than you who appears in an asset, and any customer whose words you quote, needs recorded consent in `assets/catalog.md` before a bank entry can use them. The critic blocks entries that skip this.

**Generated media is labeled.** Anything produced through the Higgsfield API is marked AI-generated in the bank and should carry whatever label the platform requires at the time you run it.

**Platform policies win.** The library's policy notes are a guide; the live policy pages of Meta, TikTok, Google and LinkedIn are the authority, and they change.

**Your data stays yours.** The tool writes to `./adlab-workspace/` and the plugin data folder on your machine. It uploads nothing. Optional keys you enter are stored locally with owner-only permissions.

**No promises.** Everything Ad Lab writes is a hypothesis until your own readout says otherwise. Editorial scores are priorities, not predictions. Nothing in the output is a guarantee of results.
