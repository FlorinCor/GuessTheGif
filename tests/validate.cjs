'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..'),d=JSON.parse(fs.readFileSync(path.join(root,'data/questions.json'),'utf8'));
assert.equal(d.questions.length,100);assert.equal(d.rounds.length,10);
assert.deepEqual(d.questions.map(q=>q.id),Array.from({length:100},(_,i)=>'q'+String(i+1).padStart(2,'0')));
assert.equal(new Set(d.questions.map(q=>q.mediaUrl)).size,100);
for(const q of d.questions){assert.equal(q.round,Math.floor((Number(q.id.slice(1))-1)/10)+1);assert.ok(q.answer.length);assert.ok(q.acceptedAnswers.includes(q.answer));assert.equal(new URL(q.mediaUrl).protocol,'https:');assert.equal(new URL(q.sourceUrl).protocol,'https:');assert.ok(q.hint);assert.equal(q.localPath,`assets/gifs/${q.id}.gif`);}
const context={window:{}};vm.runInNewContext(fs.readFileSync(path.join(root,'data/questions.js'),'utf8'),context);assert.equal(JSON.stringify(context.window.QUIZ_DATA),JSON.stringify(d));
for(const f of ['index.html','review.html','answer-sheet.html']){const s=fs.readFileSync(path.join(root,f),'utf8');assert.ok(!/(?:src|href)="\//.test(s));for(const [,asset] of s.matchAll(/(?:src|href)="([^"#]+\.(?:js|css))"/g))assert.ok(fs.existsSync(path.join(root,asset)),asset);}
assert.ok(fs.existsSync(path.join(root,'.nojekyll')),'GitHub Pages must retain .nojekyll');
const local={window:{}};vm.runInNewContext(fs.readFileSync(path.join(root,'data/local-media.js'),'utf8'),local);
for(const [id,media] of Object.entries(local.window.LOCAL_MEDIA)){assert.ok(d.questions.some(q=>q.id===id));assert.equal(media.path,`assets/gifs/${id}.gif`);assert.ok(fs.existsSync(path.join(root,media.path)));assert.ok(media.frames>=2);}
assert.ok(d.questions[13].acceptedAnswers.includes('Finding Nemo')&&d.questions[13].acceptedAnswers.includes('Finding Dory'));
assert.equal(d.questions[29].kind,'video game');assert.ok(d.questions[29].acceptedAnswers.includes('Red Alert'));
assert.ok(d.questions[38].acceptedAnswers.includes('Wednesday')&&d.questions[38].acceptedAnswers.includes('Mercredi'));
assert.ok(!d.questions[39].acceptedAnswers.includes('Baby Yoda'));
console.log('PASS: 100 unique questions/media URLs; round/alias/source/path checks; generated data matches; local map, relative assets and Pages marker validate.');

assert.equal(d.questionCount,100);assert.equal(d.questions[99].id,'q100');assert.equal(d.questions[99].kind,'TV series');
