# The GIF Break

A simple static film/TV quiz for a one-hour shared-screen activity: 40 questions in four rounds, a manual timer, hidden answers, reversible team scoring, saved games, a printable answer sheet and a host review page. q30 is an announced video-game wildcard. No framework, account, backend, analytics or deployed build step is required.

## Current status

On 6 October 2026, all 40 final remote GIFs passed real GETs, full-frame decoding and actual Chrome playback over a complete loop. Every final frame sequence was screened for source-title spoilers and unsuitable content. Eight selections were replaced. Gameplay tests pass at both the domain root and `/repository-name/`.

**No third-party GIFs are bundled.** The site currently needs internet access. No broken URLs remain in the dated checks, but host review on the venue network/display is still required. q03, q08, q31, q33 and q34 have widths below 400 px; q33 is particularly small. See [the validation report](evidence/VALIDATION.md) for exact scope, further cautions and evidence. No host approvals or redistribution permissions have been fabricated.

## Local preview

Open a terminal in this folder and run:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open [the game](http://127.0.0.1:8000/). Before projecting, open [host review](http://127.0.0.1:8000/review.html), check all links, preview every loop, tick genuine approvals and export the review record. Print `answer-sheet.html`; keep the review page and answer key off the shared display. Stop the preview server with Ctrl+C.

For a manual repository-path preview, run from this folder:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory ..
```

Open [the nested game URL](http://127.0.0.1:8000/GuessTheGif/). Browser tests also serve the exact `/repository-name/` shape.

## Optional permitted local GIFs

Review provider terms and obtain permission for the intended copying/use before downloading. This project grants no rights in third-party scenes; the flag records an operator decision and is not a licence.

```sh
python3 scripts/media.py --download --rights-reviewed
# Or download a single permitted selection:
python3 scripts/media.py --download --rights-reviewed --id q01
# Scan existing local files without network requests:
python3 scripts/media.py
```

The standard-library script requires multiple frames, validates GIF structure and LZW pixel counts, rejects HTML/stills/truncation, and writes `data/local-media.js` and `data/media-report.json`. Exit 0 means all 40 local animations validate; exit 1 means missing/invalid local files. Neither establishes visual approval or permission. With this delivery, 0 local files is expected. Valid local files are preferred; a missing mapped file falls back to its remote URL. Empty maps produce no nonexistent local-GIF requests.

## GitHub Pages — after approval

Nothing has been published or pushed. **Get the owner's explicit approval before creating a public repository, pushing publicly or enabling public Pages hosting.**

After approval, upload/commit the contents of this folder to the repository's `main` branch at the root. `index.html`, `.nojekyll`, `data/`, `assets/` and the other site files must retain their relative locations. Do not put an extra enclosing folder around the site or upload host score/review exports.

In repository **Settings → Pages → Build and deployment → Source**, choose **Deploy from a branch**, **main**, **/(root)** and **Save**. Wait for deployment and open GitHub's displayed URL, normally `https://USERNAME.github.io/REPOSITORY/`. Run `review.html` again at that URL and check the actual host browser before the event. These steps follow [GitHub's publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site). A live Pages deployment has not been tested.

Answers, source links and the host pages can be inspected by anyone who can access the static site. `noindex` is not access control. Use synthetic team names; do not upload confidential workplace or attendee data. Saved names/scores stay in the host browser's localStorage. Remote GIF requests contact third-party providers; a complete permitted local-media setup avoids those requests when its files load.

## Files and editing

- `index.html`, `styles.css`, `app.js`: game; vanilla HTML/CSS/JavaScript.
- `review.html`, `review.js`: host preflight, private by convention, with spoilers.
- `data/questions.json`: canonical dataset; q01–q40 and round order remain stable.
- `data/questions.js`, `ANSWER_KEY.md`: regenerate after JSON changes with `python3 scripts/build_data.py`.
- `data/local-media.js`, `data/media-report.json`: local validation map/report.
- `HOST_GUIDE.md`: rules and separate 60-minute running order.
- `answer-sheet.html`: printable sheet without answers.
- `evidence/`: dated validation reports and fixture-interface screenshots.
- `CODEX_PROMPT.md`: original task specification; its initial media-status paragraph describes the starter, not the current delivery.

## Verification

Offline checks:

```sh
python3 scripts/build_data.py
node tests/validate.cjs
python3 tests/test_media.py
node --check app.js
node --check review.js
```

The current browser suites require Node.js, Playwright and Chromium for testing only. They do not add runtime dependencies to the site. If unavailable, install test tools outside the project:

```sh
npm install --prefix /tmp/gif-break-test-tools playwright
/tmp/gif-break-test-tools/node_modules/.bin/playwright install chromium
NODE_PATH=/tmp/gif-break-test-tools/node_modules node tests/ui_smoke.cjs
```

For an existing Chrome/Chromium installation, skip the browser-install command and set `CHROMIUM_EXECUTABLE=/absolute/path/to/browser` alongside `NODE_PATH`. The UI suite uses synthetic animations with real HTTP and localStorage, and writes `evidence/ui-test-results.json`.

Separate real-media checks (internet required):

```sh
python3 scripts/check_remote.py
NODE_PATH=/tmp/gif-break-test-tools/node_modules node tests/media_browser.cjs
```

The GET checker stores temporary inspection binaries outside the site and writes `evidence/remote-media-report.json`. Optional Pillow adds independent decoding of every frame; structural/LZW checking always runs. The browser suite uses actual remote GIFs and writes `evidence/browser-media-results.json`. Re-running automated checks never grants visual/venue approval; inspect changed media yourself. Older Python browser harnesses remain as legacy alternatives; the current report comes from the Node suites.
