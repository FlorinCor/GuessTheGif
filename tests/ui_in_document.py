from pathlib import Path
import re,base64,json
from playwright.sync_api import sync_playwright,expect
R=Path(__file__).resolve().parents[1]
# In-document harness: Chromium policy blocks localhost/file navigation in this environment.
# Media and storage are explicitly synthetic; tests do not establish real media or real persistence.
raw=b'GIF89a\x02\x00\x02\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff'+b'\x21\xf9\x04\x00\x0a\x00\x00\x00\x2c\x00\x00\x00\x00\x02\x00\x02\x00\x00\x02\x03\x44\x02\x05\x00'*2+b'\x3b'
uri='data:image/gif;base64,'+base64.b64encode(raw).decode()
def load(page,file='index.html',saved=None,fail=False):
 text=(R/file).read_text();text=re.sub(r'<script\b[^>]*>.*?</script>','',text);text=re.sub(r'<link[^>]+stylesheet[^>]+>','',text)
 page.set_content(text);page.add_style_tag(content=(R/'styles.css').read_text())
 page.evaluate('''seed => {window.mockStorage=seed||{};Object.defineProperty(window,'localStorage',{value:{getItem:k=>window.mockStorage[k]||null,setItem:(k,v)=>{window.mockStorage[k]=v}}});}''',saved)
 page.add_script_tag(content=(R/'data/questions.js').read_text())
 page.evaluate('u=>{window.QUIZ_DATA.questions.forEach(q=>q.mediaUrl=u);window.LOCAL_MEDIA={};}', 'data:image/gif;base64,AAAA' if fail else uri)
 page.add_script_tag(content=(R/('review.js' if file=='review.html' else 'app.js')).read_text())
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 c=b.new_context(viewport={'width':1440,'height':1000});page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));load(page)
 expect(page.locator('.round-card')).to_have_count(4);page.screenshot(path=str(R/'evidence/setup-desktop.png'),full_page=True)
 page.locator('#startBtn').click();expect(page.locator('#clip')).to_be_visible();expect(page.locator('#timerValue')).to_have_text('45');assert page.locator('#answerText').text_content()==''
 page.locator('#timerBtn').click();page.wait_for_timeout(1250);page.locator('#timerBtn').click();assert int(page.locator('#timerValue').inner_text())<45
 page.locator('#hintBtn').click();expect(page.locator('#hintText')).not_to_be_empty();page.locator('#revealBtn').click();expect(page.locator('#answerText')).to_have_text('The Matrix')
 award=page.locator('#awardButtons button').first;award.click();expect(award).to_have_attribute('aria-pressed','true');award.click();expect(award).to_have_attribute('aria-pressed','false');award.click()
 page.locator('#nextBtn').click();expect(page.locator('#answerPanel')).to_be_hidden();page.locator('#prevBtn').click();expect(page.locator('#awardButtons button').first).to_have_attribute('aria-pressed','true')
 page.once('dialog',lambda d:d.accept());page.locator('#voidBtn').click();page.locator('#scoresBtn').click();assert '0 / 39' in page.locator('#scoreList').inner_text();page.locator('#closeScoresBtn').click();page.locator('#voidBtn').click();page.locator('#scoresBtn').click();assert '1 / 40' in page.locator('#scoreList').inner_text();page.locator('#closeScoresBtn').click()
 results.append('In-document harness: setup, timer start/pause, reveal, hint, reversible awards, revisits, void/restore and score display passed.')
 saved=page.evaluate('window.mockStorage');page.close();page=c.new_page();load(page,saved=saved);page.locator('#resumeBtn').click();expect(page.locator('#awardButtons button').first).to_have_attribute('aria-pressed','true');results.append('Saved-state serialization/resume passed with an in-memory storage shim; not a real browser-storage test.')
 for i in range(2,41):page.locator('#nextBtn').click();expect(page.locator('#roundLabel')).to_contain_text(f'{i} of 40')
 page.locator('#nextBtn').click();expect(page.locator('#finish')).to_be_visible();results.append('All 40 navigation positions and final scores passed with synthetic GIFs.')
 mob=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');mp=mob.new_page();load(mp);assert mp.evaluate('document.documentElement.scrollWidth<=innerWidth');mp.screenshot(path=str(R/'evidence/setup-mobile.png'),full_page=True);mp.locator('#startBtn').click();expect(mp.locator('#clip')).to_be_hidden();expect(mp.locator('#timerBtn')).to_be_disabled();mp.locator('#motionBtn').click();expect(mp.locator('#clip')).to_be_visible();assert mp.evaluate('document.documentElement.scrollWidth<=innerWidth');results.append('390px layout and reduced-motion opt-in passed.')
 fp=c.new_page();load(fp,fail=True);fp.locator('#startBtn').click();expect(fp.locator('#mediaStatus')).to_contain_text('could not load');expect(fp.locator('#timerBtn')).to_be_disabled();results.append('Invalid-media failure state and disabled timer passed.')
 rp=c.new_page();load(rp,'review.html');expect(rp.locator('.review-item')).to_have_count(40);rp.locator('#checkAll').click();expect(rp.locator('#checkProgress')).to_contain_text('Checked 40 / 40');assert '0 / 40 visually approved' in rp.locator('#reviewSummary').inner_text();results.append('Preflight checked all 40 synthetic images without automatically granting visual approval.')
 assert not errors,errors;b.close()
(R/'evidence/ui-test-results.json').write_text(json.dumps({'mode':'in-document-harness','syntheticMedia':True,'syntheticStorage':True,'realMediaValidated':False,'passed':results},indent=2)+'\n')
print('\n'.join(results))
