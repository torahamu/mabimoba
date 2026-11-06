from pathlib import Path
import json
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parents[1]
data=json.loads((P/'data/class-balance-history.json').read_text())
assert len(data['classes'])==19
changes=sum((len(c['changes']) for c in data['classes']),0)
assert changes==91
assert len({c['slug'] for c in data['classes']})==19
assert len({c['name'] for c in data['classes']})==19
assert [c['name'] for c in data['classes'] if c['slug']=='lightning']==['電撃術師']
for c in data['classes']:
 assert c['changes'],c['name']
 for x in c['changes']:
  assert x['date']<='2025-10-30'
  assert x['source'].startswith('https://mabinogimobile.nexon.com/')
  assert x['phase']==('S0' if x['date']<'2025-09-25' else 'S1')
for p in P.rglob('*.html'):
 soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 assert soup.title, p
 # local path links, but not references into same-page anchors
 for tag in soup.select('a[href],link[href],script[src]'):
  ref=tag.get('href') or tag.get('src')
  if not ref or ref.startswith(('#','http://','https://','mailto:','javascript:','data:')):continue
  target=(p.parent / ref.split('#')[0].split('?')[0]).resolve()
  assert target.is_file(),(p,ref)
print(f'OK: classes={len(data["classes"])}, changes={changes}, html links valid')
