# Validation record — 6 October 2026

The final static quiz has 40 working remote animations, four rounds and unchanged q01–q40 order. All 40 source pages were read, every GIF was fetched with a real HTTPS GET, and every image frame passed structural/LZW validation and Pillow decoding. All 40 then loaded and showed changing pixels in Chrome at an actual HTTP `/repository-name/` path, observed for at least one complete decoded loop. No JavaScript page errors occurred.

The binaries were fetched into temporary inspection folders outside this project. **No third-party GIF files are bundled, and redistribution permission has not been established.** Remote availability is a dated result, not a guarantee for the venue network or future provider changes.

## Content and replacements

Every final frame sequence was visually screened using ordered contact sheets; complete-loop playback was also observed in the browser. No captions or watermarks spelling out a source title were found in the final selections. Ordinary dialogue remains where it does not name the answer. No explicit sexual content, graphic violence or heavy profanity was found in these selected clips. These observations do not replace the host's audience and display judgement.

Eight selections were improved, retaining the same answers:

- q05: replaced an unrelated meme caption with Kevin's uncaptioned scream.
- q09: replaced neon text/explosion edits with a plain dialogue scene.
- q12: replaced a narrow crop with a wider Woody/Buzz scene.
- q13: replaced a thumbnail with the larger individual source GIF.
- q20: replaced a harsh transition with a calmer kitchen scene.
- q21: replaced a dark six-frame clip with a longer recognizable cave scene.
- q28: replaced a face-swapped upload; rejected another candidate whose watermark revealed the title.
- q34: replaced the 31.8 MB film meme with a 2.1 MB scene from the television series.

q06's actual GIF is 403 × 200, rather than the small size suggested by the original metadata. q16 has no film-title overlay; its Netflix attribution remains. q36's full 24-frame desert dialogue clip contains none of the drugs, weapons or graphic content that motivated the initial caution.

## Gameplay and deployment checks

`python3 scripts/build_data.py`, `node tests/validate.cjs`, Python GIF-parser tests and JavaScript syntax checks pass. The current Node/Playwright suite uses real HTTP and real browser localStorage, with synthetic GIFs only for deterministic gameplay/error tests. It covers:

- Setup validation, safe team names, all 40 positions, hints, reveals and exact aliases.
- Timer start/pause/resume/expiry/reset, loading failures/timeouts, concealed motion, reveal stopping and a deterministically dispatched tab-visibility event.
- Reversible awards, revisits, void/restore, wildcard handling, tied final rankings and downloaded score exports.
- Persistence, malformed state, unavailable storage, reduced-motion opt-in and keyboard/native-button behavior.
- Actual full-screen entry/exit and a simulated denied-permission fallback.
- Root and nested repository URLs; an empty local map and missing-local-to-remote fallback.
- Four-worker host preflight, individual previews, approval persistence/invalidation and review exports. Load checks never grant visual approval.
- 1366 × 768 primary-control fit, 390 px layouts without horizontal overflow, and the answer-free printable sheet.

The four PNG screenshots show the real interface with **synthetic test media**, not film GIFs. Legacy Python browser harnesses are retained; the current verification used `tests/ui_smoke.cjs`, not their older storage shim. Real-provider playback is recorded separately by `tests/media_browser.cjs` without any media interception.

## Remaining checks and unresolved items

**Broken/unavailable media IDs: none in this run.** All final files are below 8 MiB; the largest is q29 at 6.03 MiB.

Projector quality remains unresolved for q03 (374 px), q08 (361 px), q31 (353 px), q33 (245 px) and q34 (374 px). q33 is the weakest-resolution clip: replace it with another permitted clip from the same series or void it if unreadable. q06, q19, q23 and q24 are also below the preferred 480 px width. q21 needs a contrast check because the cave is dim. q01/q15/q24 contain bright scene elements; q24/q37 include drinking and q33 includes mild hostile dialogue. Check their suitability on the actual display with the intended audience.

**Host venue approvals: 0.** No host approval boxes were prefilled. Use `review.html` privately to check actual loading, watch each loop, approve suitable clips and export the record. Physical projector contrast, OS tab switching and the venue network have not been tested here.

The local-media scanner correctly reports **0/40 local GIFs** and exits 1 because no permitted local copies were supplied. The empty map prevents 40 requests for nonexistent local files. This is a remote-media edition and requires internet access.

GitHub Pages packaging is ready: relative URLs, `.nojekyll` and nested-path checks pass. No repository was created, no commit or push was made, no live Pages deployment was tested, and nothing was published. Public deployment requires the user's approval.

## Evidence

- `initial-media-report.json`: original URL/binary audit before replacements.
- `remote-media-report.json`: final GETs, dimensions, sizes, frame counts and SHA-256 hashes.
- `content-review.json`: final-frame screening, cautions and explicit separation from venue/rights approval.
- `browser-media-results.json`: 40 actual browser animations, timing and changing-pixel hashes.
- `ui-test-results.json`: deterministic gameplay and failure-test scope.
- `../data/media-report.json`: local-files-only report; it must not be confused with remote validation.
