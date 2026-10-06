#!/usr/bin/env python3
"""Check local animated GIFs and optionally download listed direct URLs.
No scraping, API keys, credential handling, access-control bypass or licence claims.
Python 3.9+; standard library only. Run --help for options.
"""
import argparse, hashlib, json, struct, sys, time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]

def lzw_pixels(payload, minimum, expected):
    """Validate the LZW stream and decoded pixel count without allocating pixels."""
    if not 2 <= minimum <= 8:raise ValueError('Invalid LZW minimum code size')
    clear=1<<minimum;end=clear+1;lengths=list([1]*clear)+[0,0]+[0]*(4096-clear-2)
    size=minimum+1;next_code=end+1;previous=None;count=0;bits=0;buffer=0;offset=0
    while True:
        while bits<size:
            if offset>=len(payload):raise ValueError('Truncated LZW stream: missing end code')
            buffer|=payload[offset]<<bits;bits+=8;offset+=1
        code=buffer&((1<<size)-1);buffer>>=size;bits-=size
        if code==clear:
            size=minimum+1;next_code=end+1;previous=None;continue
        if code==end:
            if count!=expected:raise ValueError('Incomplete GIF frame pixels')
            return
        if code<next_code:current=lengths[code]
        elif code==next_code and previous is not None:current=previous+1
        else:raise ValueError('Invalid GIF LZW code')
        count+=current
        if count>expected:raise ValueError('Excess GIF frame pixels')
        if previous is not None and next_code<4096:
            lengths[next_code]=previous+1;next_code+=1
            if next_code==(1<<size) and size<12:size+=1
        previous=current

def gif_info(raw):
    """Parse GIF block structure and count actual image frames (not header alone)."""
    if len(raw)<14 or raw[:6] not in (b'GIF87a', b'GIF89a'): raise ValueError('Not a GIF file (possibly an HTML error page)')
    width,height=struct.unpack_from('<HH',raw,6)
    if width<2 or height<2: raise ValueError('Unusable dimensions')
    p=13+(3*(2**((raw[10]&7)+1)) if raw[10]&128 else 0)
    if p>len(raw):raise ValueError('Truncated global colour table')
    frames=0; duration=0; trailer=False;delay=0
    def skip_blocks(pos, collect=False):
        chunks=[]
        while True:
            if pos>=len(raw): raise ValueError('Truncated GIF sub-block')
            size=raw[pos];pos+=1
            if not size:return (pos,b''.join(chunks)) if collect else pos
            if collect:chunks.append(raw[pos:pos+size])
            pos+=size
            if pos>len(raw):raise ValueError('Truncated GIF payload')
    while p<len(raw):
        block=raw[p];p+=1
        if block==0x3b: trailer=True;break
        if block==0x21:
            if p>=len(raw):raise ValueError('Truncated GIF extension')
            label=raw[p];p+=1
            if label==0xf9:
                if p+6>len(raw) or raw[p]!=4 or raw[p+5]!=0:raise ValueError('Invalid graphic control extension')
                delay=struct.unpack_from('<H',raw,p+2)[0]/100
            p=skip_blocks(p)
        elif block==0x2c:
            if p+9>len(raw):raise ValueError('Truncated image descriptor')
            left,top,fw,fh=struct.unpack_from('<HHHH',raw,p)
            if not fw or not fh or left+fw>width or top+fh>height:raise ValueError('Invalid GIF frame dimensions')
            packed=raw[p+8];p+=9
            if packed&128:p+=3*(2**((packed&7)+1))
            if p>=len(raw):raise ValueError('Truncated image colour table or LZW code size')
            minimum=raw[p];p+=1
            p,payload=skip_blocks(p,True)
            lzw_pixels(payload,minimum,fw*fh);frames+=1;duration+=delay;delay=0
        else:raise ValueError(f'Invalid GIF block 0x{block:02x}')
    if not trailer:raise ValueError('Missing GIF trailer')
    if frames<2:raise ValueError('Not animated: fewer than 2 image frames')
    return dict(width=width,height=height,frames=frames,durationSeconds=round(duration,2),bytes=len(raw))

def local_path(q):
    path=(ROOT/q['localPath']).resolve()
    if ROOT not in path.parents:raise ValueError('Unsafe local path')
    return path

def fetch(q,max_bytes,timeout):
    url=q['mediaUrl'];host=urlparse(url).hostname or ''
    if urlparse(url).scheme!='https' or not any(host==d or host.endswith('.'+d) for d in ('tenor.com','giphy.com','gifdb.com')):raise ValueError('Only listed HTTPS media-provider hosts are allowed')
    request=Request(url,headers={'User-Agent':'GIFBreak-MediaCheck/1.0','Accept':'image/gif'})
    with urlopen(request,timeout=timeout) as res:
        if res.status!=200:raise ValueError(f'HTTP {res.status}')
        final=urlparse(res.geturl())
        if final.scheme!='https' or not any(final.hostname==d or (final.hostname or '').endswith('.'+d) for d in ('tenor.com','giphy.com','gifdb.com')):raise ValueError('Unexpected redirect outside the listed providers')
        length=int(res.headers.get('Content-Length') or 0)
        if length>max_bytes:raise ValueError(f'File too large: {length} bytes')
        raw=res.read(max_bytes+1)
        if length and len(raw)!=length:raise ValueError('Truncated response: Content-Length mismatch')
    if len(raw)>max_bytes:raise ValueError('Download exceeds size limit')
    info=gif_info(raw)
    path=local_path(q);path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix('.part');temp.write_bytes(raw);temp.replace(path)
    return info

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download',action='store_true',help='Download the specific direct GIF URLs (otherwise scan local files only)')
    parser.add_argument('--rights-reviewed',action='store_true',help='Confirm you have reviewed and have the necessary permission for the intended downloads/use; this flag does not grant permission')
    parser.add_argument('--id',action='append',dest='ids',help='Download only this ID, e.g. --id q01; repeatable')
    parser.add_argument('--max-mb',type=int,default=50,help='Per-file limit; default 50 MiB')
    parser.add_argument('--timeout',type=int,default=25)
    args=parser.parse_args()
    if args.download and not args.rights_reviewed:parser.error('Review rights and provider terms first, then add --rights-reviewed when appropriate.')
    qs=json.loads((ROOT/'data/questions.json').read_text())['questions'];errors={}
    known={q['id'] for q in qs}
    if args.ids and set(args.ids)-known:parser.error('Unknown question ID')
    if args.download:
        for q in qs:
            if args.ids and q['id'] not in args.ids:continue
            path=local_path(q)
            if path.exists():
                try:gif_info(path.read_bytes());print(q['id'],'existing valid GIF');continue
                except ValueError:pass
            try:info=fetch(q,args.max_mb*1024*1024,args.timeout);print(q['id'],'downloaded',info['bytes'],'bytes')
            except Exception as exc:errors[q['id']]=str(exc);print(q['id'],'FAILED',exc,file=sys.stderr)
            time.sleep(.2)
    report=[];mapping={}
    for q in qs:
        row={'id':q['id'],'sourceUrl':q['sourceUrl'],'mediaUrl':q['mediaUrl'],'visualReviewRequired':True,'rightsClearedByThisTool':False}
        try:
            path=local_path(q)
            if not path.exists():raise FileNotFoundError('Local GIF missing')
            if path.stat().st_size>args.max_mb*1024*1024:raise ValueError('Local GIF exceeds size limit')
            info=gif_info(path.read_bytes());row.update(status='local-animation-validated',**info)
            row['warnings']=[]
            if info['bytes']>8*1024*1024:row['warnings'].append('Large file: optimize or replace for slower connections')
            if info['width']<400:row['warnings'].append('Low width: inspect projector legibility')
            mapping[q['id']]={'path':q['localPath'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),**info}
        except Exception as exc:row.update(status='not-validated',error=errors.get(q['id'],str(exc)))
        report.append(row)
    out={'checkedAt':datetime.now(timezone.utc).isoformat(),'localAnimationsValidated':len(mapping),'total':len(qs),'visualReviewStillRequired':True,'questions':report}
    (ROOT/'data/local-media.js').write_text('// Generated after GIF structure validation. Not a visual/content approval.\nwindow.LOCAL_MEDIA = '+json.dumps(mapping,indent=2)+';\n')
    (ROOT/'data/media-report.json').write_text(json.dumps(out,indent=2)+'\n')
    print(f'{len(mapping)}/{len(qs)} local animated GIFs validated. See data/media-report.json.')
    return 0 if len(mapping)==len(qs) else 1
if __name__=='__main__':sys.exit(main())
