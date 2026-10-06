/* No backend or framework. This is an honour-system shared-screen quiz, not secure multiplayer. */
'use strict';
(() => {
 const data=window.QUIZ_DATA, qs=data.questions, $=id=>document.getElementById(id), KEY='gif-break-state-v1';
 const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 let state=null, tick=null, deadline=0, ready=false, concealed=reduced, generation=0, mediaTimer=null, pendingImage=null;
 const ids=new Set(qs.map(q=>q.id)), isRecord=x=>Boolean(x)&&typeof x==='object'&&!Array.isArray(x);
 function getSaved(){try{
  const s=JSON.parse(localStorage.getItem(KEY));
  if(!isRecord(s)||s.version!==1||!Array.isArray(s.teams)||s.teams.length<2||s.teams.length>8||
   !s.teams.every(t=>typeof t==='string'&&t.trim()&&t.length<=40)||new Set(s.teams.map(t=>t.trim().toLowerCase())).size!==s.teams.length||
   !Number.isInteger(s.index)||s.index<0||s.index>=qs.length||![30,45,60,90].includes(s.seconds)||
   !Number.isFinite(s.remaining)||s.remaining<0||s.remaining>s.seconds||!Array.isArray(s.voids)||
   !s.voids.every(id=>ids.has(id))||new Set(s.voids).size!==s.voids.length||!isRecord(s.awards)||!isRecord(s.revealed))return null;
  for(const [id,awards] of Object.entries(s.awards))if(!ids.has(id)||!isRecord(awards)||!Object.entries(awards).every(([i,v])=>/^(0|[1-7])$/.test(i)&&Number(i)<s.teams.length&&typeof v==='boolean'))return null;
  for(const flags of [s.revealed,s.hints??{}])if(!isRecord(flags)||!Object.entries(flags).every(([id,v])=>ids.has(id)&&typeof v==='boolean'))return null;
  return {version:1,teams:s.teams.map(t=>t.trim()),seconds:s.seconds,remaining:s.remaining,index:s.index,awards:s.awards,revealed:s.revealed,hints:s.hints??{},voids:s.voids};
 }catch{}return null;}
 function persist(){try{if(state)localStorage.setItem(KEY,JSON.stringify(state));}catch{$('liveNotice').textContent='Browser storage is unavailable. Keep this tab open and export the scores.';}}
 function stop(){if(tick&&state)state.remaining=Math.max(0,(deadline-performance.now())/1000);clearInterval(tick);tick=null;renderTimer();}
 function renderTimer(){if(!state)return;const id=qs[state.index].id;$('timerValue').textContent=Math.max(0,Math.ceil(state.remaining));$('timerStatus').textContent=state.voids.includes(id)?'Question voided':state.revealed[id]?'Answer revealed':concealed?'Motion hidden':tick?'Thinking time':state.remaining<=0?'Pens down':ready?'Ready when you are':'Waiting for the clip';$('timerBtn').textContent=tick?'Pause timer':state.remaining<=0?'Reset timer':'Start timer';$('timerBtn').disabled=!ready||concealed||Boolean(state.revealed[id])||state.voids.includes(id);}
 function toggleTimer(){if(!state||!ready||concealed||document.hidden||state.revealed[qs[state.index].id]||state.voids.includes(qs[state.index].id))return;if(tick){stop();persist();return;}if(state.remaining<=0)state.remaining=state.seconds;deadline=performance.now()+state.remaining*1000;tick=setInterval(()=>{state.remaining=Math.max(0,(deadline-performance.now())/1000);if(state.remaining<=0){stop();$('liveNotice').textContent='Time is up. Pens down; the host can reveal the answer.';}renderTimer();persist();},150);renderTimer();persist();}
 function sources(q){return [...new Set([window.LOCAL_MEDIA?.[q.id]?.path,q.mediaUrl].filter(Boolean))];}
 function message(text){$('mediaStatus').textContent=text;$('mediaMessage').hidden=false;$('clip').hidden=true;}
 function loadClip(){
  if(!state)return;stop();persist();ready=false;const token=++generation,q=qs[state.index], urls=sources(q);clearTimeout(mediaTimer);if(pendingImage){pendingImage.onload=null;pendingImage.onerror=null;pendingImage.removeAttribute('src');pendingImage=null;}$('clip').removeAttribute('src');
  $('motionBtn').textContent=concealed?'Show motion':'Hide motion';renderTimer();
  if(concealed){message('Motion is hidden. Select Show motion when everyone is ready.');$('retryBtn').hidden=true;return;}
  $('retryBtn').hidden=true;message('Loading the mystery clip…');
  function attempt(i){if(token!==generation)return;if(i>=urls.length){message('This clip could not load. Retry, or void it fairly for all teams.');$('retryBtn').hidden=false;renderTimer();return;}
   const img=new Image();pendingImage=img;img.id='clip';img.referrerPolicy='no-referrer';let settled=false;
   const fail=()=>{if(settled||token!==generation)return;settled=true;clearTimeout(mediaTimer);img.onload=null;img.onerror=null;img.removeAttribute('src');attempt(i+1);};
   img.onload=()=>{if(settled||token!==generation)return;settled=true;clearTimeout(mediaTimer);pendingImage=null;ready=true;img.onload=null;img.onerror=null;$('clip').replaceWith(img);img.hidden=false;$('mediaMessage').hidden=true;renderTimer();};
   img.onerror=fail;mediaTimer=setTimeout(fail,18000);img.alt=`Mystery clip ${state.index+1}`;img.src=urls[i];
  }attempt(0);
 }
 function scores(){return state.teams.map((name,i)=>({name,index:i,points:Object.entries(state.awards).reduce((sum,[id,award])=>sum+(!state.voids.includes(id)&&award[i]?1:0),0)})).sort((a,b)=>b.points-a.points||a.index-b.index);}
 function scoreList(target){const root=$(target);root.replaceChildren();if(!state){root.textContent='Start a game to create the teams.';return;}const values=scores();values.forEach((s,i)=>{const row=document.createElement('div');row.className='score-row';const name=document.createElement('span'),points=document.createElement('span');const rank=1+values.filter(x=>x.points>s.points).length;name.textContent=`${rank}. ${s.name}`;points.className='points';points.textContent=`${s.points} / ${qs.length-state.voids.length}`;row.append(name,points);root.append(row);});}
 function renderAnswer(){const q=qs[state.index], revealed=Boolean(state.revealed[q.id]), isVoid=state.voids.includes(q.id);$('answerPanel').hidden=!revealed;
  $('answerText').textContent=revealed?q.answer:'';$('sceneText').textContent=revealed?q.scene:'';
  $('acceptedText').textContent=revealed&&q.acceptedAnswers.length>1?'Also accept: '+q.acceptedAnswers.slice(1).join(' · '):'';
  $('sourceLink').removeAttribute('href');if(revealed)$('sourceLink').href=q.sourceUrl;
  $('revealBtn').disabled=revealed;$('voidBtn').textContent=isVoid?'Restore question':'Void this question';$('awardButtons').replaceChildren();
  if(revealed)state.teams.forEach((name,i)=>{const b=document.createElement('button');b.textContent=name;b.disabled=isVoid;b.setAttribute('aria-pressed',String(Boolean(state.awards[q.id]?.[i])));b.addEventListener('click',()=>{state.awards[q.id]??={};state.awards[q.id][i]=!state.awards[q.id][i];persist();renderAnswer();});$('awardButtons').append(b);});renderTimer();
 }
 function render(){const q=qs[state.index],r=data.rounds[q.round-1];$('roundLabel').textContent=`Round ${q.round} / ${r.title} / ${state.index+1} of ${qs.length}`;$('questionLabel').textContent=q.id==='q30'?'Which video game is this from?':q.round===4?'Which TV series is this?':'Which movie or source?';$('questionType').textContent=state.voids.includes(q.id)?'VOID — no points for any team':q.id==='q30'?'VIDEO-GAME WILDCARD':'';$('hintText').textContent=state.hints?.[q.id]?q.hint:'';$('progressFill').style.width=`${(state.index+1)/qs.length*100}%`;$('prevBtn').disabled=state.index===0;$('nextBtn').textContent=state.index===qs.length-1?'Final scores →':'Next →';$('liveNotice').textContent='';renderAnswer();loadClip();persist();}
 function showGame(){ $('welcome').hidden=true;$('finish').hidden=true;$('game').hidden=false;render();window.scrollTo(0,0);}
 function start(){const teams=$('teamNames').value.split('\n').map(x=>x.trim().slice(0,40)).filter(Boolean);if(teams.length<2||teams.length>8){$('setupError').textContent='Please enter between 2 and 8 team names.';return;}if(new Set(teams.map(t=>t.toLowerCase())).size!==teams.length){$('setupError').textContent='Give every team a different name.';return;}if(getSaved()&&!confirm('Start a new game and replace the saved progress?'))return;state={version:1,teams,seconds:Number($('seconds').value),remaining:Number($('seconds').value),index:0,awards:{},revealed:{},hints:{},voids:[]};showGame();}
 function move(delta){if(!state||state.index+delta<0)return;stop();if(state.index+delta>=qs.length){finish();return;}state.index+=delta;state.remaining=state.seconds;concealed=reduced;render();window.scrollTo(0,0);}
 function reveal(){if(!state)return;stop();state.revealed[qs[state.index].id]=true;persist();renderAnswer();}
 function hint(){if(!state)return;state.hints??={};state.hints[qs[state.index].id]=true;$('hintText').textContent=qs[state.index].hint;persist();}
 function motion(){concealed=!concealed;loadClip();}
 function finish(){stop();persist();clearTimeout(mediaTimer);generation++;if(pendingImage){pendingImage.onload=null;pendingImage.onerror=null;pendingImage.removeAttribute('src');pendingImage=null;}$('clip').removeAttribute('src');$('game').hidden=true;$('finish').hidden=false;scoreList('finalScores');window.scrollTo(0,0);}
 function exportScores(){if(!state)return;const payload={exportedAt:new Date().toISOString(),scores:scores(),voidedQuestions:state.voids,game:state};const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='gif-break-scores.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
 data.rounds.forEach(r=>{const article=document.createElement('article');article.className='round-card';const n=document.createElement('span'),h=document.createElement('h2'),p=document.createElement('p');n.className='number';n.textContent=`ROUND 0${r.id} / 10 CLIPS`;h.textContent=r.title;p.textContent=r.subtitle;article.append(n,h,p);$('roundCards').append(article);});
 $('resumeBtn').hidden=!getSaved();$('startBtn').onclick=start;$('resumeBtn').onclick=()=>{state=getSaved();if(state)showGame();};$('timerBtn').onclick=toggleTimer;$('retryBtn').onclick=loadClip;$('motionBtn').onclick=motion;$('prevBtn').onclick=()=>move(-1);$('nextBtn').onclick=()=>move(1);$('hintBtn').onclick=hint;$('revealBtn').onclick=reveal;$('finishBtn').onclick=finish;$('backGameBtn').onclick=showGame;$('exportBtn').onclick=exportScores;
 $('voidBtn').onclick=()=>{const id=qs[state.index].id;if(state.voids.includes(id)){state.voids=state.voids.filter(x=>x!==id);}else{if(!confirm('Void this question for every team? It will not count toward the maximum score.'))return;state.voids.push(id);stop();}persist();renderAnswer();$('questionType').textContent=state.voids.includes(id)?'VOID — no points for any team':id==='q30'?'VIDEO-GAME WILDCARD':'';};
 $('newBtn').onclick=()=>{if(!confirm('Return to setup? A new game will replace saved progress only when started.'))return;$('finish').hidden=true;$('welcome').hidden=false;$('resumeBtn').hidden=false;};
 $('scoresBtn').onclick=()=>{stop();persist();scoreList('scoreList');$('scoresDialog').showModal();};$('closeScoresBtn').onclick=()=>$('scoresDialog').close();
 $('fullscreenBtn').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{$('fullscreenBtn').textContent='Use browser full screen';}};
 document.addEventListener('visibilitychange',()=>{if(document.hidden){stop();persist();}});
 window.addEventListener('pagehide',()=>{stop();persist();});
 document.addEventListener('keydown',e=>{if(!state||$('game').hidden||$('scoresDialog').open||e.repeat||e.ctrlKey||e.metaKey||e.altKey||/INPUT|TEXTAREA|SELECT/.test(e.target.tagName)||e.target.isContentEditable)return;if(e.key===' '&&e.target.closest('button,a,[role="button"]'))return;const handlers={' ':toggleTimer,r:reveal,h:hint,ArrowRight:()=>move(1),ArrowLeft:()=>move(-1),m:motion};const fn=handlers[e.key]||handlers[e.key.toLowerCase()];if(fn){e.preventDefault();fn();}});
})();
