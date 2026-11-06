from pathlib import Path
import re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json,sys
root=Path(__file__).resolve().parents[1]
pagefile=root/'growth/index.html'
html=pagefile.read_text(encoding='utf8')
soup=BeautifulSoup(html,'html.parser')
assert len(soup.select('#trace-table tbody tr'))==65
assert len(soup.select('#traceStart option'))==65
assert len(soup.select('#traceGoal option'))==65
assert not soup.select('#traceJob')
D=json.loads((root/'data/class-exp.json').read_text('utf8'))
assert len(D['rows'])==65
assert D['rows'][-1]['expCumulative']==2688083277
assert D['rows'][-1]['tracesCumulative']==134405
assert sum(r['expFromPrevious'] or 0 for r in D['rows'])==2688083277
assert sum(r['tracesFromPrevious'] or 0 for r in D['rows'])==134405
errs=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox','--disable-dev-shm-usage'])
 for width in (390,1365):
  page=browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1)
  page.on('pageerror',lambda exc:errs.append(str(exc)))
  def embed_resources(text):
   scripts = []
   def script_sub(m):
    scripts.append((pagefile.parent/m.group(1)).read_text(encoding='utf8'))
    return ''
   text = re.sub(r'<script\s+defer\s+src="([^"]+)"\s*></script>',script_sub,text)
   text = re.sub(r'<link\s+rel="stylesheet"\s+href="([^"]+)"\s*>', lambda m: '<style>'+(pagefile.parent/m.group(1)).read_text(encoding='utf8')+'</style>',text)
   return text.replace('</body>', ''.join('<script>'+js+'</script>' for js in scripts)+'</body>')
  page.set_content(embed_resources(html), wait_until='load')
  page.wait_for_timeout(250)
  result=page.locator('#traceResult').inner_text()
  assert '2,688,083,277' in result and '134,405' in result,(width,result)
  print('initial',width,result.replace('\n',' ')[:150])
  page.locator('#traceStart').select_option('37')
  page.locator('#traceGoal').select_option('43')
  result=page.locator('#traceResult').inner_text()
  expectedExp=D['rows'][42]['expCumulative']-D['rows'][36]['expCumulative']
  expectedTrace=D['rows'][42]['tracesCumulative']-D['rows'][36]['tracesCumulative']
  assert f'{expectedExp:,}' in result and f'{expectedTrace:,}' in result,(result,expectedExp,expectedTrace)
  page.locator('#traceStart').select_option('1')
  page.locator('#traceGoal').select_option('65')
  result=page.locator('#traceResult').inner_text()
  assert '2,688,083,277' in result and '134,405' in result,result
  page.locator('#traceStart').select_option('60')
  page.locator('#traceGoal').select_option('40')
  assert '目標Lvを現在より高く' in page.locator('#traceResult').inner_text()
  size=page.evaluate('({page:document.documentElement.scrollWidth,viewport:document.documentElement.clientWidth,table:document.querySelector(".growth-table-scroll").scrollWidth})')
  print('dimensions',width,size)
  assert size['page']<=size['viewport']+2,'horizontal page overflow'
  page.locator('#grow-lv-65').scroll_into_view_if_needed()
  page.screenshot(path=str(root/f'_v8_growth_{width}.png'),full_page=False)
  page.close()
 browser.close()
print('Browser errors:',errs)
if errs:sys.exit(1)
