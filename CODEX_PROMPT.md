# Codex task — finish and validate The GIF Break

Work in this extracted project folder. Build a reliable, attractive, very simple static quiz for a one-hour activity with colleagues. The attached starter already contains a working vanilla HTML/CSS/JavaScript implementation and 40 researched GIF selections. Inspect and improve it; do not restart with a framework.

## Read first
Read `README.md`, `HOST_GUIDE.md`, `ANSWER_KEY.md`, `data/questions.json`, `index.html`, `app.js`, `styles.css`, `review.html`, `review.js` and `scripts/media.py`.

The canonical dataset is `data/questions.json`. It contains exactly 40 questions, each with a source title/answer, accepted aliases, an original hint, scene description, direct media URL, source-page URL and neutral local filename. `data/questions.js` is generated from it. Run `python3 scripts/build_data.py` after edits; it also regenerates the answer key.

Important: the preparation environment could read source-page metadata but could not download the GIF binaries. No actual GIF files are supplied. None has passed a complete playback/content check. GIFDB media URLs marked `derived-provider-path` use the provider's URL convention and must be validated, not assumed correct. Do not report that 40 GIFs work until you have actually checked them.

## Intended experience
One host operates one laptop/projector or shared meeting screen. Teams discuss and write their guesses on paper. This is NOT live multi-device multiplayer: no accounts, forms service, backend, database, Firebase, analytics, tracking scripts or API keys.

Use four rounds of ten in the supplied fixed order. Keep q01–q40 stable so the answer key and printable sheets match. Preserve the mix of broad film/animation favourites and television, with q30 as an explicitly announced video-game wildcard. Default to 45 seconds thinking time and roughly 15 seconds for the answer and points. Include the separate one-hour running order from HOST_GUIDE.md.

## Media is the first priority
1. Check all 40 listed source/media pairs. Where appropriate permissions and provider terms permit local copies, use `python3 scripts/media.py --download --rights-reviewed`. The flag records an operator choice; it is not a licence. Do not claim that an online GIF is automatically free to redistribute or that an internal office game is automatically exempt from copyright.
2. The downloader must reject HTML/error pages, truncated files and single-frame images; preserve GIF animation. Do not scrape around access controls, use credentials or bypass provider restrictions. The supplied script only requests the individual direct URLs.
3. For a broken endpoint, privately open the specific `sourceUrl` and get the provider's actual allowed download/embed URL. If unavailable, find a replacement scene from the SAME movie/show wherever practical; update both mediaUrl and sourceUrl. Never invent provider hashes or file paths. Do not substitute still images and call them GIFs.
4. Inspect every complete loop. Reject clips with title cards, text revealing the answer, inappropriate sexual content, graphic violence, heavy profanity, distracting edits, excessive flashes or poor projector legibility. Captions containing ordinary dialogue are acceptable when they do not name the source. Do not strip attribution or watermarks just to hide a title; choose a different clip.
5. Special checks: q06 and q13 are small; q12 may be a meme/crop; q16 needs scene/overlay verification; q34 is approximately 30 MB; q36 requires workplace screening. Prefer roughly 480–800 px-wide GIFs and files below 8 MB where possible. Optimize permitted local copies without destroying legibility or animation. Do not invent that every source meets these targets.
6. Store usable local copies as `assets/gifs/q01.gif` through `q40.gif`. Run `python3 scripts/media.py` to rebuild `data/local-media.js` and a truthful report. The site should prefer validated local files and fall back to the supplied remote URL if a local file cannot load. Avoid trying 40 nonexistent local files when no download map exists.
7. Keep source attribution in the host review and answer reveal, plus the answer key. Do not embed provider browsing pages, recommendation widgets or unrelated content in the player view.
8. Retain a host-only-by-convention preflight page that loads/checks all media with limited concurrency, previews individual clips, allows genuine visual approvals and exports the review record. A load success is not a content approval. Mark unresolved items explicitly. Never fabricate a passed test or an approval.

## Gameplay and behaviour
- Setup: 2–8 editable team names; default 45-second timer; start/resume game.
- Main screen: dominant centred GIF using object-fit: contain, question/round progress, clear timer, hint, reveal, previous/next, hide/show motion, optional browser full screen and scores.
- The timer starts ONLY after the media is ready and the host presses Start. Loading, hidden motion, a failed clip or leaving the tab must never silently consume thinking time. No automatic answer reveal or automatic next question.
- Revealing an answer stops the timer. Show the source title, accepted aliases, scene cue and source link only after reveal. No source title in player-visible headings, captions or alt text before reveal. Runtime filenames and metadata are not anti-cheat protection; never pretend otherwise.
- One point per correct team per question. Use a reversible per-question award toggle, not an unrestricted counter that can accidentally double-award. Preserve the score when revisiting a question. A voided question contributes no points and is removed from the maximum for every team.
- Accept broad film franchises only where allowed by the data. For ambiguous Nemo/Dory accept either. q39 requires Wednesday/Mercredi, and q40 requires The Mandalorian, not just a character name. Do not demand an exact installment the source evidence does not establish.
- Save progress/team names/awards in localStorage, with graceful handling when unavailable or corrupted. Show a final leaderboard with ties and score export. Team names should be inserted with textContent, never unsafe HTML.
- Keep keyboard shortcuts: Space timer, R reveal, H hint, arrows navigate, M motion. Do not intercept typing or native button actions. Preserve visible focus and usable touch targets.
- Respect prefers-reduced-motion by starting clips concealed until the host opts in. A hide-motion button is honest; do not call it GIF pause unless you implement a genuine controlled video or canvas player. Do not introduce flashing countdown effects or sound autoplay.

## Visual design
Keep the existing clean, dark, black-and-white cinema-night look. Large typography, generous spacing, thin borders, understated rounded panels and a very large undistorted media stage. Make it pleasant on a 16:9 projector and usable at 390 px width. No decorative emoji, stock-photo collage, excessive gradients, external fonts or unnecessary animations. The GIF is the focus. Keep preparation/debug warnings on the host page, not constantly over the game.

## Technical and deployment constraints
Use only static HTML, CSS, JavaScript and media. No build step required for the deployed site. All internal URLs must be relative so both a domain root and GitHub Pages `/repository-name/` work. Keep `.nojekyll`. Retain the printable `answer-sheet.html` without answers. Do not publish credentials, internal work information or private attendee data.

Prepare for GitHub Pages: repository Settings → Pages → Deploy from a branch → main → /(root). Do not create a repo or push publicly unless separately authorized. A public static site exposes its answer data to inspection; this is an honour-system social game, not secure exam software. `noindex` is not access control.

## Verification and delivery
Run `python3 scripts/build_data.py`, `node tests/validate.cjs` and available browser tests. Test desktop and mobile layouts, all 40 navigation positions, timer pause/resume/expiry, reveal, aliases, score toggling, revisits, void/restore, final ranking, persistence, storage errors, media timeouts and local-to-remote fallback. Test at a nested repository path, not just `/`.

Keep fixture/mock tests separate from real-media checks. The supplied UI smoke test uses synthetic GIF fixtures because external media was inaccessible during preparation; passing it does not prove any film GIF plays. Use actual GIFs for the final media/content report. Add or fix tests as needed. Do not skip tests merely to reduce tokens.

Deliver the completed static folder, exact local preview/deployment steps, brief change summary and an honest validation report listing any unresolved media IDs. If network access is blocked, finish every offline-testable part, preserve the full source list and clearly report the blocked checks rather than inventing assets or saying the whole project is production-verified. Keep progress updates and the final summary brief; do not reprint every source file.
