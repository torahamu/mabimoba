from pathlib import Path
import sys,re
from playwright.sync_api import sync_playwright
r=Path(__file__).resolve().parents[1]
errors=[]

def embedded_html(path):
    f=r/path
    txt=f.read_text(encoding='utf-8')
    scripts=[]
    def js_replace(m):
        scripts.append((f.parent/m.group(1)).read_text(encoding='utf-8'))
        return ''
    txt=re.sub(r'<script\s+defer\s+src="([^"]+)"\s*></script>',js_replace,txt)
    def css_replace(m):return '<style>'+ (f.parent/m.group(1)).read_text(encoding='utf-8') +'</style>'
    txt=re.sub(r'<link\s+rel="stylesheet"\s+href="([^"]+)"\s*>',css_replace,txt)
    return txt.replace('</body>',''.join('<script>'+s+'</script>' for s in scripts)+'</body>')

with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for name,path,width,height in [('stats_mobile','stats/index.html',390,844),('stats_desktop','stats/index.html',1380,900),('growth_mobile','growth/index.html',390,844),('equipment_mobile','guides/equipment.html',390,844),('home_mobile','index.html',390,844)]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(embedded_html(path),wait_until='load');page.wait_for_timeout(180)
  size=page.evaluate('({scrollWidth:document.documentElement.scrollWidth,clientWidth:document.documentElement.clientWidth})')
  print(name,'scroll:',size,'title:',page.title())
  if size['scrollWidth']>size['clientWidth']+3:errors.append(f'HORIZONTAL OVERFLOW {name}: {size}')
  page.screenshot(path=str(r/f'_preview_{name}.png'),full_page=False)
  if name.startswith('stats_'):
   print('calcResult:',page.locator('#statCalcResult').inner_text()[:120], 'title summary:',page.locator('#titleDone').inner_text())
   page.locator('input[data-title="frostmage"]').check()
   print('title after:',page.locator('#titleBonus').inner_text().replace('\n',' '),page.locator('#titleDone').inner_text())
   page.locator('#statCalcType').select_option('extra')
   print('extra:',page.locator('#statCalcResult').inner_text()[:120])
  elif name.startswith('growth_'):
   print('growth:',page.locator('#traceResult').inner_text()[:130]);page.locator('#traceGoal').select_option('65');print('growth65:',page.locator('#traceResult').inner_text()[:170])

  page.close()
 browser.close()
print('errors:',errors)
if errors: sys.exit(1)
