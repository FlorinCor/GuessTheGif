/* Actual remote GIFs in the player over HTTP. No fixtures and no approvals. */
'use strict';
const {chromium}=require('playwright'),{expect}=require('playwright/test');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),crypto=require('node:crypto');
const ROOT=path.resolve(__dirname,'..'),DATA=JSON.parse(fs.readFileSync(path.join(ROOT,'data/questions.json')));
const audit=JSON.parse(fs.readFileSync(path.join(ROOT,'evidence/remote-media-report.json'))),rows=[],errors=[];
const server=http.createServer((req,res)=>{const name=new URL(req.url,'http://localhost').pathname.replace(/^\/repository-name\//,'/');const file=path.resolve(ROOT,'.'+(name.endsWith('/')?name+'index.html':name));if(!file.startsWith(ROOT+path.sep)){res.writeHead(403).end();return;}fs.readFile(file,(e,b)=>{if(e){res.writeHead(404).end();return;}res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css'})[path.extname(file)]||'application/octet-stream');res.end(b);});});
let browser;
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}/repository-name/`;
 browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_EXECUTABLE?{executablePath:process.env.CHROMIUM_EXECUTABLE}:{})});let next=0;
 async function worker(){
  while(next<DATA.questions.length){const index=next++,q=DATA.questions[index],meta=audit.questions.find(r=>r.id===q.id);const context=await browser.newContext({viewport:{width:1440,height:900}}),p=await context.newPage();p.on('pageerror',e=>errors.push(e.message));
   const row={id:q.id,mediaUrl:q.mediaUrl,fixture:false};
   try{
    await context.addInitScript(s=>{if(location.protocol==='http:')localStorage.setItem('gif-break-state-v1',JSON.stringify(s));},{version:1,teams:['Test A','Test B'],index,seconds:45,remaining:45,voids:[],awards:{},revealed:{},hints:{}});
    const started=Date.now();await p.goto(base);await p.locator('#resumeBtn').click();await expect(p.locator('#clip')).toBeVisible({timeout:30000});row.loadMilliseconds=Date.now()-started;
    const clip=p.locator('#clip');row.dimensions=await clip.evaluate(img=>[img.naturalWidth,img.naturalHeight]);const hashes=[];
    // Spend at least a complete decoded loop in the actual browser and compare pixels.
    const loop=Math.max(1000,meta.durationSeconds*1000);
    for(let i=0;i<4;i++){hashes.push(crypto.createHash('sha256').update(await clip.screenshot()).digest('hex'));await p.waitForTimeout(loop/4+70);}
    row.observedMilliseconds=loop+280;row.changingPixels=new Set(hashes).size>1;row.pixelHashes=hashes;
    if(!row.changingPixels)throw new Error('No pixel change observed across a loop');
    await expect(p.locator('#timerValue')).toHaveText('45');await expect(p.locator('#answerPanel')).toBeHidden();row.status='real-browser-animation-passed';
   }catch(e){row.status='failed';row.error=e.message;process.exitCode=1;}
   rows.push(row);console.log(q.id,row.status,row.dimensions||row.error);await context.close();
  }
 }
 await Promise.all(Array.from({length:4},worker));rows.sort((a,b)=>a.id.localeCompare(b.id));
 fs.writeFileSync(path.join(ROOT,'evidence/browser-media-results.json'),JSON.stringify({checkedAt:new Date().toISOString(),mode:'real-remote-media-http-nested-path',syntheticMedia:false,passed:rows.filter(r=>r.status==='real-browser-animation-passed').length,total:40,pageErrors:errors,questions:rows},null,2)+'\n');
 if(errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();await new Promise(r=>server.close(r));});
