#!/usr/bin/env python3
"""Rebuild jobs/index.html and 18 jobs/*.html from data/job-builds.json + data/job-guides.json.

Run from any working directory: python scripts/rebuild_jobs.py
Requires: beautifulsoup4 (pip install beautifulsoup4)
No network access. Other existing portal files are unchanged. Paths are relative to this site root.
"""
from pathlib import Path
import html, json, re, urllib.parse
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
SOURCE='https://erinn.tw/runes'
WEBSITE='https://mabinogimobile.nipponhashi.com/ja/runes/'
STATS_DATE='2026-11-01'
jobs=json.loads((ROOT/'data/job-builds.json').read_text(encoding='utf-8'))['jobs']
guides=json.loads((ROOT/'data/job-guides.json').read_text(encoding='utf-8'))['jobs']
combat=json.loads((ROOT/'data/combat-guides.json').read_text(encoding='utf-8'))['jobs']
skilldata=json.loads((ROOT/'data/job-skills.json').read_text(encoding='utf-8'))['jobs']
soup=BeautifulSoup((ROOT/'runes/index.html').read_text(encoding='utf-8'),'html.parser')
catalog=json.loads(soup.select_one('#runeDataset').string)
rune_by_name={r['name']:r for r in catalog}
def esc(text):return html.escape(str(text),quote=True)
def pct(rate):return f'{rate:.1f}%'
def link_to_rune(name):
    canonical=re.sub(r'（対訳暫定）$', '', name)
    if canonical in rune_by_name:
        return f'../runes/index.html?q={urllib.parse.quote(canonical)}'
    return None

def colored_name(item,heading=False):
    name=item['name'];href=link_to_rune(name)
    if href:return f'<a class="job-rune-link" href="{esc(href)}" title="ルーン図鑑で検索">{esc(name)}</a>'
    return f'<span class="job-rune-name">{esc(name)}</span>'

def rate_item(rec,slot,idx):
    name=rec['name'];rate=rec['rate'];shortdesc=''
    canonical=re.sub(r'（対訳暫定）$', '', name)
    if canonical in rune_by_name and slot=='accessory' and idx < 3:
        shortdesc=f'<p class="job-effect"><span class="job-effect-label">日本語図鑑の基本効果</span>{esc(rune_by_name[canonical]["effect"])}</p>'
    if '対訳暫定' in name:
        shortdesc+='<p class="job-effect job-uncertain">台湾版と日本版の対訳は暫定対応です。実際のルーン名を確認してください。</p>'
    elif '未照合' in name:
        shortdesc='<p class="job-effect job-uncertain">日本語ルーン名との照合前。％を別名のルーンへ転用しないでください。</p>'
    return (f'<div class="job-rank" data-rune="{esc(name)}"><div class="job-rank-main">'
            f'<span class="job-rank-no">{idx+1:02d}</span><span class="job-rank-title">{colored_name(rec)}'
            f'</span><strong class="job-rank-rate">{pct(rate)}</strong></div>'
            f'<div class="job-meter" aria-hidden="true"><span style="width:{min(max(rate,0),100)}%"></span></div>'
            f'{shortdesc}</div>')

def section(title,kicker,arr,slot,desc):
    return (f'<section class="portal-panel job-stats-card"><div class="job-section-heading"><div><div class="portal-kicker">{esc(kicker)}</div><h2>{esc(title)}</h2></div><span class="portal-pill">{len(arr)}件表示</span></div>'
            f'<p class="job-section-help">{esc(desc)}</p><div class="job-rank-list">'+ ''.join(rate_item(x,slot,i) for i,x in enumerate(arr)) + '</div></section>')

def page_doc(title,body,relative='../',key='jobs',desc=''):
    return ('<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    '<meta name="theme-color" content="#09111e"><title>'+esc(title)+'</title><meta name="description" content="'+esc(desc)+'">'
    f'<link rel="stylesheet" href="{relative}assets/site.css"><script defer src="{relative}assets/site.js"></script></head><body>'
    f'<div id="siteNav" data-current="{key}" data-root="{relative}"><a href="{relative}index.html">ホーム</a></div>'
    f'<main class="portal-wrap">{body}</main></body></html>')


def combat_detail(job):
    x=combat[job['slug']]
    steps=[('01','開幕／準備',x['opening']),('02','主力の回し方',x['rotation']),('03','オートとの併用',x['auto'])]
    cards=''.join('<div class="combat-step"><span>'+n+'</span><div><h3>'+esc(t)+'</h3><p>'+esc(v)+'</p></div></div>' for n,t,v in steps)
    return ('<section class="portal-panel combat-card" id="combat-guide"><div class="job-section-label">COMBAT PLAYBOOK · SEASON 0</div><h2>実戦の戦い方・半オート運用</h2>'
        '<p class="job-guide-sub">固定コンボではなく、手動で仕込む操作とオートへ任せる部分を整理しています。</p>'
        '<div class="combat-steps">'+cards+'</div><p class="combat-tip"><strong>運用のコツ：</strong>'+esc(x['tip'])+'</p>'
        '<div class="job-guide-basis">'+esc(x['confidence'])+'。'+esc(x['warning'])+'</div></section>')

def skill_detail(job):
    """S0 skill / accessory rune matrix. Tags and exact slots are shown ONLY when independently verified."""
    info=skilldata[job['slug']]
    primary={int(x) for x in guides[job['slug']]['specialization']['primary'] if x in '123456'}
    fixed=set(guides[job['slug']]['specialization']['fixed'])
    gemtags=[x['tag'] for x in guides[job['slug']]['gems']['priorities']]
    cards=[]
    for i,skill in enumerate(info['skills']):
        number=skill.get('slot')
        is_main=bool(number and number in primary)
        runes=skill['runes']
        label=(f'<span class="skill-index">{number:02d}</span>' if number else '<span class="skill-index skill-index-unknown" title="このスキルの番号は未照合">—</span>')
        tags=(''.join(f'<span class="skill-tag">{esc(t)}</span>' for t in skill['tags'])
            if skill['tags'] else '<span class="skill-tag skill-tag-unverified">個別タグ：要実機確認</span>')
        desc=skill['description'] or '日本語のスキル名と対応ルーンを照合済みです。ルーン未装着時の基本効果は確認中のため、以下の改造効果と混同しないでください。'
        content=[]
        for r in runes:
            href=link_to_rune(r['name'])
            rname=(f'<a href="{esc(href)}">{esc(r["name"])}</a>' if href else esc(r['name']))
            content.append('<div class="skill-rune-entry"><div class="skill-rune-head"><strong>'+rname+'</strong><span class="portal-pill">'+esc(r['grade'])+'</span></div>'
                '<p>'+esc(r['effect'])+'</p></div>')
        if not content:
            content=['<p class="skill-empty">現在の日本版ルーン図鑑では、このスキルを直接変更する専用アクセサリールーンを確認できていません。</p>']
        captions=[]
        if is_main:captions.append('<span class="skill-reco">基本特化の対象</span>')
        if number in fixed:captions.append('<span class="skill-fixed">優先固定</span>')
        cards.append('<article class="skill-entry" id="skill-entry-'+str(i+1)+'"><div class="skill-entry-head">'+label+'<div class="skill-entry-title"><h3>'+esc(skill['name'])+'</h3>'
            +''.join(captions)+'</div></div><div class="skill-tags"><b>スキルタグ</b>'+tags+'</div>'
            '<p class="skill-base">'+esc(desc)+'</p><div class="skill-rune-group"><h4>対応アクセサリールーン・改造効果</h4>'+''.join(content)+'</div></article>')
    tag_map={}
    for skill in info['skills']:
        for tag in skill.get('tags',[]):
            tag_map.setdefault(tag,[]).append((skill['name'],skill.get('slot')))
    covered=''.join('<div class="skill-tag-coverage-row"><b>'+esc(tag)+'</b><span>'+esc('・'.join((f"{number} {name}" if number else name) for name,number in entries))+'</span></div>' for tag,entries in tag_map.items())
    coverage=('<div class="skill-tag-coverage"><h3>タグ別：どのスキルが強化対象？</h3>'+covered+'<small>照合済みのスキルだけ表示しています。空欄は「そのタグがない」ことの証明ではありません。タグ変更ルーン装着後は再確認してください。</small></div>' if covered else '')
    intro=(f'<section class="portal-panel class-skill-panel" id="skill-dictionary"><div class="job-section-label">SKILL ENCYCLOPEDIA · JAPAN S0</div>'
      f'<h2>スキルと対応ルーンの詳細</h2><p>「スキル名 → 基本動作 → 対応ルーン → 変化する効果」の順に確認できます。'
      f'既存の日本語ルーン図鑑に収録された<strong>日本版実装扱いのアクセサリールーン</strong>をスキル名で照合しています。</p>'
      f'<div class="skill-legend"><span>確認できたスキル名：<b>{len(info["skills"])}件</b></span><span>対応ルーン効果：<b>{sum(len(x["runes"]) for x in info["skills"])}件</b></span></div>'
      f'<p class="skill-legend-tip">職全体の推奨タグ：<b>{esc(" → ".join(gemtags))}</b>。これはクラス単位のおすすめです。'
      '各スキルの個別タグや①〜⑥の番号は、裏付けがあるものだけ明記しました。未確認欄は推奨タグから推定して埋めていません。'
      'ルーンによってタグ・スキル名・攻撃方式が変わる場合は、日本版の装着後画面を最優先してください。</p>'
      '<div class="skill-filter-note"><span class="skill-reco">基本特化の対象</span>＝上記「おすすめスキル特化」に含まれる番号。'
      '番号が「—」のスキルは未確認であり、特化対象外という意味ではありません。</div>')
    footer='<div class="skill-sources"><strong>スキル名・説明の参照先：</strong><a href="'+esc(info['source_gamewith'])+'" target="_blank" rel="noopener noreferrer">GameWith・'+esc(job['name'])+'のスキル一覧</a>。'
    footer+='<strong>ルーン効果・名称：</strong><a href="'+esc(info['source_runes'])+'" target="_blank" rel="noopener noreferrer">アリス氏の日本語ルーンDB（CC BY 4.0）</a>。'
    if job['slug']=='frostmage':
        footer+='<a href="https://mabinogimobile.nipponhashi.com/ja/guides/frostmage-gem-tags/" target="_blank" rel="noopener noreferrer">氷結術師タグの先行検証</a>。'
    if job['slug']=='healer':
        footer+='<a href="https://mabinogimobile.nipponhashi.com/ja/guides/healer-s0-build/" target="_blank" rel="noopener noreferrer">ヒーラーのスキル番号</a>。'
    return intro+coverage+'<div class="skill-entries">'+''.join(cards)+'</div><p class="skill-sources">'+footer+'</p></section>'

def guide_detail(job):
    """Independent editorial advice; adoption percentages are never inferred from this."""
    guide=guides[job['slug']]
    sk=guide['specialization']; gem=guide['gems']; pets=guide['pets']
    # Skill highlighting is based on primary three digits; the fixed numbers are independently highlighted in text.
    chosen={int(n) for n in sk['primary'] if n in '123456'}
    slots=''.join(f'<span class="job-skill-slot {"is-active" if n in chosen else ""} {"is-core" if n in sk["fixed"] else ""}" aria-label="スキル{n}{" 推奨" if n in chosen else ""}">{n}</span>' for n in range(1,7))
    alts=''.join('<div class="job-alt-row"><div><strong>'+esc(a['label'])+'</strong><span>'+esc(a['why'])+'</span></div><b>'+esc(a['slots'])+'</b></div>' for a in sk['alternatives'])
    specials=('<section class="portal-panel job-guide-card" id="skill-guide"><div class="job-section-label">01 · SKILL SPECIALIZATION</div><h2>おすすめスキル特化</h2>'
       '<p class="job-guide-sub">ルーン刻印のスキル強化位置。固定したい枠と、用途で変える枠を分けています。</p>'
       '<div class="job-priority"><div><span>基本構成</span><strong>'+esc(sk['primary'])+'</strong><small>固定枠：'+('・'.join(''+str(i) for i in sk['fixed']))+'</small></div><div class="job-skills">'+slots+'</div></div>'
       +(f'<div class="job-alternates"><h3>用途別の入れ替え</h3>{alts}</div>' if alts else '')
       +'<p class="job-guide-note">'+esc(sk['note'])+'</p>'
       '<div class="job-guide-basis">参考：'+esc(sk['basis'])+'。固定3枠にこだわるより、主力2枠を優先する育成も有効です。</div></section>')
    names=['第一候補','第二候補','第三候補']
    gems='<div class="job-gem-rows">'+''.join(f'<div class="job-gem-row"><span class="job-gem-rank">{i+1:02d}</span><strong>{esc(t["tag"])}</strong><span class="job-gem-marker">{names[i] if i<len(names) else "候補"}</span></div>' for i,t in enumerate(gem['priorities']))+'</div>'
    gemhtml=('<section class="portal-panel job-guide-card" id="gem-guide"><div class="job-section-label">02 · GEM TAGS</div><h2>おすすめ宝石タグ</h2>'
        '<p class="job-guide-sub">スタープリズムは主力スキルに付いているタグを優先します。順位は最適化の目安です。</p>'
        +gems+'<p class="job-guide-note">'+esc(gem['note'])+'</p>'
        +'<div class="job-guide-basis">'+esc(gem['basis'])+'。ダメージタグとクールタイム短縮は効果を区別してください。</div></section>')
    petcards=''.join('<div class="job-pet-item"><div class="job-pet-meta"><span class="job-pet-position">'+esc(pet['label'])+'</span><span class="job-pet-state">'+esc(pet['status'])+'</span></div><h3>'+esc(pet['name'])+'</h3><p class="job-pet-stat">'+esc(pet['stats'])+'</p></div>' for pet in pets['candidates'])
    pethtml=('<section class="portal-panel job-guide-card" id="pet-guide"><div class="job-section-label">03 · COMPANION PETS</div><h2>おすすめ同行ペット</h2>'
        '<p class="job-guide-sub">この欄は<span class="job-no-rate">職別の採用率ではありません</span>。同行ステータスと主力攻撃の相性で選んだ候補です。</p>'
        '<div class="job-pet-list">'+petcards+'</div><p class="job-guide-note">'+esc(pets['note'])+'</p>'
        +'<div class="job-guide-basis">'+esc(pets['basis'])+' 種類・等級・固有スキル・一般スキルを実際の個体で確認してください。</div></section>')
    return '<div class="job-guide-grid">'+specials+gemhtml+'</div>'+pethtml

for i,job in enumerate(jobs):
    pre=jobs[(i-1)%len(jobs)];nxt=jobs[(i+1)%len(jobs)]
    essential=job['accessory'][:3]
    supplement=job['accessory'][3:]
    rec=('<section class="portal-panel job-top-picks" id="build-guide"><div class="portal-kicker">SEASON 0 · STARTING BUILD</div><h2>まず検討したい構成</h2>'
    '<p class="job-regular">下記は採用状況と過去の職別検証から作成した<strong>検討用の初期セット</strong>です。DPS最適解の確定表ではありません。</p>'
    '<div class="job-setup"><div class="job-setup-item"><span>武器候補</span><strong>'+esc(job['weapon'][0]['name'])+'</strong></div>'
    '<div class="job-setup-item"><span>エンブレム候補</span><strong>'+esc(job['emblem'][0]['name'])+'</strong></div>'
    '<div class="job-setup-item job-setup-wide"><span>アクセサリー・優先候補（3枠）</span><strong>'+' ＋ '.join(esc(x['name']) for x in essential)+'</strong></div>'
    '<div class="job-setup-item job-setup-wide"><span>防具・採用上位の検討候補（5種類）</span><strong>'+' ／ '.join(esc(x['name']) for x in job['armor'][:5])+'</strong></div></div>'
    f'<p class="job-note">{esc(job["note"])}</p></section>')
    overview=('<section class="job-hero"><div class="job-breadcrumb"><a href="../index.html">ホーム</a> / <a href="index.html">職業別おすすめ</a> / '+esc(job['name'])+'</div>'
    '<div class="job-hero-inner"><span class="job-hero-icon" aria-hidden="true">'+job['icon']+'</span><div><div class="portal-kicker">'+esc(job['family'])+' · RUNE BUILDS</div>'
    '<h1 class="portal-page-title">'+esc(job['name'])+'の攻略ガイド</h1><p class="portal-lead">'+esc(job['role'])+'。ルーン・スキル名・改造ルーンの効果・スキル特化・宝石タグ・同行ペットを、台湾のルーン採用率と分けてまとめています。</p></div></div>'
    '<div class="job-hero-chips"><span class="portal-pill">戦い方</span><span class="portal-pill">スキル特化</span><span class="portal-pill">宝石タグ</span><span class="portal-pill">同行ペット</span><span class="portal-pill">スキル・対応ルーン</span><span class="portal-pill">台湾の採用傾向</span><span class="portal-pill">2026-11-01取得</span></div></section>')
    explanations='<div class="job-warning"><strong>読み方：</strong>採用率は台湾の公開ランキングに基づく数値で、各ルーンを装備している割合です。日本版の使用率ではありません。アクセサリー・防具は複数枠なので合計100%にはなりません。アクセサリーは台湾の主に「＋」版の率です。日本語図鑑にある基本効果は参照用で、＋版の追加数値・性能と同一視しないでください。千本剣には対象職のクラスLv条件もあります。</div>'
    block=('<div class="job-columns">'+section('アクセサリー採用ランキング','ACCESSORIES',job['accessory'],'accessory','候補の上位3つが基本セットの参考値。4位以下も運用を変える選択肢です。')+
    section('防具採用ランキング','ARMOR',job['armor'],'armor','防具は5枠です。上位から5つを無条件に固定せず、セット効果・発動条件を確認します。')+'</div>')
    tail=('<div class="job-columns">'+section('武器の採用傾向','WEAPON',job['weapon'],'weapon','高採用ルーンが必ずしも全コンテンツで最大DPSになるとは限りません。')+
    section('エンブレムの採用傾向','EMBLEM',job['emblem'],'emblem','火力・サポート・耐久の目的に合わせた比較が必要です。')+'</div>')
    links=('<section class="portal-panel job-source"><h2>出典・補足</h2><p>採用率：<a href="'+SOURCE+'" target="_blank" rel="noopener noreferrer">愛爾琳網／瑪奇 Mobile 符文採用排行（台湾）</a>、2026年11月1日参照。原サイトの順位と割合を独自レイアウトで日本語整理した静的スナップショットです。集計母数・対象プレイヤー・更新条件は必ず出典側で確認してください。</p>'
    '<p>スキル特化・宝石タグの参考：<a href="https://mabinogimobile.nipponhashi.com/ja/guides/jp-launch-class-quickstart/" target="_blank" rel="noopener noreferrer">マビノギモバイル Wiki DB・18職クイックスタート</a>（韓国S0期を基準にした日本版向け編集）。同行ペット：<a href="https://peak.nexon.com/ja/post/2760" target="_blank" rel="noopener noreferrer">Nexon Peak・同行ペットガイド</a>。本サイトでの職別割り当ては主力スキルとの相性による編集判断です。ペット採用率は取得していません。</p>'
    '<p>日本語ルーン名・効果：<a href="'+WEBSITE+'" target="_blank" rel="noopener noreferrer">マビノギモバイル Wiki DB</a>（アリス氏／CC BY 4.0）。名称の一致しない台湾語表記は照合中として区別しました。スキル調整・実装時期に地域差があります。</p>'
    '<div class="job-bottom-links"><a href="../runes/index.html">全ルーン図鑑を見る</a><a href="../tools/damagecalc.html">ダメージ計算を使う</a></div></section>')
    pagernav=(f'<nav class="job-pager" aria-label="前後の職業"><a href="{pre["slug"]}.html"><span>← 前の職業</span><strong>{esc(pre["name"])}</strong></a><a href="{nxt["slug"]}.html"><span>次の職業 →</span><strong>{esc(nxt["name"])}</strong></a></nav>')
    quicknav=('<nav class="job-jump" aria-label="職業ページ内ナビゲーション"><a href="#build-guide">おすすめ構成</a><a href="#skill-guide">スキル特化</a><a href="#gem-guide">宝石タグ</a><a href="#skill-dictionary">スキル・改造</a><a href="#pet-guide">ペット</a><a href="#rune-stats">ルーン採用率</a></nav>')
    statstart='<div class="job-stats-heading" id="rune-stats"><div class="portal-kicker">04 · RUNE ADOPTION · TAIWAN</div><h2>台湾版のルーン採用率</h2><p>ここからは使用者の割合を示した統計です。上のスキル・宝石・ペットの推薦根拠とは異なります。</p></div>'
    body=overview+quicknav+rec+combat_detail(job)+guide_detail(job)+skill_detail(job)+explanations+statstart+block+tail+links+pagernav+'<footer class="portal-foot">非公式の攻略ノート。日本版ゲーム内の最新表記を優先してください。</footer>'
    (ROOT/'jobs'/f'{job["slug"]}.html').write_text(page_doc(f'{job["name"]}のスキル特化・宝石・ペット・ルーン採用率｜エリン調査ノート',body,desc=f'{job["name"]}のスキル特化・宝石タグ・同行ペット・ルーン構成。台湾の武器防具アクセ採用率。'),encoding='utf-8')

families=['戦士系','弓系','魔法系','回復系','音楽系','盗賊系']
index_intro=('<section class="job-hero job-list-hero"><div class="job-breadcrumb"><a href="../index.html">ホーム</a> / 職業別おすすめ</div>'
'<div class="portal-kicker">CLASS BUILD LIBRARY · SEASON 0</div><h1 class="portal-page-title">全18職の攻略ガイド</h1>'
'<p class="portal-lead">スキルと改造ルーンの対応、基本効果・確認済みスキルタグ、特化・宝石・ペットから台湾ルーン採用率まで職業別に掲載。日本語のルーン図鑑とも連携します。</p>'
'<div class="job-hero-chips"><span class="portal-pill">18クラス</span><span class="portal-pill">スキル特化・宝石タグ・ペット</span><span class="portal-pill">スマホ対応</span></div></section>'
'<div class="job-warning"><strong>採用率の注意：</strong>台湾の公開データです。日本版の全プレイヤー統計ではありません。採用上位＝理論上の最強ではなく、使用率は所持状況やコンテンツで変動します。<a href="'+SOURCE+'">出典：愛爾琳網</a></div>'
'<section class="portal-panel job-index-tools"><label for="jobSearch">職業を検索</label><input id="jobSearch" type="search" placeholder="氷結術師、元素、シーズー…" autocomplete="off"><div class="job-family-chips" role="group" aria-label="職業の系統">'
'<button class="job-filter active" type="button" data-family="all" aria-pressed="true">すべて</button>'+
''.join(f'<button class="job-filter" type="button" data-family="{esc(f)}" aria-pressed="false">{esc(f)}</button>' for f in families)+'</div><p id="jobFound" class="job-found" aria-live="polite">18職を表示</p></section>')

cards=['<div class="job-directory">']
for job in jobs:
    info=guides[job['slug']]
    trio=' / '.join(x['name'] for x in job['accessory'][:3])
    spec=info['specialization']['primary']
    gems=' → '.join(x['tag'] for x in info['gems']['priorities'])
    # Accessible search also matches role, recommended rune, and pet names.
    keywords=' '.join([job['name'],job['family'],job['role'],trio,gems]+[x['name'] for x in info['pets']['candidates']])
    cards.append(f'<a class="job-directory-card" href="{job["slug"]}.html" data-name="{esc(keywords)}" data-family="{esc(job["family"])}"><div class="job-directory-top"><span class="job-directory-icon">{job["icon"]}</span><span class="portal-pill">{esc(job["family"])}</span></div><h2>{esc(job["name"])}</h2><p>{esc(job["role"])}</p><div class="job-directory-facts"><span>スキル特化 <b>{esc(spec)}</b></span><span>宝石 <b>{esc(gems)}</b></span></div><div class="job-mini-title">採用上位のアクセサリー</div><strong>{esc(trio)}</strong><div class="job-open">職業ガイドを見る →</div></a>')
cards.append('</div>')
index_body=index_intro+''.join(cards)+'<p class="job-index-source">数値出典：<a href="'+SOURCE+'">愛爾琳網・台湾ルーン採用ランキング</a>（2026-11-01参照）。日本語訳語は独立編集。</p><footer class="portal-foot">非公式の攻略ノート。日本版ゲーム内の最新表記を優先してください。</footer>'
index_html=page_doc('18職のスキル特化・宝石・ペット・ルーン攻略｜エリン調査ノート',index_body,desc='全18職の攻略ガイド。日本版Season0向けスキル特化・宝石タグ・同行ペット・台湾版のルーン採用率。')
index_html=index_html.replace('</body></html>','<script defer src="../assets/jobs.js"></script></body></html>')
(ROOT/'jobs/index.html').write_text(index_html,encoding='utf-8')

print(f'Rebuilt {len(jobs)} job pages and jobs/index.html')
