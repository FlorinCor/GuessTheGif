#!/usr/bin/env python3
"""Read the current public source/media pairs for validation, without bundling copies.

GETs (not HEADs) are required: some providers return 404 for HEAD on working GIFs.
Temporary media stays outside the static project, for private content inspection.
This check does not grant redistribution rights or automatically approve content.
Optional Pillow validates decoding of every frame. Standard library otherwise.
"""
import argparse
import concurrent.futures
import hashlib
import json
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from media import ROOT, gif_info


def request(url, path, timeout):
    if urlparse(url).scheme != 'https':
        raise ValueError('HTTPS required')
    result = subprocess.run(['curl', '--silent', '--show-error', '--location',
        '--max-time', str(timeout), '--max-filesize', str(50 * 1024 * 1024),
        '--proto', '=https', '--proto-redir', '=https', '--output', str(path),
        '--write-out', '%{http_code}', url], capture_output=True, text=True)
    code = int(result.stdout or 0)
    if result.returncode or code != 200:
        raise ValueError(f'HTTP {code}: {result.stderr.strip() or "request failed"}')


def check(q, directory, timeout):
    row = {'id': q['id'], 'sourceUrl': q['sourceUrl'], 'mediaUrl': q['mediaUrl'],
           'visualApproval': False, 'rightsCleared': False}
    source = directory / (q['id'] + '.html')
    try:
        request(q['sourceUrl'], source, timeout)
        html = source.read_text(errors='replace')
        row['sourceStatus'] = 'read'
        row['advertisedGifUrls'] = list(dict.fromkeys(re.findall(
            r'https://(?:media[^/]*\.tenor\.com|[^/]*giphy\.com|gifdb\.com)/[^\s"<>]+\.gif', html)))[:30]
    except Exception as exc:
        row.update(sourceStatus='failed', sourceError=str(exc))
    target = directory / (q['id'] + '.gif')
    try:
        request(q['mediaUrl'], target, timeout)
        raw = target.read_bytes()
        row.update(gif_info(raw))
        row['sha256'] = hashlib.sha256(raw).hexdigest()
        try:
            from PIL import Image
        except ImportError:
            row['decodedAllFrames'] = False
        else:
            with Image.open(target) as gif:
                for i in range(gif.n_frames):
                    gif.seek(i)
                    gif.load()
                row['decodedAllFrames'] = True
        row['mediaStatus'] = 'animated-gif-validated'
    except Exception as exc:
        row.update(mediaStatus='failed', mediaError=str(exc))
        target.unlink(missing_ok=True)
    print(q['id'], row['mediaStatus'], row.get('mediaError', f"{row.get('width')}x{row.get('height')}; {row.get('frames')} frames; {row.get('bytes')} bytes"), flush=True)
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inspection-dir', type=Path, help='Temporary folder OUTSIDE this project for private inspection')
    parser.add_argument('--timeout', type=int, default=45)
    parser.add_argument('--id', action='append', dest='ids')
    args = parser.parse_args()
    directory = (args.inspection_dir or Path(tempfile.mkdtemp(prefix='gif-break-inspection-'))).resolve()
    if directory == ROOT or ROOT in directory.parents:
        parser.error('Inspection binaries must stay outside the publishable project')
    directory.mkdir(parents=True, exist_ok=True)
    qs = json.loads((ROOT / 'data/questions.json').read_text())['questions']
    if args.ids:
        if set(args.ids) - {q['id'] for q in qs}:
            parser.error('Unknown question ID')
        qs = [q for q in qs if q['id'] in args.ids]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(lambda q: check(q, directory, args.timeout), qs))
    report = {'checkedAt': datetime.now(timezone.utc).isoformat(), 'method': 'public HTTPS GET; temporary inspection only',
              'total': len(rows), 'animatedGifsValidated': sum(r['mediaStatus'] == 'animated-gif-validated' for r in rows),
              'visuallyApproved': 0, 'inspectionDirectory': str(directory), 'questions': rows}
    (ROOT / 'evidence/remote-media-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f"{report['animatedGifsValidated']}/{len(rows)} animated GIFs. Inspection files: {directory}")
    return 0 if report['animatedGifsValidated'] == len(rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())
