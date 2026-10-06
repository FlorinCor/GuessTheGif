# Validation record — 6 October 2026

The quiz now contains 100 actual animated GIF selections in ten rounds of ten. The original q01–q40 entries and order are unchanged; q41–q100 add 60 new sources. The game remains vanilla HTML/CSS/JavaScript with relative URLs, `.nojekyll` and no deployed build step. Pacing is flexible and the manually started timer is optional.

All 100 final source pages were read, all 100 media URLs returned valid animations in real HTTPS GETs, and every frame passed structural/LZW validation and Pillow decoding. All 100 then loaded and showed changing pixels in Chrome at an actual HTTP `/repository-name/` path for at least a complete decoded loop, with no JavaScript page errors. Binary hashes in the audit identify the screened files; hashes for the original 40 still match their earlier screening record.

Inspection binaries and frame sheets stay in temporary folders outside the project. **No third-party GIFs are bundled, and redistribution rights have not been established.** Availability is a dated check; the host must still test the venue network and display.

## Content and curation

Every final composited frame sequence was screened in order. No answer-title captions or watermarks were found in the final selections. Ordinary dialogue, character names that differ from the source title, and non-title creator/network attribution remain. No explicit sexual content, graphic violence or heavy profanity was found in these clips. This is content screening of particular GIFs, separate from venue/audience approval.

For the expansion, title-spoiling Dumb and Dumber and Beetlejuice captions were rejected. Several Schitt’s Creek candidates were rejected for title watermarks, including a small watermark appearing later in a loop. The final clip shows David in a polka-dot sweater and a towel. Other new selections were improved to avoid distracting colours, unrelated captions and poor crops. This project did not strip watermarks or manufacture GIF hashes.

The earlier eight replacements remain: q05, q09, q12, q13, q20, q21, q28 and q34. Their reasons and initial audit are preserved in Git history and `initial-media-report.json`; their current clips and screening notes remain in `content-review.json`. In particular q28's face-swapped candidate and q34's 31.8 MB film meme were replaced before the first publication.

## Gameplay and print checks

The builder, dataset/path/alias validator, eight Python GIF-parser tests and JavaScript syntax checks pass. The Node/Playwright gameplay suite uses real HTTP/localStorage and synthetic media for deterministic tests, separately from the actual-provider playback suite. Its 14 passing groups cover:

- All 100 navigation positions, exact reveals/aliases and TV prompting in both TV rounds; the q30 video-game wildcard.
- Setup/team validation, safe team-name rendering and answer-free headings, alt text and source links before reveal.
- Manual timer start/pause/resume/expiry/reset, media failures/timeouts, hidden motion, reveal stopping and a deterministic tab-visibility event.
- Reversible scoring, revisits, void/restore, ties, final rankings and downloaded score exports.
- Existing 40-question saved progress continuing into q41; q100 awards, void/restore, revisits, saved resume and final totals.
- Corrupt or denied storage, reduced-motion opt-in, all shortcuts, native focused-button Space, typing and full-screen entry/exit/denial.
- Root and nested paths, empty local map, local-to-remote fallback, four-worker preflight, previews, saved approvals/invalidation and review export. Load checks grant no approvals.
- 1366 × 768 primary controls and 390 px setup/game layouts without horizontal overflow.

The generated answer sheet has exactly 100 answer spaces and no answers. Chrome printed it to a temporary PDF: Poppler confirmed three A4 pages, and all pages were visually inspected. White print margins avoid the site's dark-screen theme using extra ink. The PDF is a private QA intermediate, not a bundled site file.

The four interface PNGs use synthetic test media. Legacy Python browser harnesses were updated for the current dataset, syntax-checked and retained, but were not used for these browser results.

## Unresolved venue checks

**Broken/unavailable media IDs: none in the final dated checks.** All GIFs are below 8 MiB; the largest is q91 at 7.80 MiB. All 60 added clips are at least 480 px wide. q87, q91 and q95 are larger downloads: allow time for loading.

The original resolution cautions remain: q03 (374 px), q08 (361 px), q31 (353 px), q33 (245 px) and q34 (374 px) need projector checks; q33 is the weakest and should be voided if unreadable. q06/q19/q23/q24 also fall below the preferred 480 px width. These were preserved with the original 40 entries.

Check contrast for q21's cave and the darker new scenes q47/q50/q67/q76/q89/q95. q01/q15/q24 and new q79/q90 have bright or changing lighting. q24/q37/q85 include drinking; q33 has mild hostile dialogue; q67 has a cartoon romantic reaction; q79 has emotional crying; q98 shows a pistol without injury or graphic action. Audience/display suitability is a host decision, documented per question.

**Host venue approvals: 0.** No approval boxes are prefilled. Watch every loop on the actual network/display using `review.html`, approve genuinely suitable clips and export the record. Physical projector contrast and OS tab switching remain untested here.

The local scanner reports **0/100 local animations** and correctly exits 1 because no permitted local files were supplied. The empty map avoids nonexistent local-file requests. This remote-media edition requires internet access.

## Evidence and deployment

- `remote-media-report.json`: 100 real GET checks, decoded dimensions/frames/sizes and SHA-256 hashes.
- `content-review.json`: 100 screened sequences, curation and audience cautions; no venue or rights approval.
- `browser-media-results.json`: 100 actual browser animations at the nested local HTTP path.
- `ui-test-results.json`: 14 deterministic gameplay/failure test groups with synthetic media.
- `print-test-results.json`: three-page A4 print verification.
- `../data/media-report.json`: local files only, 0/100; separate from remote validation.

The owner explicitly approved the public [FlorinCor/GuessTheGif repository](https://github.com/FlorinCor/GuessTheGif) and [GitHub Pages site](https://florincor.github.io/GuessTheGif/). Pages uses `main` at `/(root)` with HTTPS. The original 40-question deployment succeeded and was checked with live GIFs. The 100-question edition is prepared and locally validated; its public deployment and live verification are the remaining release steps.
