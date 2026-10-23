# Specs and safe zones

This file gives the sizes, safe zones, and legibility rules the render step and the critic use so a creative reads correctly on a phone. Every number below is guidance, not law: the platforms change their interfaces, and the live spec pages win when they disagree with this file.

## The three aspect ratios the bank ships

- **1:1 (square).** 1080 by 1080 pixels. Works in Facebook and Instagram feed and in most carousel placements. The safest single size if only one can be made.
- **4:5 (vertical feed).** 1080 by 1350 pixels. Takes more of the phone screen in feed than 1:1 without being cropped. The default for feed statics and feed video.
- **9:16 (full vertical).** 1080 by 1920 pixels. Reels, Stories, TikTok, and YouTube Shorts. The default for short video and the only ratio where interface overlays cover part of the frame.

Export each concept in all three unless the test plan excludes a placement. Do not stretch; recompose. A 4:5 can usually be cropped from a 9:16 master if the subject sits in the middle band.

## Safe zones for 9:16 (guidance)

On Reels, Stories, TikTok, and Shorts, the platform draws its own controls over the video: the account name and caption at the bottom, the like, comment, and share stack on the right, and status or progress elements at the top. Anything placed there is hidden or hard to read.

As guidance, keep essential text and faces inside a central band and treat these as covered:

- The top roughly 14 percent of the frame (about 250 to 270 pixels on a 1080 by 1920 canvas).
- The bottom roughly 20 to 35 percent (about 400 to 650 pixels), where captions, the CTA button, and the audio tag sit. TikTok's bottom overlay is taller than Meta's.
- A column of roughly 10 to 12 percent on the right edge (about 120 pixels) for the engagement stack.

The safe area that results is roughly the middle 1080 by 1000 pixels, offset slightly left. The render step should draw a safe-zone overlay on every 9:16 proof and the critic should reject text that crosses it. Check the current overlay on a live phone before a big build; the exact pixel counts drift with every app update.

## The first three seconds

Platforms count a view at three seconds and Ad Lab reads hook rate as three-second plays over impressions. The hook, in words or in picture, must land before the three-second mark. Practical rules: the first frame is already the hook (no logo sting, no fade-in); the first spoken or on-screen line is the hook line from the bank; movement or a face appears in the first second; the product or the problem is visible by the third.

A static has no three seconds. Its equivalent is the two-second stranger test in the rubrics: can a stranger say what it is and who it is for after two seconds.

## Captions on by default

Most feed video is watched without sound. Every video in the bank ships with burned-in captions inside the safe zone. Platform auto-captions are a fallback, not the plan: they get names and numbers wrong and sit where the platform puts them. Keep captions to two lines and time them to the spoken line.

## Legibility at phone size (guidance)

The frame will be viewed at roughly 2.5 to 3 inches wide. As guidance, on a 1080-pixel-wide canvas:

- Headline or hook text: about 70 pixels tall or more.
- Body or caption text: about 40 to 48 pixels tall or more.
- Anything under about 32 pixels is fine print and will not be read.

Use high contrast, a solid or semi-opaque backing when text sits over footage, no thin weights, and lines under about 30 characters. The test is simple: view the export on a phone at arm's length. Density matters as much as size; the per-ad rubric tags on-screen text density, and most native ads sit at low or medium.

## File guidance

- **Video:** MP4 (H.264) or MOV, square pixels, fixed frame rate (24, 25, or 30 fps), stereo AAC audio even when the cut is silent, and a file size well under the platform caps (Meta accepts files up to several gigabytes; keep exports under a few hundred megabytes for upload speed). Length: short for Reels and TikTok (15 to 60 seconds is the usual range), with feed video able to run longer.
- **Images:** JPG or PNG at the sizes above. Keep under a few megabytes. PNG for flat graphics with text, JPG for photos.
- **Carousels:** every card the same ratio, 1:1 or 4:5. Up to ten cards on Meta; the first card does the work.
- **Naming:** `<concept>-<hook>-<ratio>-<version>` so the asset catalog and the test readout can match assets to results.

Read the current spec page for each platform before the first upload; frame rate and bitrate limits change.

## Related

- [tiktok-youtube-differences.md](tiktok-youtube-differences.md)
- [meta-policy-pitfalls.md](meta-policy-pitfalls.md)
- [../rubrics/two-second-stranger-test.md](../rubrics/two-second-stranger-test.md)
- [../rubrics/asset-catalog-schema.md](../rubrics/asset-catalog-schema.md)
- [../rubrics/critic-checklist.md](../rubrics/critic-checklist.md)
- [../finance/signals-glossary.md](../finance/signals-glossary.md)

## Sources

- Ad Lab framework seed, section 8 (specs: 1:1, 4:5, 9:16; safe zones for 9:16 overlays; first three seconds; captions on by default; legibility at phone size), October 2026.
- Meta Ads Guide and the Meta Business Help Center pages on Reels and Stories safe zones; TikTok's ad specifications pages; YouTube's Shorts ad specifications. Read the live pages; the pixel figures above are guidance drawn from common practice, not quotations.
