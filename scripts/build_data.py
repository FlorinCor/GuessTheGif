#!/usr/bin/env python3
"""Validate canonical questions and generate browser data, host key and printable sheets."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'data/questions.json').read_text())
qs = data['questions']
count = data.get('questionCount', len(qs))
assert len(qs) == count and count > 0, 'Question count must match the dataset'
assert [q['id'] for q in qs] == [f'q{i:02}' for i in range(1, count + 1)], 'IDs/order must be consecutive'
assert len({q['mediaUrl'] for q in qs}) == count, 'Media URLs must be unique'
assert [r['id'] for r in data['rounds']] == list(range(1, len(data['rounds']) + 1))
for q in qs:
    assert q['answer'] in q['acceptedAnswers'] and q['hint'] and q['scene']
    assert q['round'] == (int(q['id'][1:]) - 1) // 10 + 1
    assert q['round'] <= len(data['rounds'])
    assert q['mediaUrl'].startswith('https://') and q['sourceUrl'].startswith('https://')
    assert q['localPath'] == f"assets/gifs/{q['id']}.gif"
    assert q['kind'] in ('film / film franchise', 'video game', 'TV series')
(ROOT / 'data/questions.js').write_text('// Generated from questions.json. Do not edit by hand.\nwindow.QUIZ_DATA = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n')
validated = sum(q.get('verification', {}).get('remoteAnimationValidated', False) for q in qs)
screened = sum(q.get('verification', {}).get('allFramesScreened', False) for q in qs)
lines = ['# The GIF Break — host answer key', '', '**Spoilers. Keep this off the audience display.**', '',
    f"{count} selections in {len(data['rounds'])} rounds. Media record: {validated}/{count} remote animations validated; {screened}/{count} frame sequences screened. No third-party GIFs are bundled. See evidence/VALIDATION.md for dated checks and venue cautions; host approvals are recorded separately in review.html.", '',
    'One point per correct source. Accept the aliases below and equivalent localized titles. For franchise entries, do not demand a sequel title that the source evidence does not establish. TV entries require the series; character names count only when explicitly listed as an accepted source title.', '']
for r in data['rounds']:
    lines += [f"## Round {r['id']} — {r['title']}", '', '| # | Answer | Scene / recognition cue |', '|---|---|---|']
    for q in qs:
        if q['round'] == r['id']:
            lines.append(f"| {int(q['id'][1:])} | {q['answer']} | {q['scene']} |")
    lines.append('')
lines += ['## Full media and acceptance details', '']
for q in qs:
    lines += [f"### {q['id'][1:]} — {q['answer']}", '', f"**Accept:** {'; '.join(q['acceptedAnswers'])}.", f"**Hint:** {q['hint']}", f"**Source page:** {q['sourceUrl']}", f"**Direct GIF:** {q['mediaUrl']}", f"**Local filename:** `{q['localPath']}`", f"**URL evidence:** {q['mediaUrlMethod']}.", f"**Review:** {q['reviewNote'] or 'Watch the full loop and check captions, source and suitability.'}", '']
(ROOT / 'ANSWER_KEY.md').write_text('\n'.join(lines) + '\n')

# Forty spaces per A4 page keeps the existing readable two-column layout.
pages = [qs[i:i + 40] for i in range(0, count, 40)]
rounds = {r['id']: r for r in data['rounds']}
parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>The GIF Break — team answer sheet</title><link rel="stylesheet" href="styles.css"></head><body class="print-body"><button onclick="window.print()">Print these sheets</button>']
for i, page in enumerate(pages):
    parts += ['<section class="print-page"><h1>The GIF Break</h1>', f'<div class="sheet-top"><span>Team: __________________________</span><span>Page {i + 1} / {len(pages)} · Questions {page[0]["id"][1:]}–{page[-1]["id"][1:]}</span></div>', '<p class="small">One source per clip. Equivalent translated titles are welcome. No searching. Question 30 is a video-game wildcard.</p><div class="answer-grid">']
    split = (len(page) + 1) // 2
    for column in [page[:split], page[split:]]:
        parts.append('<div>')
        for rid in dict.fromkeys(q['round'] for q in column):
            parts += [f'<h2 class="sheet-round">Round {rid} — {escape(rounds[rid]["title"])}</h2><table><tbody>']
            for q in column:
                if q['round'] == rid:
                    parts.append(f'<tr><td>{q["id"][1:]}</td><td>_________________________________</td></tr>')
            parts.append('</tbody></table>')
        parts.append('</div>')
    parts.append('</div><p class="small">Final score: _____ / _____</p></section>')
parts.append('</body></html>')
(ROOT / 'answer-sheet.html').write_text('\n'.join(parts) + '\n')
print(f'Validated {count} questions; rebuilt questions.js, ANSWER_KEY.md and {len(pages)} printable pages.')
