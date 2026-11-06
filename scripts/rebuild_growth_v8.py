#!/usr/bin/env python3
"""v8: クラス EXP 1〜65表の再生成。data/class-exp.json が唯一の元データ。"""
from pathlib import Path
import html, json, re
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/class-exp.json'
PAGE=ROOT/'growth/index.html'
JS=ROOT/'assets/growth.js'

# Korean Season 0 per-level class EXP, 1->2 ... 64->65.
# Sources: https://adimpnem.tistory.com/149 and https://mabinogi.begchi.com/.../
EXP=[
6754,13508,20262,27014,33768,40522,47276,54030,60784,63000,
64000,65000,66000,67000,68000,69000,70000,76000,82000,140000,
141828,148582,155334,162088,168842,175596,182350,189104,195856,202610,
1829022,1865594,4013190,7000000,10908518,11235754,11572798,11919958,12277536,14542710,
15415272,16340188,17320600,18359836,19461426,22769688,26640746,31169673,36468517,42668165,
49921753,58408451,68337888,79955329,93547735,109450850,128057495,149827269,175297905,205098549,
239965302,280759403,328488502,384331547]
TRACE_STEP=[
1,1,1,1,2,2,2,3,3,3,
3,3,4,3,3,4,3,4,4,7,
7,8,7,9,8,9,9,9,10,10,
92,93,201,350,545,562,579,596,613,728,
770,817,866,918,973,1139,1332,1558,1824,2133,
2496,2921,3417,3997,4678,5472,6403,7492,8764,10255,
11999,14038,16424,19217]
assert len(EXP)==len(TRACE_STEP)==64
cume=0; cumt=0
rows=[dict(level=1,expFromPrevious=None,expCumulative=0,tracesFromPrevious=None,tracesCumulative=0)]
for i,(exp,traces) in enumerate(zip(EXP,TRACE_STEP),2):
    cume+=exp;cumt+=traces
    rows.append(dict(level=i,expFromPrevious=exp,expCumulative=cume,tracesFromPrevious=traces,tracesCumulative=cumt))
assert len(rows)==65
for lvl,expectedExp,expectedTraces in [(25,1741750,88),(35,17563914,879),(40,75478478,3774),(45,157457084,7873),(50,293967134,14699),(55,593258720,29663),(60,1249439974,62472),(65,2688083277,134405)]:
    record=rows[lvl-1]
    assert (record['expCumulative'],record['tracesCumulative'])==(expectedExp,expectedTraces),(lvl,record)
info={
'schemaVersion':1,
'region':'KR',
'season':'Season 0 (2025-06-01先行掲載表)',
'updatedAt':'2026-11-06',
'kind':'class-level exp (not character-level exp)',
'expPerTraceEstimate':20000,
'rows':rows,
'sources':[
  {'label':'韓国・個人実測（2025-06-01）','url':'https://adimpnem.tistory.com/149'},
  {'label':'韓国・非公式センター（2025-04〜05）','url':'https://mabinogi.begchi.com/%EB%AA%A8%EB%B0%94%EC%9D%BC-%ED%81%B4%EB%9E%98%EC%8A%A4-%EA%B2%BD%ED%97%98%EC%B9%98-%ED%85%8C%EC%9D%B4%EB%B8%94-%EC%A0%95%EB%A0%B9%EC%9D%98-%ED%9D%94%EC%A0%81-%EC%86%8C%EB%AA%A8%EB%9F%89'},
  {'label':'台湾コミュニティ実測 Lv1〜51','url':'https://forum.gamer.com.tw/C.php?bsn=32564&snA=2853'}
],
'conflicts':[
  {'source':'https://danasn.tistory.com/1544','issue':'Lv64→65を400,000,000EXPとする別報告（本表は384,331,547）'},
  {'source':'https://www.inven.co.kr/board/mabimo/6366/318','issue':'Lv1→65を3,137,751,367EXP、痕跡約156,888とする別報告（本表2,688,083,277EXP、痕跡134,405）'}
],
'caution':'日本版のゲーム画面での数値は未検証。痕跡は先行プレイヤー表の各段階切上げ計算であり、途中獲得EXPや端数引き継ぎで実際の必要数が変わり得ます。'
}
DATA.write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

number=lambda v:('—' if v is None else f'{v:,}')
options=''.join(f'<option value="{n}">{n}</option>' for n in range(1,66))
trs=[]
for r in rows:
    lv=r['level']; mark=' class="growth-milestone"' if lv in (25,35,40,45,55,65) else ''
    trs.append(f'<tr{mark} id="grow-lv-{lv}"><th scope="row">Lv{lv}</th><td>{number(r["expFromPrevious"])}</td><td>{number(r["expCumulative"])}</td><td>{number(r["tracesFromPrevious"])}</td><td>{number(r["tracesCumulative"])}</td></tr>')
content=''.join(trs)
page=PAGE.read_text(encoding='utf-8')
# v8.1: this calculation is identical across classes, so the class selector is removed.
page=re.sub(r'<label>クラス<select id="traceJob">.*?</select></label>', '', page, count=1, flags=re.S)
page=page.replace('<div class="sim-form"><label>現在のクラスLv', '<div class="sim-form growth-level-form"><label>現在のクラスLv')
page=re.sub(r'<h1 class="portal-page-title">クラス育成と精霊の痕跡</h1>', '<h1 class="portal-page-title">クラス育成と精霊の痕跡</h1>', page)
page=page.replace('Lv35・40・65の優先度と必要個数。先行表の差分を自動計算し、Lv65の矛盾する資料もそのまま残しています。','Lv1〜65のクラス経験値を1レベル刻みで掲載。必要EXP・累積EXP・精霊の痕跡を比較し、育成費用を計算できます。')
# Note: replace prior entire research-note (contains conflicting old wording)
oldnote=re.search(r'<div class="research-note"><strong>(?:数値の出典について：|表の基準：)</strong>.*?</div>',page)
assert oldnote
newnote=('''<div class="research-note"><strong>表の基準：</strong>韓国Season 0のクラス育成に関するプレイヤー実測（2025年5〜6月）です。日本版の確定値ではありません。'''
         '''<strong>Lv1→65は累積2,688,083,277 EXP、痕跡134,405個</strong>という一貫した先行表を採用。'''
         '''別の韓国実測では累積<strong>3,137,751,367 EXP・約156,888個</strong>とされるため、表の末尾で差異を明記しています。'''
         '''「痕跡」は端数の持ち越し・途中で貯めた経験値によって実際の使用個数が変動します。</div>''')
page=page.replace(oldnote.group(0),newnote)
page=page.replace('「この職をLv35からLv40にしたら何個必要？」を確認できます。必要個数は登録された節目間のみ計算します。','「Lv37からLv43まで」など、1レベル単位で必要EXPと痕跡の先行目安を計算します。現在のレベルゲージに既に入っている経験値は含めません。')
page=re.sub(r'(<select id="traceStart">).*?(</select>)',lambda m:m.group(1)+options+m.group(2),page)
page=re.sub(r'(<select id="traceGoal">).*?(</select>)',lambda m:m.group(1)+options+m.group(2),page)
# Add info right after calc note, keep all existing other sections
panelstart=page.index('<section class="portal-panel" id="trace-table">')
nextsec=page.index('<section class="portal-panel" id="growth-tactics">',panelstart)
newsection='''<section class="portal-panel" id="trace-table"><span class="portal-kicker">LEVEL BY LEVEL · KR S0</span><h2>Lv1〜65：必要経験値と精霊の痕跡</h2>
<p class="muted-note">「前Lvからの必要EXP」は<strong>そのレベルへ到達するため</strong>に必要なクラス経験値です。例：Lv40行はLv39→40の必要EXP。<strong>累積EXP</strong>はLv1からそのレベルまでの合計です。</p>
<div class="growth-milestone-links" aria-label="レベル節目へ移動"><span>節目へ：</span>'''+''.join(f'<a href="#grow-lv-{x}">Lv{x}</a>' for x in (25,35,40,45,55,65))+'''</div>
<p class="growth-scroll-hint">表は横スクロールできます <span aria-hidden="true">⇆</span>（スマホ）</p>
<div class="table-scroll growth-table-scroll"><table class="research-table growth-exp-table"><caption class="sr-only">クラスLv1〜65の必要経験値、累積経験値、精霊の痕跡必要個数</caption><thead><tr><th scope="col">到達Lv</th><th scope="col">前Lvからの必要EXP</th><th scope="col">累積EXP</th><th scope="col">必要な痕跡</th><th scope="col">累積の痕跡</th></tr></thead><tbody>'''+content+'''</tbody></table></div>
<div class="research-note"><b>数値差に注意：</b>主表は韓国の2025年6月1日付の1〜65実測表に準拠。別資料では<strong>Lv64→65を400,000,000 EXP</strong>（主表384,331,547）、さらに韓国Invenには<strong>Lv1→65を3,137,751,367 EXP</strong>とする報告があります。日本版にそのまま当てはまると断定しないでください。</div>
<div class="ref-links"><a href="https://adimpnem.tistory.com/149" target="_blank" rel="noopener noreferrer">韓国・Lv別必要EXP原表</a><a href="https://mabinogi.begchi.com/%EB%AA%A8%EB%B0%94%EC%9D%BC-%ED%81%B4%EB%9E%98%EC%8A%A4-%EA%B2%BD%ED%97%98%EC%B9%98-%ED%85%8C%EC%9D%B4%EB%B8%94-%EC%A0%95%EB%A0%B9%EC%9D%98-%ED%9D%94%EC%A0%81-%EC%86%8C%EB%AA%A8%EB%9F%89" target="_blank" rel="noopener noreferrer">韓国・累積表照合</a><a href="https://forum.gamer.com.tw/C.php?bsn=32564&amp;snA=2853" target="_blank" rel="noopener noreferrer">台湾・Lv1〜51実測</a></div>
</section>'''
page=page[:panelstart]+newsection+page[nextsec:]
page=page.replace('必要個数は登録された節目間のみ計算します。','必要個数を1レベル刻みで計算します。')
page=page.replace('当サイトではLv1→35を879個、Lv1→40を3,774個とする表を優先掲載。別サイトの計算表にはLv35が600個の例もあるため、日本版で再測定が必要です。計算器はこの表に忠実に動作します。','当サイトは韓国Season 0先行実測値を採用。日本版の実機表示を優先してください。')
page=page.replace('根拠：本プロジェクト2026-11-06引継ぎ資料「精霊の痕跡でクラスLv1から育てる累計表」および2026-10-19調査まとめ。独立した公式必要量表は取得できていません。','出典：韓国2025年のLv別実測表と台湾Lv1〜51の検証。日本公式はクラスEXPの獲得方法を説明していますが、65段階の必要EXPの数値表は確認できませんでした。')
# Inline dataset: no fetch, works offline and on GitHub Pages. Script doesn't parse this tag recursively.
page=page.replace('<script defer src="../assets/growth.js"></script>','<script defer src="../assets/growth.js"></script>')
dataset_tag=f'<script type="application/json" id="classExpDataset">{json.dumps(rows,ensure_ascii=False,separators=(",",":"))}</script>'
if 'id="classExpDataset"' in page:
    page=re.sub(r'<script type="application/json" id="classExpDataset">.*?</script>',lambda m:dataset_tag,page)
else:
    page=page.replace('</main></body></html>',dataset_tag+'</main></body></html>')
PAGE.write_text(page,encoding='utf-8')
JS.write_text('''/* KR Season 0 class EXP data is embedded into growth/index.html at build-time. */
(() => {
  'use strict';
  const el = id => document.getElementById(id);
  const levels = JSON.parse(el('classExpDataset').textContent);
  const byLevel = new Map(levels.map(r => [r.level, r]));
  const fmt = n => n.toLocaleString('ja-JP');
  el('traceStart').value = '1';
  el('traceGoal').value = '65';
  function calculate() {
    const a = Number(el('traceStart').value), b = Number(el('traceGoal').value);
    const target = el('traceResult');
    if (a >= b) {
      target.innerHTML = '<div class="result-main"><b>目標Lvを現在より高くしてください</b></div>';
      return;
    }
    const start = byLevel.get(a), goal = byLevel.get(b);
    if (!start || !goal) return;
    const xp = goal.expCumulative - start.expCumulative;
    const traces = goal.tracesCumulative - start.tracesCumulative;
    const note = b === 65
      ? 'この痕跡数は韓国Season 0の一つの実測表に基づきます。別の報告ではLv1→65に約156,888個必要とされ、差があります。'
      : '韓国Season 0のLv別経験値表と痕跡消費表から計算。必要な痕跡は端数・現在のEXP残高によって変動します。';
    target.innerHTML = `<div class="result-main"><b>${fmt(xp)} EXP</b><small>Lv${a} → Lv${b} に必要なクラス経験値</small></div><div class="result-columns"><span>精霊の痕跡 <strong>${fmt(traces)} 個</strong></span><span>累積EXP ${fmt(start.expCumulative)} → ${fmt(goal.expCumulative)}</span></div><p class="muted-note">${note} 現在Lvで既に獲得した経験値は含みません。</p>`;
  }
  ['traceStart', 'traceGoal'].forEach(id => el(id).addEventListener('change', calculate));
  calculate();
})();
''',encoding='utf-8')

CSS=ROOT/'assets/site.css'
css=CSS.read_text(encoding='utf-8')
if '/* v8: クラスLv1〜65 EXP表。' not in css:
    css+='''\n/* v8: クラスLv1〜65 EXP表。スマホでは数値を横スクロールして確認 */
.growth-table-scroll{border:1px solid var(--p-border);border-radius:10px;overflow-x:auto;scrollbar-color:#4e7b94 #15273b}
.growth-exp-table{width:100%;min-width:760px;border-collapse:separate;border-spacing:0;font-variant-numeric:tabular-nums;font-size:.87rem}
.growth-exp-table th,.growth-exp-table td{padding:10px 14px;text-align:right;white-space:nowrap;border-bottom:1px solid #2b4157}
.growth-exp-table th:first-child,.growth-exp-table td:first-child{text-align:left;position:sticky;left:0;background:#14263a;z-index:1;min-width:82px;box-shadow:3px 0 9px #0004}
.growth-exp-table thead th{background:#204056;color:#a9e9ef;position:sticky;top:0;z-index:2;line-height:1.45}
.growth-exp-table thead th:first-child{background:#204056;z-index:3}
.growth-exp-table tbody tr:hover td,.growth-exp-table tbody tr:hover th{background:#24445b}
.growth-exp-table tbody tr.growth-milestone td,.growth-exp-table tbody tr.growth-milestone th{background:#25413f;color:#e0fff6;font-weight:800}
.growth-exp-table tbody tr.growth-milestone:hover td,.growth-exp-table tbody tr.growth-milestone:hover th{background:#35615a}
.growth-milestone-links{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:13px 0}.growth-milestone-links span{font-size:13px;color:var(--p-muted)}
.growth-milestone-links a{padding:4px 10px;border:1px solid #486a74;background:#193647;border-radius:7px;text-decoration:none;font-size:12px;font-weight:750}
.growth-exp-table tbody tr{scroll-margin-top:120px}
.growth-scroll-hint{font-size:.76rem;color:#a6bdcb;margin:4px 0 10px}.growth-scroll-hint span{font-size:1.2rem;color:#91dbeb}
.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap}
@media(min-width:900px){.growth-scroll-hint{display:none}}
@media(max-width:620px){.growth-exp-table{font-size:.83rem;min-width:725px}.growth-exp-table th,.growth-exp-table td{padding:10px 10px}.growth-exp-table th:first-child,.growth-exp-table td:first-child{min-width:69px}}
'''
css += '''\n/* v8.1 class-independent calculator */\n.sim-form.growth-level-form{grid-template-columns:repeat(2,minmax(0,1fr))}\n@media(max-width:620px){.sim-form.growth-level-form{grid-template-columns:1fr}}\n'''
CSS.write_text(css,encoding='utf-8')
print('Generated 65 levels:', rows[24], rows[34], rows[39], rows[64])
