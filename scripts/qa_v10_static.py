#!/usr/bin/env python3
"""Offline static checks for the v10 Korean class balance archive."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote
import json

ROOT = Path(__file__).resolve().parents[1]
archive = json.loads((ROOT/'data/class-balance-history.json').read_text(encoding='utf-8'))
classes = archive['classes']
entries = [entry for job in classes for entry in job['changes']]
phases = Counter(entry['phase'] for entry in entries)
assert len(classes) == 21, f'classes: {len(classes)}'
assert len(entries) == 187, f'events: {len(entries)}'
assert dict(phases) == {'S0': 57, 'S1': 36, 'S2': 94}, phases
assert len(archive['metadata']['sources']) == 27
assert len({job['slug'] for job in classes}) == 21
assert all(x['source'].startswith('https://mabinogimobile.nexon.com/News/') for x in entries)
assert all(x['type'] in {'強化','弱体化','調整','仕様変更','不具合修正','新職追加'} for x in entries)
assert all(x['phase'] in {'S0','S1','S2'} for x in entries)
assert all(x['date'] and x['title'] and x['detail'] for x in entries)

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=set();self.links=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if d.get('id'): self.ids.add(d['id'])
        for key in ('href','src'):
            if d.get(key): self.links.append(d[key])

pages={}
for page in ROOT.rglob('*.html'):
    parsed=Parser();parsed.feed(page.read_text(encoding='utf-8'));pages[page.resolve()]=parsed
broken=[]
for page, parsed in pages.items():
    for url in parsed.links:
        if url.startswith(('http:','https:','//','data:','mailto:','tel:','javascript:')):continue
        main, _, hash_ = url.partition('#')
        file_path=main.partition('?')[0]
        dest=(page.parent / unquote(file_path)).resolve() if file_path else page
        if not dest.exists():broken.append((str(page.relative_to(ROOT)),url,'missing file'))
        elif hash_ and dest in pages and unquote(hash_) not in pages[dest].ids:
            broken.append((str(page.relative_to(ROOT)),url,'missing anchor'))
assert not broken, f'broken links: {broken[:10]}'
html=(ROOT/'jobs/balance-history.html').read_text(encoding='utf-8')
assert html.count('class="balance-event"') == 187
assert html.count('class="balance-class portal-panel"') == 21
assert 'option value="S2"' in html
assert '韓国S0 → S1 → S2' in html
print(f'PASS: {len(pages)} HTML pages, 21 classes, 187 events, S2 94, 27 primary sources, 0 broken local links.')
