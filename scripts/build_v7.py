#!/usr/bin/env python3
"""Add v7 standalone research pages based on the current project's source notes.
Preserves the v6 job builds / rune dataset. Re-run from the site root.
"""
from pathlib import Path
from html import escape
import json, re
ROOT=Path(__file__).resolve().parents[1]
(ROOT/'stats').mkdir(exist_ok=True)
(ROOT/'growth').mkdir(exist_ok=True)
(ROOT/'guides').mkdir(exist_ok=True)

JOBS=json.loads((ROOT/'data/job-builds.json').read_text(encoding='utf-8'))['jobs']
PAIR={
 'warrior':['STR','WILL'],'greatsword':['STR','WILL'],'swordmaster':['STR','LUCK'],
 'archer':['DEX','LUCK'],'crossbow':['DEX','LUCK'],'longbow':['DEX','WILL'],
 'mage':['INT','LUCK'],'firemage':['INT','LUCK'],'frostmage':['INT','WILL'],
 'healer':['INT','WILL'],'priest':['INT','WILL'],'monk':['INT','WILL'],
 'bard':['DEX','LUCK'],'dancer':['DEX','LUCK'],'musician':['DEX','WILL'],
 'rogue':['DEX','LUCK'],'fighter':['DEX','WILL'],'dualblade':['DEX','LUCK']}
TITLES=[dict(slug=x['slug'],job=x['name'],family=x['family'],attrs=PAIR[x['slug']],source='韓国先行の候補値',status='要JP照合') for x in JOBS]
(ROOT/'data/class-titles.json').write_text(json.dumps({'reference_date':'2026-11-06','status':'韓国先行（+25×2）。Lv65で称号獲得自体は日本公式確認。各職組み合わせは日本実機要照合。','items':TITLES},ensure_ascii=False,indent=2)+'\n', encoding='utf-8')

def stat(k,label,attr,value,brief,detail,formula,tip,kind='model'):
 return dict(id=k,name=label,attr=attr,example=value,short=brief,detail=detail,formula=formula,note=tip,kind=kind)
STATS=[
 stat('break','ブレイク','STR',664,'敵のブレイクゲージと、ブレイク中の無防備攻撃を強化。','ブレイクゲージへの蓄積と、敵がブレイク状態の間に与える無防備ダメージは異なる判定です。','無防備時の能力値部分 ≈ 1 + ブレイク / 5250','ブレイクゲージの蓄積量への正確な換算は未確定。'),
 stat('damage-down','ダメージダウン','STR',791,'敵から受けるダメージを抑える防御系能力。','ダメージダウンは割合表示ではありません。防御力と併せて被ダメージへ反映されます。韓国検証でも異なる推定式が併存しています。','推定式A：被ダメ ≈ 元ダメ / {1+(防御/6500)×(1+ダウン/6500)}\n推定式B：被ダメ ≈ 元ダメ/(1+防御/10000)−ダウン','どちらが日本版の内部式と一致するか未検証。固定値のまま引く式Bは小ダメージで破綻し得るため、試算の目安まで。', 'disputed'),
 stat('strong','強打強化','STR',764,'強打判定が成立した攻撃のダメージを上乗せ。','強打強化を上げるだけで全攻撃が強打になるわけではありません。強打判定の成立条件が必要です。','強打時の能力値部分 ≈ 1 + 強打強化 / 8500','さらに強打ダメージ+○%などの補正を掛け合わせるモデルです。'),
 stat('quick','速攻','DEX',645,'通常攻撃の間隔を短くする能力。','「スキル高速化」と別物で、通常攻撃の速度に関与します。','数値→通常攻撃間隔の公式：未確認','韓国先行に換算モデルはありますが、日本版の速度上限やスキルとの関係は未検証。','unknown'),
 stat('combo','コンボ強化','DEX',501,'コンボが積み重なる戦闘で、コンボ判定の攻撃を強化。','コンボ数の段階で強化量が変わるという韓国先行モデルがあります。','コンボ加算の能力値部分 ≈ (コンボ強化 / 17500) × (段階 / 4)\n段階：1〜10→1／11〜50→2／51〜100→3／101以上→4','コンボ状態の成立条件・加算枠に版差があり得ます。'),
 stat('rapid','連打強化','DEX',531,'短時間で多数ヒットした際の「連打」判定を強化。','連打はヒット回数の条件が必要で、通常の「追加攻撃」とは別のダメージ判定です。','連打時の能力値部分 ≈ 1 + 連打強化 / 8500','「3秒内6ヒット以上」は韓国先行の条件例。日本版での判定は要確認。'),
 stat('skill','スキル威力','INT',887,'主にスキルダメージへ作用する汎用の攻撃補正。','攻撃力や「与ダメージ+%」とは異なる計算段階です。','スキル威力による倍率の基本項 ≈ 1 + スキル威力 / 8500','ほかのスキルダメージ増加・与ダメージ増加と同一枠とは限りません。'),
 stat('skill-speed','スキル高速化','INT',738,'キャスト・チャージ・スキル使用モーションを短縮。','スキルのCTを直接減らす能力ではありません。通常魔法使いのパッシブなど、間接作用する可能性は別途検証が必要です。','値→時間短縮の一般式：未確定\n台湾実測例：能力値+1028で約5.5〜12.1%短縮（5技）','使用スキル、モーション、初期値で差があり、+1000＝固定で10%短縮ではありません。','unknown'),
 stat('area','広域強化','INT',591,'同時に複数の対象へ当てるマルチヒット判定を強化。','単体ボスに広範囲スキルを1発当てただけでは、マルチヒット判定を満たさない場合があります。','マルチヒット時の能力値部分 ≈ 1 + 広域強化 / 8500','技の表示が範囲攻撃でも、敵が1体なら発動しないという区別に注意。'),
 stat('hp-extra','追加HP','WILL',4561,'最大HPに加算される耐久系能力。','画面の「追加HP」はキャラクターの最大HP総量ではありません。','最大HPの構成：基礎HP + 追加HP + その他HP補正（概念式）','割合HPバフとの加算順序は別途確認が必要。','partial'),
 stat('healing','回復力','WILL',1591,'スキルや回復アイテムの回復量に関わる。','回復役だけでなく大剣戦士などの自己回復にも関係します。','韓国推定モデルで回復力 / 8750 を含む\n回復量には攻撃力・スキル係数・回復%等も関与','単純に「回復力1591＝回復15.91%」ではありません。','partial'),
 stat('ultimate','究極技','WILL',862,'究極技のダメージとゲージの回復量を強化。','究極技がバフ主体の職では、ダメージ補正があまり有用でないこともあります。','ゲージ獲得倍率 ≈ 1 + 究極技 / 7250\n究極技ダメージ倍率 ≈ 1 + 究極技 / 8750','スキル固有のゲージ獲得条件、他の究極技バフを除いた能力値部分。'),
 stat('weak','急所回避','LUCK',530,'被弾時に確率でダメージの一部を軽減。','完全回避・クリティカル無効ではありません。公式韓国ガイドで一部軽減と説明されています。','発動確率への厳密な換算式：未確認','「急所回避＝被ダメージ0」と説明する資料もありますが、公式側の説明を優先します。','unknown'),
 stat('critical','クリティカル','LUCK',1057,'発生率と、クリティカル発動時の倍率の両方が上昇。','能力値由来のクリ率と、装備やコンテンツ条件の追加補正を区別します。','能力値由来の基礎率 ≈ 0.5×C/(C+2000)\nクリ倍率 ≈ 1.4 + C/5000\n（追加補正なし）期待倍率 ≈ 1 + C/10000','最終クリ率は能力値以外のバフ・戦力差・敵などで変動。高難度での戦力差補正は未確認。'),
 stat('extra','追加攻撃','LUCK',369,'攻撃判定に追加のヒットが発生する確率に関与。','クリティカル、連打、強打とは別の判定です。先行版では追加攻撃100%超過の扱いに更新差があります。','追加攻撃の期待倍率 ≈ 1 + 追加攻撃 / 13000\n追加攻撃率バフrを仮定： (1+能力値/13000)×(1+r) − 1','このモデルは期待倍率であり、すべてのスキルで同じ追加ヒットが保証されるわけではありません。')
]
(ROOT/'data/stats.json').write_text(json.dumps({'asof':'2026-11-06','example_origin':'2026-11-06添付画像を手動転記した例','primary':{'STR':1482,'DEX':1404,'INT':1776,'WILL':1679,'LUCK':1478},'attack':6983,'defense':5752,'secondary':STATS,'sources':[
 {'name':'日本公式：基本ステータス','url':'https://mabinogimobile.nexon.co.jp/about/guide/3541615'},
 {'name':'韓国公式：ダメージ判定','url':'https://mabinogimobile.nexon.com/Info/Guide/2751060'},
 {'name':'SNOMET：非公式計算モデル','url':'https://www.snomet.kr/mobi/stat'},
 {'name':'韓国コミュニティWiki：能力値の式（非公式）','url':'https://dark.namu.moe/w/%EB%A7%88%EB%B9%84%EB%85%B8%EA%B8%B0%20%EB%AA%A8%EB%B0%94%EC%9D%BC/%EB%8A%A5%EB%A0%A5%EC%B9%98'},
 {'name':'台湾プレイヤー：スキル高速化の実測','url':'https://forum.gamer.com.tw/C.php?bsn=32564&snA=2236'},
 {'name':'日本公式：クラスとエンブレム','url':'https://mabinogimobile.nexon.co.jp/about/guide/3541625'},
 {'name':'日本公式：タイトル','url':'https://mabinogimobile.nexon.co.jp/about/guide/3541613'}]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

STYLE='''<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#09111e"><link rel="stylesheet" href="../assets/site.css"><script defer src="../assets/site.js"></script>'''
def page(title, section, kicker, heading, subtitle, content, js='',footer='情報更新：2026-11-06。非公式研究資料。日本公式・ゲーム内表示を優先してください。'):
 return f'''<!doctype html><html lang="ja"><head>{STYLE}<title>{escape(title)}｜エリン調査ノート</title>{js}</head><body><div id="siteNav" data-current="{section}" data-root="../"></div><main class="portal-wrap"><section class="job-hero"><div class="portal-kicker">{escape(kicker)}</div><h1 class="portal-page-title">{escape(heading)}</h1><p class="portal-lead">{escape(subtitle)}</p></section>{content}<footer class="portal-foot">{escape(footer)}</footer></main></body></html>'''
def sources(items):return '<div class="ref-links">'+''.join(f'<a href="{escape(url)}" target="_blank" rel="noopener">{escape(label)} ↗</a>' for label,url in items)+'</div>'

# ----- Stats dossier, screenshot-like numbers and interactive analysis -----
base={'STR':1482,'DEX':1404,'INT':1776,'WILL':1679,'LUCK':1478}
cols=[('STR','筋力','strength'),('DEX','器用','dexterity'),('INT','知力','intelligence'),('WILL','意志','will'),('LUCK','幸運','luck')]
primary_html=''.join(f'<a href="#group-{key.lower()}" class="stat-primary stat-{key.lower()}"><span>{label}</span><b>{key}</b><strong>{base[key]:,}</strong></a>' for key,label,_ in cols)
# faithful screenshot pair order
left=['break','strong','combo','skill','area','healing','weak','extra']
right=['damage-down','quick','rapid','skill-speed','hp-extra','ultimate','critical']
byid={x['id']:x for x in STATS}
def demo_line(k):
 x=byid[k];return f'<a href="#stat-{k}" class="stat-demo-line stat-tone-{x["attr"].lower()}"><i class="stat-demo-dot"></i><span>{x["name"]}</span><b>{x["example"]:,}</b></a>'
screenshot_demo=f'''<section class="stat-demo" id="snapshot"><div class="stat-demo-head"><span>CHARACTER PROFILE · 添付画面の値を再現</span><span>2026-11-06 参考</span></div><div class="stat-primary-grid">{primary_html}</div><div class="stat-attack-row"><div>⚔ <span>攻撃力</span><b>6,983</b></div><div>⬡ <span>防御力</span><b>5,752</b></div></div><div class="stat-demo-abilities"><div>{''.join(demo_line(x) for x in left)}</div><div>{''.join(demo_line(x) for x in right)}</div></div><p class="stat-demo-hint">各ステータスをタップすると効果・計算式へ移動します。数値は添付画像を転記した例で、現在のライブ値ではありません。</p></section>'''

stat_cards=[]
for attr,label,_ in cols:
 subset=[x for x in STATS if x['attr']==attr]
 cards=''.join(f'''<article id="stat-{x['id']}" class="stat-explain-card"><div class="stat-explain-top"><h3>{x['name']}</h3><span class="status-small {'unknown' if x['kind'] in ('unknown','disputed') else 'estimate'}">{'式未確定' if x['kind']=='unknown' else 'モデル競合' if x['kind']=='disputed' else '一部のみ検証' if x['kind']=='partial' else '非公式モデル'}</span></div><p>{x['short']}</p><p class="muted-note">{x['detail']}</p><div class="stat-formula"><div>計算・換算</div><code>{escape(x['formula'])}</code></div><div class="stat-qualify">{x['note']}</div></article>''' for x in subset)
 stat_cards.append(f'<section id="group-{attr.lower()}" class="stat-group"><div class="stat-group-title stat-tone-{attr.lower()}"><h2>{attr} <small>{label}</small></h2><span>{len(subset)}項目 ／ 添付画像 {base[attr]:,}</span></div><div class="stat-explain-grid">{cards}</div></section>')

title_rows=''.join(f'''<label class="title-choice"><input type="checkbox" data-title="{x['slug']}" data-attrs="{','.join(x['attrs'])}"><span><strong>{x['job']}</strong><small>{x['family']}</small></span><em>{' · '.join(f'{a} +25' for a in x['attrs'])}</em><a href="../jobs/{x['slug']}.html" class="title-joblink" aria-label="{x['job']}のガイド">職攻略 ↗</a></label>''' for x in TITLES)

stats_content=f'''<nav class="doc-jumps"><a href="#snapshot">画面から探す</a><a href="#stat-dictionary">15項目の解説</a><a href="#estimate">計算シミュレーター</a><a href="#class-title">Lv65称号</a><a href="#stat-sources">情報源</a></nav>
<section class="research-note"><b>このページの読み方：</b>各能力の「何に効くか」は公式説明に合わせ、％への変換は韓国・台湾プレイヤーの非公式モデルを掲載しています。<b>「STR+100でブレイクが何点増えるか」など、基本能力値→特殊ステータスの内部換算式は公開されていません。</b>装備・タイトル・ペット・レベルアップカード等の加算も含むため、添付の数値だけでは係数を逆算できません。</section>
{screenshot_demo}
<section class="portal-panel stat-flow" id="stat-dictionary"><h2>ステータスが伸びるまでの3段階</h2><div class="stat-flow-grid"><div><b>01 ｜入手</b><p>カード・クラス成長・称号・装備・宝石・ルーン・ペット</p></div><div><b>02 ｜表示値</b><p>STR等 → 関連する15能力値へ。内部の換算係数は未公開</p></div><div><b>03 ｜戦闘判定</b><p>強打・連打・範囲・クリなどの判定が成立して、非公式倍率モデルを適用</p></div></div><p class="muted-note">攻撃力・防御力も装備と能力値の影響を受けます。攻撃力の概算式や防御・ダメージダウンの別説は<a href="../tools/damagecalc.html">ダメージ計算</a>と、このページの式に併記しています。</p></section>
{''.join(stat_cards)}
<section class="portal-panel sim-section" id="estimate"><div class="mini-heading"><div><span class="portal-kicker">INTERACTIVE · FAN-MADE MODEL</span><h2>数値が増えると何が変わる？</h2></div><span class="status-small estimate">韓国非公式近似式</span></div><p class="muted-note">スキル・敵・装備が同じという条件で、能力値による倍率部分だけを比較します。日本版実測結果ではありません。</p><div class="sim-form"><label>調べる能力<select id="statCalcType"><option value="critical">クリティカル</option><option value="extra">追加攻撃</option><option value="skill">スキル威力</option><option value="strong">強打強化</option><option value="rapid">連打強化</option><option value="area">広域強化</option><option value="combo">コンボ強化</option><option value="break">ブレイク中の無防備</option><option value="ultimate">究極技</option></select></label><label>現在の能力値<input id="statCalcCurrent" type="number" inputmode="numeric" min="0" max="999999" value="1057"></label><label>増やすポイント<input id="statCalcPlus" type="number" inputmode="numeric" min="0" max="999999" value="100"></label></div><div id="statCalcResult" class="stat-sim-result" aria-live="polite"></div><div class="sim-second"><h3>防御式の2説を比較</h3><p>どちらも非公式です。片方を確定式として使わず、違いを把握するための比較です。</p><div class="sim-form"><label>軽減前の被ダメ<input id="defIncoming" type="number" value="10000" min="1"></label><label>防御力<input id="defValue" type="number" value="5752" min="0"></label><label>ダメージダウン<input id="defDownValue" type="number" value="791" min="0"></label></div><div id="defResult" class="def-result" aria-live="polite"></div></div></section>
<section class="portal-panel title-section" id="class-title"><div class="mini-heading"><div><span class="portal-kicker">PERMANENT PROGRESSION · CLASS LV65</span><h2>クラスLv65の所持称号ボーナス</h2></div><span class="status-small estimate">職別+25は先行資料</span></div><p>日本公式は「クラスLv65で永続的に能力値が上がる称号を獲得」と案内しています。<strong>以下の18職・2能力値各+25は、韓国先行資料と既存攻略本から整理した候補表です。</strong>日本版で個別名称・数値を再照合するまでは確定値として扱いません。</p><div class="title-summary"><div><span>チェック済み</span><strong id="titleDone">0 <small>/ 18職</small></strong></div><div><span>獲得した場合の合計</span><strong id="titleTotal">+0 <small>能力値ポイント</small></strong></div></div><div class="title-bonus-grid" id="titleBonus"></div><div class="title-actions"><button class="portal-btn" type="button" id="titlesAll">すべてチェック</button><button type="button" id="titlesClear">チェックを解除</button><small>チェックはこのブラウザ内に保存されます。日本版実績と自動同期するものではありません。</small></div><div class="title-choices" id="titleChoices">{title_rows}</div><p class="muted-note">各職のクラスLvはキャラクター別です。所持称号のアカウント共有範囲は個別に確認してください。全18職を達成した場合の増分はチェックボックスで確認できます。<a href="../growth/index.html">精霊の痕跡の育成計画 →</a></p></section>
<section id="stat-sources" class="portal-panel"><h2>参考資料・確度の区別</h2><p>公式ガイドは能力の方向性と称号獲得条件を説明していますが、％換算の分母（8500・13000・5250など）は公開していません。非公式式は時期・地域・敵条件で変化する可能性があります。</p>{sources([
 ('日本公式：基本ステータス','https://mabinogimobile.nexon.co.jp/about/guide/3541615'),('日本公式：クラスとエンブレム','https://mabinogimobile.nexon.co.jp/about/guide/3541625'),('日本公式：タイトル','https://mabinogimobile.nexon.co.jp/about/guide/3541613'),('韓国公式：ダメージ判定','https://mabinogimobile.nexon.com/Info/Guide/2751060'),('韓国非公式：SNOMET計算モデル','https://www.snomet.kr/mobi/stat'),('韓国コミュニティ：能力値検証まとめ','https://dark.namu.moe/w/%EB%A7%88%EB%B9%84%EB%85%B8%EA%B8%B0%20%EB%AA%A8%EB%B0%94%EC%9D%BC/%EB%8A%A5%EB%A0%A5%EC%B9%98'),('台湾：スキル高速化120fps実測','https://forum.gamer.com.tw/C.php?bsn=32564&snA=2236')])}<p class="muted-note">クラスLv65の職別組み合わせは本プロジェクト「氷結術師攻略本v1.4」CH05 および「総合引継ぎ2026-10-19」のリストを採用しています。</p></section>'''
(ROOT/'stats/index.html').write_text(page('ステータス図鑑とクラスLv65ボーナス','stats','COMBAT STATS · SYSTEM RESEARCH','戦闘ステータス図鑑','15種類の能力の意味と計算式を、添付のステータス画面から逆引き。18職のLv65所持称号もチェックして合算できます。',stats_content,js='<script defer src="../assets/stats.js"></script>'),encoding='utf-8')

# ----- Class leveling planner -----
TRACE={1:0,5:4,10:16,15:32,20:50,25:88,30:133,35:879,40:3774,45:7873,50:14699,55:29663,60:62472,65:134405}
trace_json={'reference_date':'2026-11-06','entries':[{'level':k,'quantity':v} for k,v in TRACE.items()],'conflict':{'level':65,'another_report':156888,'remarks':'資料間不一致。Lv65累計134,405と156,888を同一条件の確定値として使用しない。'} ,'usage':'レベル間の差分は表中の対象レベル同士だけ計算できる。間のレベルは公式補間値がないため使わない。'}
(ROOT/'data/class-traces.json').write_text(json.dumps(trace_json,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
trace_options=''.join(f'<option value="{lv}">{lv}</option>' for lv in TRACE)
trace_rows=''.join(f'<tr><th>Lv{lv}</th><td>{val:,}</td><td>{(val - TRACE[list(TRACE)[i-1]]):,}' if i else f'<tr><th>Lv{lv}</th><td>0</td><td>—' for i,(lv,val) in enumerate(TRACE.items()))
# above builds table row 
trace_rows=''.join(f'<tr><th>Lv{lv}</th><td>{val:,}</td><td>{"—" if i==0 else f"+{val-list(TRACE.values())[i-1]:,}"}</td>{"<td>※別報告 156,888</td>" if lv==65 else "<td>先行実測の目安</td>"}</tr>' for i,(lv,val) in enumerate(TRACE.items()))
jobopts=''.join(f'<option value="{x["slug"]}">{x["name"]}</option>' for x in JOBS)
growth_content=f'''<nav class="doc-jumps"><a href="#trace-calc">必要個数計算</a><a href="#trace-table">目安一覧</a><a href="#growth-tactics">育成の順序</a><a href="../stats/index.html#class-title">Lv65称号</a></nav><div class="research-note"><strong>数値の出典について：</strong>精霊の痕跡の必要量は韓国・台湾の先行検証表を元にした目安です。特にLv65の累計値は<b>134,405 と 156,888</b> の2つの資料が競合しています。日本版の同条件測定ではないため、レベル間を勝手に補間しません。</div><section class="portal-panel" id="trace-calc"><span class="portal-kicker">INTERACTIVE · CLASS EXP</span><h2>精霊の痕跡：育成コスト試算</h2><p>「この職をLv35からLv40にしたら何個必要？」を確認できます。必要個数は登録された節目間のみ計算します。</p><div class="sim-form"><label>クラス<select id="traceJob">{jobopts}</select></label><label>現在のクラスLv<select id="traceStart">{trace_options}</select></label><label>目標クラスLv<select id="traceGoal">{trace_options}</select></label></div><div class="growth-calc-result" id="traceResult" aria-live="polite"></div><div class="stat-flow-grid growth-miles"><div><b>Lv35まで</b><p>メダル回収と累積Lv増加を低コストで狙う候補</p></div><div><b>Lv40まで</b><p>千本剣の対象職なら、追加の約2,895個が重要</p></div><div><b>Lv65まで</b><p>所持称号。累計数には資料間の差があるので注意</p></div></div></section><section class="portal-panel" id="trace-table"><h2>Lv1からの累計必要数・先行表</h2><div class="table-scroll"><table class="research-table"><thead><tr><th>到達</th><th>累計の痕跡</th><th>前節目との差</th><th>確度</th></tr></thead><tbody>{trace_rows}</tbody></table></div><p class="muted-note">当サイトではLv1→35を879個、Lv1→40を3,774個とする表を優先掲載。別サイトの計算表にはLv35が600個の例もあるため、日本版で再測定が必要です。計算器はこの表に忠実に動作します。</p></section><section class="portal-panel" id="growth-tactics"><h2>Season 0の育成優先順位</h2><div class="guide-steps"><article><span>01</span><div><h3>本命職のスキルを整える</h3><p>日課・レイド攻略に必要なメイン職を優先し、精霊の痕跡を使わなくても上がる戦闘経験値を活用します。</p></div></article><article><span>02</span><div><h3>Lv35でメダルと累積Lvを広く回収</h3><p>転職に必要なメダルは各職Lv25/35/45/55/65。メダルを集めつつ、累積Lv675の称号を長期目標にします。</p></div></article><article><span>03</span><div><h3>千本剣の対象6職をLv40へ</h3><p>戦士／大剣戦士／剣術師／氷結術師／盗賊／デュアルブレイドを装備者本人でLv40にする、という先行報告に基づくプラン。日本版の武器ルーン説明と照合してください。</p></div></article><article><span>04</span><div><h3>Lv65称号は必要な順に</h3><p>各職の所持称号効果は永続的ですが、終盤の精霊の痕跡消費が急増します。全職65を最初の目標にしなくても大丈夫です。</p></div></article></div><div class="research-note"><b>累積675の作例：</b>氷結55 + 対象の他5職40×5 + 残り12職35×12 = 675。先行称号には攻撃+275/防御+275の報告がありますが、日本版の称号表示とクラスLv集計条件を優先してください。</div></section><section class="portal-panel"><h2>関連ページ</h2><div class="ref-links"><a href="../stats/index.html#class-title">18職Lv65称号の選択・合算 →</a><a href="../jobs/index.html">全職のスキル・ルーン・タグを見る →</a><a href="../guides/equipment.html">装備更新の考え方を見る →</a></div><p class="muted-note">根拠：本プロジェクト2026-11-06引継ぎ資料「精霊の痕跡でクラスLv1から育てる累計表」および2026-10-19調査まとめ。独立した公式必要量表は取得できていません。</p></section>'''
(ROOT/'growth/index.html').write_text(page('クラス育成と精霊の痕跡','growth','CLASS EXP · RESOURCE PLANNER','クラス育成と精霊の痕跡','Lv35・40・65の優先度と必要個数。先行表の差分を自動計算し、Lv65の矛盾する資料もそのまま残しています。',growth_content,js='<script defer src="../assets/growth.js"></script>'),encoding='utf-8')

# ----- equipment transfer workflow -----
equipment_content='''<nav class="doc-jumps"><a href="#equip-basics">装備の見分け方</a><a href="#improvement">性能改善</a><a href="#rune-workflow">ルーンの注意</a><a href="#gem-workflow">宝石とタグ</a><a href="#season-forward">S1への準備</a></nav><section class="portal-panel" id="equip-basics"><span class="portal-kicker">EQUIPMENT DECISIONS · JP SEASON 0</span><h2>落ちた装備は「本体」と「刻印」を分けて考える</h2><p>良い装備は単純にレアリティが高いものではありません。基本攻撃／防御・装備レベル・宝石穴数と、刻印中のルーン／強化値は別々に見ます。</p><div class="compare-cards"><div><strong>保管したい器</strong><h3>宝石3穴の装備</h3><p>低基礎値でも穴数が多ければ本命母体候補です。性能改善で基本性能を更新できる可能性があります。</p></div><div><strong>改善用の素材</strong><h3>高い基礎値の装備</h3><p>穴が少なくてもレベル・基礎値が高い装備は素材候補です。素材側のルーンが移るわけではありません。</p></div></div><div class="ref-links"><a href="https://mabinogimobile.nexon.co.jp/about/guide/3541622" target="_blank" rel="noopener">日本公式：良い装備は基礎性能と穴数 ↗</a></div></section><section class="portal-panel" id="improvement"><span class="portal-kicker">JP PLAY TEST · ALCHEMY</span><h2>性能改善で残るもの／取り込むもの</h2><div class="equipment-flow"><div><span class="flow-label">残す側（母体）</span><h3>育てた装備</h3><p>刻印ルーン／刻印強化ポイント／エンチャントなどは母体側を維持（実機・先行報告）。</p></div><span class="flow-arrow">＋</span><div><span class="flow-label">使う側（素材）</span><h3>高基礎値・多穴</h3><p>装備名・レベル・基礎性能・宝石穴数など、素材装備の本体性能を反映（確認範囲）。</p></div><span class="flow-arrow">→</span><div class="flow-result"><span class="flow-label">結果</span><h3>育成を残した強化装備</h3><p>材料のルーン・刻印をコピーする機能ではありません。</p></div></div><div class="research-note"><b>実例（日本実機）</b> +4・刻印+64/+32・ルーン付き母体に高Lv装備を使った際、母体の+4・刻印・ルーンを維持し基礎性能が更新された報告があります。ただし組み合わせ制限・レアリティ差・ロック状況によって材料に選べない場合があるので、結果プレビューを必ず確認してください。</div></section><section class="portal-panel" id="rune-workflow"><h2>ルーン上書きと昇級は別の操作</h2><div class="guide-steps"><article><span>01</span><div><h3>使うルーンはロック</h3><p>ルーン上書きで以前のルーンがそのまま返却されるわけではありません。ゲーム内では旧ルーンが欠片または痕跡に変換される仕様です。</p></div></article><article><span>02</span><div><h3>刻印強化ポイントは継続</h3><p>強化後に新ルーンへ上書きしても累積ポイントは維持されますが、★の差により表示+値が変わる場合があります。</p></div></article><article><span>03</span><div><h3>昇級は同名進化ではない</h3><p>同部位の結果抽選です。素材と同じルーン名が出る保証はありません。出現等級・成功率をゲーム内の結果プレビューで確認してください。</p></div></article><article><span>04</span><div><h3>ゴロの呼び声の確定機会</h3><p>台湾S0では主線で★5×3→★6の1回確定昇級が報告され、貴重な紋章ルーンを用意する戦略がありました。日本版で同じ条件かはゲーム内確認が必要です。</p></div></article></div><div class="ref-links"><a href="https://mabinogimobile.nexon.co.jp/about/guide/3541619" target="_blank" rel="noopener">日本公式：ルーンの刻印・上書き ↗</a><a href="https://mabinogimobile.nexon.co.jp/about/guide/3541618" target="_blank" rel="noopener">日本公式：刻印強化ポイント継続 ↗</a><a href="https://mabinogimobile.nexon.co.jp/about/guide/3541658" target="_blank" rel="noopener">日本公式：ルーン昇級錬金術 ↗</a></div></section><section class="portal-panel" id="gem-workflow"><h2>宝石はタグ数と再抽選タイミングが大切</h2><p>一般宝石は能力値を、スタープリズムは全能力値・最大HPに加え、スキルタグを強化します。上位化でタグ数が増える一方、タグ内容が変わる場合があります。</p><div class="compare-cards"><div><strong>序盤</strong><h3>まず空き穴を埋める</h3><p>戦闘力や基礎能力値が上がる装備を優先し、序盤の1〜2タグを深追いしすぎない。</p></div><div><strong>最終候補</strong><h3>3タグから本格厳選</h3><p>現在の職業の主力スキルに対応するタグを確認してから厳選。タグ一致はすべてのスキルに効くわけではありません。</p></div></div><p>2026年11月4日の日本版更新では、装着中の宝石を錬金術の素材1番目として選び、結果を元のスロットに装着できる操作改善がありました。以前の手順をそのまま使わず、現在の画面を確認してください。</p><div class="ref-links"><a href="https://mabinogimobile.nexon.co.jp/about/guide/3541621" target="_blank" rel="noopener">日本公式：宝石システム ↗</a><a href="https://mabinogimobile.nexon.co.jp/news/update/3575405?pageNo=1" target="_blank" rel="noopener">日本公式：11月4日の宝石錬金術変更 ↗</a><a href="../jobs/index.html">職業別タグ・スキルを確認 →</a></div></section><section class="portal-panel" id="season-forward"><h2>Season 1に持ち越すとき</h2><div class="research-note"><b>韓国の実績であり日本版未実装：</b>★8ルーン用の「記憶刻印」や「ルーンワード」、2025年11月13日開始の「ルーン超越」は日本S0の★6伝説をそのまま超越できるという意味ではありません。今育成した装備を全て無駄と決めつける前に、該当シーズンの仕様差を確認してください。</div><p>韓国の超越素材は武器/エンブレムと防具/アクセサリーで必要量が異なります。実装日・詳細は<a href="../content/season1.html">韓国Season 1の履歴</a>と<a href="../guides/rune-transcend.html">超越・昇級の比較表</a>へ。</p></section>'''
(ROOT/'guides/equipment.html').write_text(page('装備更新と性能改善','equipment','GEAR SYSTEM · JP SEASON 0','装備更新・性能改善の判断','宝石3穴と基礎性能の見分け方から、母体を残す性能改善、ルーン上書き、宝石タグ厳選までを一続きで。',equipment_content),encoding='utf-8')

# ----- Battle mechanics -----
battle_content='''<nav class="doc-jumps"><a href="#damage-chain">ダメージの流れ</a><a href="#hit-flags">判定と発動条件</a><a href="#break-window">ブレイク中</a><a href="#field-test">試すときの条件</a></nav><section class="portal-panel" id="damage-chain"><h2>ひとつの攻撃に、複数の判定が重なる</h2><p>基本攻撃力・スキル威力のあとに、強打・連打・マルチヒット・クリティカル・追加攻撃・ノーガードなどの判定が重なることがあります。各判定の条件を満たしていなければ、対応する能力値を上げてもその攻撃には効きません。</p><div class="battle-chain"><div>基本攻撃・スキル係数</div><span>→</span><div>強打／連打／範囲／コンボ</div><span>→</span><div>クリティカル／追加攻撃</div><span>→</span><div>ブレイク・敵の防御など</div></div><p class="muted-note">上図は概念図です。正確な演算順序を断定しません。数式による実際の比較は<a href="../tools/damagecalc.html">非公式ダメージ計算</a>を参照してください。</p></section><section class="portal-panel" id="hit-flags"><h2>主な戦闘判定の使い分け</h2><div class="battle-grid"><article><b>強打</b><p>一度の攻撃が一定以上の威力になったとき成立する判定。<a href="../stats/index.html#stat-strong">強打強化</a>が有効。</p></article><article><b>連打</b><p>短時間で一定回数の攻撃を重ねた場合の判定。多段技や追加ヒットとの組合せが重要。</p></article><article><b>マルチヒット（広域）</b><p>同一スキルで複数の敵を攻撃したときの判定。単体ボス戦と雑魚集団で有効性が変わります。</p></article><article><b>クリティカル</b><p>確率で強いヒットが発生。能力値で確率と倍率の両方が変わる非公式モデルがあります。</p></article><article><b>追加攻撃</b><p>一定確率で追加の攻撃判定を発生。連打判定やDoTとは仕組みが違います。</p></article><article><b>急所回避</b><p>敵から受けたダメージを一部軽減する判定。完全回避とは区別してください。</p></article><article><b>カウンター</b><p>敵がスキルを準備している間に攻撃した場合などに発生する判定。</p></article><article><b>クロス</b><p>こちらがスキルを準備している間に攻撃を受けた場合の判定。カウンターとは別です。</p></article></div><div class="ref-links"><a href="https://mabinogimobile.nexon.com/Info/Guide/2751060" target="_blank" rel="noopener">韓国公式：ダメージ判定一覧 ↗</a></div></section><section class="portal-panel" id="break-window"><h2>ブレイクは「ゲージ削り」と「無防備中の火力」が別</h2><div class="compare-cards"><div><strong>ブレイク前</strong><h3>ゲージを削る</h3><p>ブレイクゲージを満たして敵の体勢を崩します。ブレイク能力値がゲージ削りへどの程度反映するか、内部式は未確定です。</p></div><div><strong>ブレイク後</strong><h3>無防備に畳みかける</h3><p>ブレイク中の敵へ与えるダメージには、ブレイク能力値やノーガード増加、ブレイク種別の追加効果などが関係します。</p></div></div><div class="research-note"><b>韓国非公式式：</b>無防備の基本項 <code>1 + ブレイク / 5250</code>、これにノーガード・種別ボーナス等を加えるモデルがあります。数値を+5250すれば戦闘中ずっと2倍になる、という意味ではありません。</div><p>レイドなどの実戦では、ブレイク時間中に究極技を集中する戦い方と、CTを優先して常時回す戦い方を比較すると良いでしょう。</p></section><section class="portal-panel" id="field-test"><h2>実際に比べるなら、これだけ固定</h2><div class="guide-steps"><article><span>01</span><div><h3>同じ敵、同じ難度</h3><p>敵防御力・推奨戦闘力・ブレイク状態が変わると数値が揃いません。</p></div></article><article><span>02</span><div><h3>同じスキル、同じ状態</h3><p>スキルLv・ルーン、DoT・バフの有無、クリ判定、弱点、コンボ段階を揃えます。</p></div></article><article><span>03</span><div><h3>単発ダメージと総DPSを区別</h3><p>スキル1発の倍率が上がっても、モーションが遅くなれば時間あたりの火力が落ちる可能性があります。</p></div></article></div><p>「戦闘力が下がったのにDPSが上がった」という比較は十分あり得ます。実測ログがあれば、<a href="../stats/index.html">ステータス解説</a>と<a href="../tools/damagecalc.html">ダメージ計算</a>を併用してください。</p></section>'''
(ROOT/'guides/battle.html').write_text(page('戦闘判定とブレイク','battle','HIT TYPE · COMBAT MECHANICS','戦闘判定とブレイクの仕組み','強打・連打・マルチヒット・クリティカル・追加攻撃・ノーガード。どのステータスがどの攻撃に効くかを整理します。',battle_content),encoding='utf-8')

# ----- Season 1 rune upgrade -----
transcend='''<nav class="doc-jumps"><a href="#season-separation">S0とS1の違い</a><a href="#season-upgrade">昇級</a><a href="#season-memory">記憶刻印</a><a href="#season-transcend">超越刻印</a></nav><div class="research-note"><b>韓国実績の研究ページ：</b>以下は韓国2025-09-25～2025-11-13のSeason 1を中心にした情報です。日本版S0で今すぐできる操作とは限りません。日本・台湾は時点を分けます。</div><section class="portal-panel" id="season-separation"><h2>まず3つの用語を区別</h2><div class="compare-cards"><div><strong>通常ルーン昇級</strong><h3>素材を投入して抽選</h3><p>結果のルーンを得る工程。素材と同じ名前のルーンになる保証はありません。</p></div><div><strong>記憶刻印（S1）</strong><h3>記憶済み固有効果へ切替</h3><p>韓国S1の★8記憶対象。既存刻印の強化値そのものをコピーする機能ではありません。</p></div><div><strong>超越刻印（S1後発）</strong><h3>伝説ルーン固有効果を強化</h3><p>韓国2025-11-13追加。主にS1★8伝説を2段階で+、++へ強化する仕組み。</p></div></div></section><section class="portal-panel" id="season-upgrade"><h2>シーズンをまたぐ昇級の候補</h2><div class="table-scroll"><table class="research-table"><thead><tr><th>素材</th><th>結果と確率（韓国S1先行）</th><th>注意</th></tr></thead><tbody><tr><th>★5エピック×3</th><td>S0★6伝説10% ／ S1★6エリート40% ／ S1★5レア50%</td><td>「何かは100%」で伝説確定ではない</td></tr><tr><th>S0★6伝説×3</th><td>S1★7エピック40% ／ S1★6エリート60%</td><td>日本版への適用は未発表</td></tr></tbody></table></div><p class="muted-note">この確率はプロジェクトの2026-11-06引継ぎ資料にある過去調査値です。韓国公式の当時の確率画面を現在再検証できていないため、日本版実装時には必ずゲーム内の昇級成功率を見てください。</p></section><section class="portal-panel" id="season-memory"><h2>★8の記憶刻印・ルーンワード</h2><p>韓国Season 1で記憶対象となったルーンは、新しいシーズンの★8伝説・神話ルーン群です。<b>Season 0の★6「千本剣」をそのまま記憶対象として使えるとは限りません。</b></p><p>刻印側の強化値と、切り替えて使うルーンの固有効果を別管理する方向の仕組みです。ゴールド費用・切替回数について、完全無料・無制限であることまでは確定していません。</p></section><section class="portal-panel" id="season-transcend"><h2>ルーン超越：2段階の必要素材（韓国実績）</h2><div class="table-scroll"><table class="research-table"><thead><tr><th>部位</th><th>伝説 → +</th><th>+ → ++</th></tr></thead><tbody><tr><th>武器・エンブレム</th><td>精髄5 + 装飾1</td><td>精髄14 + 装飾+1</td></tr><tr><th>防具・アクセサリー</th><td>精髄3 + 装飾1</td><td>精髄8 + 装飾+1</td></tr><tr><th>ゴールド（共通）</th><td>200,000</td><td>500,000</td></tr></tbody></table></div><p>成功率100%とされた先行仕様。★8のまま固有効果を強化し、元の武器基礎攻撃力を直接上げる仕組みではありません。S0★6・S1神話★8が同条件で対象というわけではありません。</p><p>例：韓国の先行DBでは「古代の守護者」伝説の攻撃+23%が++では+27%など、ルーンごとに固有効果の変化が異なりました。伝説++がすべての神話より強いわけではありません。</p><div class="ref-links"><a href="https://mabinogimobile.nexon.com/Info/Guide/3220932" target="_blank" rel="noopener">韓国公式：ルーン超越ガイド ↗</a><a href="https://mabinogimobile.nexon.com/News/Update/3147463" target="_blank" rel="noopener">韓国公式：Season 1開始時の更新 ↗</a><a href="../content/season1.html">韓国S1実装時系列へ →</a></div></section>'''
(ROOT/'guides/rune-transcend.html').write_text(page('韓国Season 1 ルーン昇級と超越','content','SEASON 1 · KOREA RECORD','S1ルーン昇級・記憶・超越','新シーズンのルーン強化工程を分離。S0の★6ルーンとS1の★8ルーンを同じ操作として扱わないための先行資料です。',transcend),encoding='utf-8')

# ---- Shared nav, home, content hub and README ---
navpath=ROOT/'assets/site.js'
js=navpath.read_text(encoding='utf-8')
js=js.replace("['jobs/index.html','職業別攻略','jobs'],['content/index.html','コンテンツ','content']", "['jobs/index.html','職業別攻略','jobs'],['stats/index.html','ステータス','stats'],['growth/index.html','クラス育成','growth'],['guides/equipment.html','装備更新','equipment'],['content/index.html','コンテンツ','content']")
navpath.write_text(js,encoding='utf-8')
home=ROOT/'index.html'
home_txt=home.read_text(encoding='utf-8')
insert='''<a class="home-card home-stat-feature" href="stats/index.html"><div class="icon" aria-hidden="true">◈</div><div class="label">SYSTEM · 15 COMBAT STATS</div><h2>キャラステータス図鑑</h2><p>添付のステータス画面を再現。15能力の意味と非公式換算式、18職Lv65称号の合算・数値比較をひとつのページに。</p><div class="go">ステータスを調べる →</div></a>
<a class="home-card" href="growth/index.html"><div class="icon" aria-hidden="true">✧</div><div class="label">GROWTH · CLASS EXP</div><h2>クラス育成と精霊の痕跡</h2><p>Lv35・40・65までの必要個数を計算。累積Lv675・千本剣の準備と、矛盾する先行資料も整理。</p><div class="go">必要個数を計算 →</div></a>
<a class="home-card" href="guides/equipment.html"><div class="icon" aria-hidden="true">⚒</div><div class="label">GUIDES · EQUIPMENT</div><h2>装備更新・性能改善</h2><p>宝石穴・基礎攻撃・刻印の引き継ぎ判断。3穴装備を残す理由から上書き事故の防止まで。</p><div class="go">更新手順を見る →</div></a>
<a class="home-card" href="guides/battle.html"><div class="icon" aria-hidden="true">⚡</div><div class="label">COMBAT · HIT TYPES</div><h2>戦闘判定とブレイク</h2><p>強打、連打、広域、クリティカル、追加攻撃の発動条件。どのステータスが有効かを分かりやすく。</p><div class="go">戦闘の仕組みを見る →</div></a>
<a class="home-card" href="guides/rune-transcend.html"><div class="icon" aria-hidden="true">◇</div><div class="label">KOREA · SEASON 1</div><h2>ルーン記憶・超越・昇級</h2><p>韓国S1の★8ルーン、伝説++の超越必要素材と、S0からの昇級を整理。</p><div class="go">先行仕様を読む →</div></a>
'''
if 'home-stat-feature' not in home_txt:
 home_txt=home_txt.replace('  <a class="home-card home-job-feature"',insert+'  <a class="home-card home-job-feature"')
home_txt=home_txt.replace('今後はルーン単位の厳密なドロップ表や動画検証を増やします。','新たにステータス図鑑・精霊の痕跡計画・装備更新・戦闘判定を追加しました。今後も実機検証で未確定値を埋めます。')
home.write_text(home_txt,encoding='utf-8')
content_index=ROOT/'content/index.html'
t=content_index.read_text(encoding='utf-8')
if 'S1ルーン超越</a></nav>' not in t:
 t=t.replace('<a href="../tools/weeklyplanner.html">週数計算ツール</a></nav>', '<a href="../tools/weeklyplanner.html">週数計算ツール</a><a href="../guides/rune-transcend.html">S1ルーン超越</a></nav>')
if '関連の新しい研究ページ' not in t:
 t=t.replace('<section class="portal-panel content-intro"><h2>いま覚えておくポイント</h2>', '<section class="portal-panel content-intro"><h2>関連の新しい研究ページ</h2><p><a href="../stats/index.html">ステータス図鑑</a> ／ <a href="../growth/index.html">クラス育成・精霊の痕跡</a> ／ <a href="../guides/equipment.html">装備更新</a> ／ <a href="../guides/rune-transcend.html">韓国S1ルーン超越</a></p></section><section class="portal-panel content-intro"><h2>いま覚えておくポイント</h2>')
content_index.write_text(t,encoding='utf-8')
season=ROOT/'content/season1.html';t=season.read_text(encoding='utf-8');t=t.replace('</footer>', '</footer>')
if '追補：2025年11月13日のルーン超越' not in t:
 t=t.replace('<section class="portal-panel content-intro"><h2>個別ルーンの出現先を断定していない理由</h2>', '<section class="portal-panel content-intro"><h2>追補：2025年11月13日のルーン超越</h2><p>韓国S1の初日ではなく、2025年11月13日に固有効果を段階強化する「ルーン超越」が追加されました。★8伝説の伝説→+→++に必要な精髄・装飾・ゴールドは、<a href="../guides/rune-transcend.html">S1ルーン記憶・昇級・超越の比較ページ</a>に整理しました。</p></section><section class="portal-panel content-intro"><h2>個別ルーンの出現先を断定していない理由</h2>')
season.write_text(t,encoding='utf-8')

readme=ROOT/'README.md'
if not readme.read_text(encoding='utf-8').startswith('# エリン調査ノート v7'):
 readme.write_text('''# エリン調査ノート v7 — ステータス・クラス育成・装備・戦闘判定（2026-11-06）

## v7で追加したページ

| URL | 内容 |
|---|---|
| `stats/index.html` | **添付画像のステータス15種類**／公式の効果説明／非公式の換算式／数値試算／18職Lv65称号チェック・合算 |
| `growth/index.html` | 精霊の痕跡の必要数と各職Lv35/40/65の育成方針／差分計算 |
| `guides/equipment.html` | 3穴装備・性能改善・刻印／ルーン昇級／宝石タグ |
| `guides/battle.html` | 強打・連打・範囲・追加攻撃・ブレイク／無防備の関係 |
| `guides/rune-transcend.html` | 韓国S1ルーン昇級・記憶・超越（日本版未実装） |

### 既存機能の保持
- `jobs/` 18職（スキル・ルーン・宝石タグ・ペット・戦い方と先行採用率）
- `runes/index.html` 530件のルーン図鑑
- `content/` 解放スケジュール・ルーン入手先・S1履歴
- `tools/` ダメージ計算・交換週数計算
- データはHTMLと同一配下のローカルJSON。GitHub Pagesで静的配信。

### 確度と注意事項
1. 日本公式は **STRなど5主能力と15副能力の対応関係** を公開。ただし、主能力+100 → 副能力+何ポイント、という全般的な変換係数は公表していません。
2. 副能力から%へ換算する式は韓国SNOMETやWikiの**非公式モデル**。日本版現行式の保証はありません。防御式は2説が併存。急所回避は公式説明の「ダメージ一部軽減」を採用しています。
3. `data/class-titles.json` の**職別+25×2**はプロジェクトの「氷結術師攻略本 v1.4 CH05」「総合引継ぎ2026-10-19」由来の韓国先行値。日本公式が確認しているのは「Lv65で永続称号を獲得」という一般仕様です。チェックはブラウザ内だけに保存されます。
4. `data/class-traces.json` は**Lv65の累計134,405と156,888の矛盾**を残した資料値です。補間はしません。
5. 韓国S1ページは日本で実装済みと主張するものではありません。

### データ編集と再生成
```
python scripts/build_v7.py       # 新規5ページとトップ・ナビを生成
python scripts/rebuild_jobs.py   # 既存職業ガイドを更新した場合のみ
```

※ `build_v7.py` は新規ページとデータを再生成します。既存サイトのナビ・ホームは重複を避けて変更します。サイトを配布・編集する場合は生成されたHTML・JSON・CSS・JSを直接更新して問題ありません。

### 情報源
- 日本公式基本ステータス: https://mabinogimobile.nexon.co.jp/about/guide/3541615
- 日本公式クラス成長: https://mabinogimobile.nexon.co.jp/about/guide/3541625
- 日本公式タイトル: https://mabinogimobile.nexon.co.jp/about/guide/3541613
- 韓国公式ダメージ判定: https://mabinogimobile.nexon.com/Info/Guide/2751060
- 韓国非公式ステータス・ダメージ式: https://www.snomet.kr/mobi/stat
- 日本公式ルーン: https://mabinogimobile.nexon.co.jp/about/guide/3541619
- 日本公式刻印強化: https://mabinogimobile.nexon.co.jp/about/guide/3541618
- 日本公式錬金術: https://mabinogimobile.nexon.co.jp/about/guide/3541658
- プロジェクトMD資料: 2026-10-19、10-23、10-27、10-29、11-01、11-06 引継ぎ。

---

'''+readme.read_text(encoding='utf-8'),encoding='utf-8')
print('Generated',*[str(x.relative_to(ROOT)) for x in (ROOT/'stats/index.html',ROOT/'growth/index.html',ROOT/'guides/equipment.html',ROOT/'guides/battle.html',ROOT/'guides/rune-transcend.html')])
