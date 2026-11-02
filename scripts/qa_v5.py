import json,os,re
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
pages=list(ROOT.rglob('*.html'))
assert len(pages)>=28,(len(pages),pages)
errors=[]
for path in pages:
 s=BeautifulSoup(path.read_text(encoding='utf8'),'html.parser')
 for tag in s.select('a[href],link[href],script[src]'):
  target=tag.get('href') or tag.get('src')
  if target.startswith(('https://','http://','mailto:','#','javascript:','data:')):continue
  target=target.split('?',1)[0].split('#',1)[0]
  if target and not (path.parent/target).resolve().exists():errors.append((str(path.relative_to(ROOT)),target))
 if 'jobs/' in str(path) and path.name!='index.html':
  cards=s.select('.skill-entry')
  if not cards: errors.append((str(path.relative_to(ROOT)),'missing skill cards'))
assert not errors,errors[:30]
sd=json.loads((ROOT/'data/job-skills.json').read_text(encoding='utf8'))['jobs']
assert len(sd)==18
assert all(len(s['skills'])>=5 for s in sd.values())
assert sum(len(x['runes']) for s in sd.values() for x in s['skills'])>=100
print('Pass',len(pages),'HTML pages, skills',sum(len(s['skills']) for s in sd.values()),'links',sum(len(x['runes']) for s in sd.values() for x in s['skills']))
