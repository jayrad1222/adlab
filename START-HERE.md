# Ad Lab: start here

Ad Lab is a Claude Code plugin that decodes your market from the public ad libraries and builds you an evidence-backed ad bank. You paste your website, answer a short interrogation, confirm a list of competitors, and the tool pulls their ads, analyzes every one, builds buying-situation personas, grills your business the way a behavioural-science strategist would, writes your own ads with the reasoning shown for every line, and gives you a finance-grounded test plan. Then you run the ads yourself and bring back the numbers.

## What it does not do

- It never launches, edits or touches an ad account. It reads exports you give it.
- It never republishes competitor creatives. They stay in your private workspace as research references.
- It never invents proof. No made-up results, testimonials, counts, scarcity or urgency. Every claim in your bank traces to something you own.
- It does not promise results. Everything it writes is a hypothesis until a readout says otherwise.

## The twenty-minute first run

1. Install (see [INSTALL.md](INSTALL.md)): two commands, then `/adlab:setup` once per machine. Three to eight minutes, mostly a browser download.
2. `/adlab:start`: creates `./adlab-workspace/` in the folder you opened and asks for your website or a two-sentence description.
3. `/adlab:intake <url>`: reads your site, then asks twelve questions in two batches, each with a default. Answer "defaults" if you are in a hurry; come back to them later.
4. `/adlab:competitors`: proposes three rings of competitors with reasons. Cross out, add, say go.
5. `/adlab:pull`: runs in the background for 20 to 60 minutes. Make coffee.

From there: `/adlab:process`, `/adlab:analyze` (the long one), `/adlab:personas` (your review), `/adlab:interrogate`, `/adlab:angles`, `/adlab:bank`, `/adlab:assets` (drop your photos, videos and screenshots into `adlab-workspace/assets/`), `/adlab:render`, `/adlab:plan`. After your first week of ads, export the report and run `/adlab:readout`. Later, `/adlab:refresh`.

`/adlab:doctor` explains anything that breaks. `PROGRESS.md` in the workspace shows where you are, so you can stop and resume any time.

## No Python, or Windows trouble? Lite mode

Skip `/adlab:setup`. Run `/adlab:start`, then paste ad library links or drop screenshots: `/adlab:pull --mode manual --urls <links>` or `--screenshots <folder>`. Everything from analyze onward works the same.

## Read an example first

Two finished runs live in [examples/](examples/): a Skool community and a physical product. Open an `analysis/market-map.md` and a `bank/ad-bank.html` to see what you will get.

## The idea behind it

The strategic unit is the angle, not the hook. One working angle yields many hooks and several formats; one hook yields one ad. The tool decodes what angles your market already runs, who it talks to, who it ignores, and what nobody is saying, then builds concepts from that evidence. The reasoning is the product: every line shows the persona, the mechanism and the competitor ads it answers.
