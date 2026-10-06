"""Browser smoke tests with synthetic GIF responses. NOT a real-media/content check.
Needs Python Playwright and Chromium. No network downloads performed.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import functools,threading,os,shutil,json,tempfile
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
GIF=(b'GIF89a\x02\x00\x02\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff'+
 b'\x21\xf9\x04\x00\x0a\x00\x00\x00\x2c\x00\x00\x00\x00\x02\x00\x02\x00\x00\x02\x03\x44\x02\x05\x00'*2+b'\x3b')
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT.parent)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}/{ROOT.name}/'
results=[]
try:
 with sync_playwright() as p:
  exe=os.getenv('CHROMIUM_EXECUTABLE') or shutil.which('chromium')
  opts={'headless':True,'args':['--no-sandbox']}
  if exe:opts['executable_path']=exe
  browser=p.chromium.launch(**opts)
  context=browser.new_context(viewport={'width':1440,'height':1000})
  context.route('https://**/*',lambda route:route.fulfill(status=200,content_type='image/gif',body=GIF) if route.request.resource_type=='image' else route.abort())
  page=context.new_page();errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto(base);expect(page.locator('.round-card')).to_have_count(4)
  page.screenshot(path=str(ROOT/'evidence/setup-desktop.png'),full_page=True)
  page.locator('#startBtn').click();expect(page.locator('#clip')).to_be_visible();expect(page.locator('#timerValue')).to_have_text('45')
  assert page.locator('#answerText').text_content()=='' and page.locator('#sourceLink').get_attribute('href') is None
  page.locator('#timerBtn').click();page.wait_for_timeout(1250);page.locator('#timerBtn').click();assert int(page.locator('#timerValue').inner_text())<45
  paused=page.locator('#timerValue').inner_text();page.wait_for_timeout(300);assert page.locator('#timerValue').inner_text()==paused
  page.locator('#hintBtn').click();expect(page.locator('#hintText')).not_to_be_empty()
  page.locator('#revealBtn').click();expect(page.locator('#answerText')).to_have_text('The Matrix')
  award=page.locator('#awardButtons button').first;award.click();expect(award).to_have_attribute('aria-pressed','true');award.click();expect(award).to_have_attribute('aria-pressed','false');award.click()
  page.locator('#nextBtn').click();expect(page.locator('#answerPanel')).to_be_hidden();page.locator('#prevBtn').click();expect(page.locator('#awardButtons button').first).to_have_attribute('aria-pressed','true')
  page.once('dialog',lambda dialog:dialog.accept());page.locator('#voidBtn').click();assert 'VOID' in page.locator('#questionType').inner_text();page.locator('#scoresBtn').click();assert '0 / 39' in page.locator('#scoreList').inner_text();page.locator('#closeScoresBtn').click()
  page.locator('#voidBtn').click();page.locator('#scoresBtn').click();assert '1 / 40' in page.locator('#scoreList').inner_text();page.locator('#closeScoresBtn').click()
  page.reload();page.locator('#resumeBtn').click();expect(page.locator('#answerText')).to_have_text('The Matrix');expect(page.locator('#awardButtons button').first).to_have_attribute('aria-pressed','true')
  results.append('Desktop: setup, nested URL, spoiler-free pre-reveal DOM text, timer start/pause, hint, reveal, reversible awards, revisits, void/restore and saved-game resume passed.')
  for i in range(2,41):
   page.locator('#nextBtn').click();expect(page.locator('#roundLabel')).to_contain_text(f'{i} of 40')
  page.locator('#nextBtn').click();expect(page.locator('#finish')).to_be_visible();assert '1 / 40' in page.locator('#finalScores').inner_text();results.append('All 40 navigation positions and final scores passed.')
  mobile=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce')
  mobile.route('https://**/*',lambda route:route.fulfill(status=200,content_type='image/gif',body=GIF))
  mp=mobile.new_page();mp.goto(base);assert mp.evaluate('document.documentElement.scrollWidth<=innerWidth');mp.screenshot(path=str(ROOT/'evidence/setup-mobile.png'),full_page=True)
  mp.locator('#startBtn').click();expect(mp.locator('#clip')).to_be_hidden();expect(mp.locator('#timerBtn')).to_be_disabled();mp.locator('#motionBtn').click();expect(mp.locator('#clip')).to_be_visible();assert mp.evaluate('document.documentElement.scrollWidth<=innerWidth');results.append('390 px mobile layout and reduced-motion opt-in passed.')
  fail=browser.new_context();fail.route('https://**/*',lambda route:route.abort());fp=fail.new_page();fp.goto(base);fp.locator('#startBtn').click();expect(fp.locator('#mediaStatus')).to_contain_text('could not load');expect(fp.locator('#timerBtn')).to_be_disabled();results.append('Failed remote media shows a clear error and cannot consume timer time.')
  rp=context.new_page();rp.goto(base+'review.html');expect(rp.locator('.review-item')).to_have_count(40);rp.locator('#checkAll').click();expect(rp.locator('#checkProgress')).to_contain_text('Checked 40 / 40',timeout=20000);assert '0 / 40 visually approved' in rp.locator('#reviewSummary').inner_text();results.append('40-item host network preflight passed with fixtures; checks do not automatically approve content.')
  assert not errors,errors
  results.append('No JavaScript page errors in the main desktop flow.')
  browser.close()
finally:server.shutdown()
(ROOT/'evidence/ui-test-results.json').write_text(json.dumps({'mode':'synthetic-fixture-only','realMediaValidated':False,'passed':results},indent=2)+'\n')
print('\n'.join('PASS: '+x for x in results))
