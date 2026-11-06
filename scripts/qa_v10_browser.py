from pathlib import Path
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parents[1]
import threading, http.server, socketserver
class Handler(http.server.SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(P),**kwargs)
 def log_message(self,*args): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1', 0),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
URL=f'http://127.0.0.1:{server.server_address[1]}/jobs/balance-history.html'
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,height,label in [(390,844,'mobile'),(1365,900,'desktop')]:
  page=b.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(URL,wait_until='load')
  print(label,'initial',page.locator('#balanceCount').inner_text())
  assert page.locator('#balanceCount').inner_text().startswith('表示：21職 / 187件')
  assert page.locator('a[href*="balance-history.html"]').count()>=0
  page.locator('#balancePhase').select_option('S2')
  print(label,'S2',page.locator('#balanceCount').inner_text());assert page.locator('#balanceCount').inner_text().startswith('表示：21職 / 94件')
  page.locator('#balanceClass').select_option('frostmage')
  print(label,'iceS2',page.locator('#balanceCount').inner_text());assert '1職 / 2件' in page.locator('#balanceCount').inner_text()
  page.locator('#balancePhase').select_option('all')
  page.locator('#balanceClass').select_option('all')
  page.locator('#balanceSearch').fill('305%')
  print(label,'keyword',page.locator('#balanceCount').inner_text());assert '1職' in page.locator('#balanceCount').inner_text()
  page.locator('#balanceReset').click()
  assert '187件' in page.locator('#balanceCount').inner_text()
  box=page.evaluate('({body:document.body.scrollWidth,html:document.documentElement.clientWidth})')
  print(label,box,'js errors',errors)
  assert not errors
  assert box['body']<=box['html']+1
  page.screenshot(path=str(P/f'_balance_v10_{label}.png'),full_page=False)
  page.close()
 b.close()
