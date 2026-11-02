#!/usr/bin/env python3
"""Offline, conservatively join existing rune dataset to skill targets.
All generic skill targets come from the S0 JP accessory rune effect's FIRST sentence.
Confirmed slot mappings are editorial overrides with source URLs.
"""
import json,re
from pathlib import Path
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parents[1]
runes=json.loads(BeautifulSoup((root/'runes/index.html').read_text(encoding='utf8'),'html.parser').select_one('#runeDataset').string)
jobs=json.loads((root/'data/job-builds.json').read_text(encoding='utf8'))['jobs']
# Slot numbering: only values separately corroborated in the JP-language guide.
SLOTS={
'frostmage': {'クリスタルエッジ':1,'グレイシアカッター':2,'アイススパイク':3,'フリージングフィールド':4,'フローズンオーブ':5,'アブソリュートゼロ':6},
'healer': {'ライフリンク':1,'ファントムペイン':2,'生命の鼓動':3,'プロテクション':4,'サモンルミナス':5,'ウィングオブエンジェル':6},
'mage': {'ライトニング':1,'ファイアボール':2,'アイスダガー':3,'テレキネシス':4,'マナストーム':5},
}
# Brief skill mechanics, either independently supported by JP guides or identified by the accessory effects.
DESCRIPTION={
 'frostmage': {
 'クリスタルエッジ':'冷気の剣で前方を連続攻撃し、霜を生成する。短時間に最大3回まで使用できる。',
 'グレイシアカッター':'冷気の双剣で攻撃し、挑発と凍結を付与する。',
 'アイススパイク':'防御・反撃に使う氷の技。HP条件に応じた自動発動などの改造がある。',
 'フリージングフィールド':'敵を継続的に攻撃する氷の設置範囲技。',
 'フローズンオーブ':'氷球で範囲攻撃し、ルーン次第で味方を守る氷のベールを生成する。',
 'アブソリュートゼロ':'氷結術師の究極技。広域攻撃と霜・防御の管理に関わる。'},
 'healer': {
 'ライフリンク':'味方をつないで支援・回復し、敵への連結時は攻撃に使う。',
 'ファントムペイン':'敵と味方の間を行き来する攻撃・支援技。',
 '生命の鼓動':'回復と敵へのダメージを両立する主力技。',
 'プロテクション':'味方を守り、受けるダメージを下げる防御技。',
 'サモンルミナス':'光の存在を召喚し、回復と戦闘のサポートを行う。',
 'ウィングオブエンジェル':'ヒーラーの究極技。防御・回復支援に用いる。'},
 'mage': {'ライトニング':'雷撃による攻撃。ルーン「落雷」で追加落雷と感電へ拡張。',
 'ファイアボール':'火属性攻撃。ルーン「隕石」でメテオストライクへ切り替える。',
 'アイスダガー':'氷片で攻撃。ルーン「霜の棘」で氷片の射出数と攻撃方式を変える。',
 'テレキネシス':'岩片などを操って攻撃。ルーン「山崩れ」で元素ダメージ強化を得る。',
 'マナストーム':'魔力と位置取りを扱う技。「点滅」は移動・シールド、「増幅」は元素DoT強化に変える。'},
 'warrior': {'ラピッドスラッシュ':'敵へ接近して連続で斬る。闘志が最大のとき攻撃回数と速度が増える。',
 'ブレイドスマッシュ':'前方を強く斬る範囲攻撃。闘志が最大なら高速化・全周囲攻撃が可能。'},
 'greatsword': {'スピニングスラッシュ':'周囲を一閃する範囲斬撃。構えによって動作が変化する。',
 'ライジングスマッシュ':'敵を斬り上げる攻撃。ルーンでチャージと反撃動作を追加できる。'},
 'swordmaster': {'鋼のくさび':'敵に素早く突き込み、秘剣の使用につなげる。',
 '鞘アタック':'剣と鞘で薙ぎ払う攻撃。', 'ソードダンス':'斬撃を連続で繰り出し、集中状態でCTが下がる。'},
 'crossbow': {'ガスティングボルト':'強化ボルトを消費して連射する、クールタイムのない主力攻撃。',
 'バスターショット':'ショックボルトで範囲攻撃し、強化ボルトを装填する。',
 'ショックエクスプロージョン':'電気のボルトを爆発させて範囲攻撃・スタンと装填を行う。'},
 'firemage': {'ラピッドファイア':'火炎球を連射して灼熱を付与し、条件付きで再使用が速くなる。',
 'ファイアストーム':'炎の渦で敵を集め、ダメージと灼熱を与える究極技。'},
 'dancer': {'ナチュラルターン':'敵へ接近・背後へ回り込みつつ範囲攻撃する。',
 'ウィンドミル':'回転して周囲を攻撃。使用中はブレイクされない。'},
 'rogue': {'スローイングボム':'爆弾を投げて範囲ダメージ。オーバーチャージで強化。',
 'スクリューダガー':'周辺を連打しながら浮かせる攻撃。',
 '奇襲':'敵の背後を取り範囲攻撃。条件に応じて一部スキルのCTをリセット。'},
 'longbow': {'シェルブレイカー':'連射で防御を崩し、最後の矢で被ダメージ上昇効果を付ける。',
 'デススティンガー':'大量の矢で周囲を制圧し、ノックバックや衰弱を付与する。'},
}
ALIASES={ 'greatsword': {'回転斬り':'スピニングスラッシュ'},'warrior':{'シールドバッシュ':'シールドバッシュ（旧・別表記の可能性）'},
  'swordmaster':{'ブレードスマッシュ':'ブレイドスマッシュ'} }
# Verified per-skill tags. Do not infer other per-skill tags from recommended class tag order.
TAGS={'frostmage': {'クリスタルエッジ':['元素'],'グレイシアカッター':['強打'],
 'アイススパイク':['元素'],'フリージングフィールド':['元素','召喚','生存'],
 'フローズンオーブ':['元素','召喚'],'アブソリュートゼロ':['元素','召喚','生存']},
 'priest': {'サモンリンカー':['補助'],'サンクチュアリ':['補助'],'ケルティッククロス':['補助'],'ディバインウィング':['補助'],'ホーリースピア':['補助']}, 'healer': {}}
# Sources for slot/tag details. Rune descriptions are existing snapshot (CC BY 4.0).
GW={
 'warrior':'577045','greatsword':'577047','swordmaster':'577046','archer':'577048','crossbow':'577050','longbow':'577049',
 'mage':'577189','firemage':'577052','frostmage':'577051','healer':'577128','priest':'577129','monk':'577130',
 'bard':'577501','dancer':'577483','musician':'577503','rogue':'577168','fighter':'577484','dualblade':'577191'}
# Link rune to its target skill(s) from first sentence. For multi-target rune, split on Japanese enumeration.
def targets(rec,cls):
 text=rec['effect'].split('。',1)[0]
 lead=re.search(re.escape(cls)+r'の(.+?)(?:スキル)?(?:を|に)(?=変化|.{0,36}?(?:切り替え|置き換え|変化))',text)
 if not lead:return []
 fragment=lead.group(1).replace('スキル演奏:', '演奏:')
 fragment=fragment.replace('スキル','') if fragment.endswith('スキル') else fragment
 bits=re.split(r'[、，]|と(?=[^にを]{1,20}$)',fragment)
 return [v.strip() for v in bits if 1<=len(v.strip())<=32]
NOTES=json.loads((root/'data/skill-notes.json').read_text(encoding='utf8'))
out={'updated':'2026-11-01','method':'JP Season0 accessories linked by named skill in effect, some slot/tag values verified separately','jobs':{}}
for job in jobs:
 cls=job['name']; slug=job['slug'];
 acc=[r for r in runes if r['slot']=='アクセサリー' and cls in r['classes']]
 bucket={}
 for rec in acc:
  # Only bind exact '日本版実装' here; leave unimplemented S1/S2 runes visibly separate at bottom.
  if rec['status']!='日本版実装':continue
  for name in targets(rec,cls):
   name=ALIASES.get(slug,{}).get(name,name)
   item=bucket.setdefault(name,{'name':name,'slot':SLOTS.get(slug,{}).get(name),
                   'tags':TAGS.get(slug,{}).get(name,[]),
                   'description':DESCRIPTION.get(slug,{}).get(name) or NOTES.get(slug,{}).get(name,''),
                   'runes':[]})
   item['runes'].append({'name':rec['name'],'grade':rec['grade'],'status':rec['status'],'effect':rec['effect']})
 # Guarantee all six known slots for classes with reliable positions, even with no associated accessory rune.
 for name,idx in SLOTS.get(slug,{}).items():
  bucket.setdefault(name,{'name':name,'slot':idx,'tags':TAGS.get(slug,{}).get(name,[]),
            'description':DESCRIPTION.get(slug,{}).get(name) or NOTES.get(slug,{}).get(name,''),'runes':[]})
 for rec in bucket.values():
  # Stable order: skill slot first when verified, then Japanese skill name.
  rec['runes'].sort(key=lambda r:(r['grade']!='エピック',r['name']))
 out['jobs'][slug]={'class':cls,'source_gamewith':'https://gamewith.jp/mabinogimobile/'+GW[slug],
    'source_runes':'https://mabinogimobile.nipponhashi.com/ja/runes/',
    'skills':sorted(bucket.values(),key=lambda x:(x['slot'] or 99,x['name'])),
    'unreleased_count':len([a for a in acc if a['status']!='日本版実装'])}
(root/'data/job-skills.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('skill counts:',[(k,len(v['skills']),sum(len(s['runes']) for s in v['skills'])) for k,v in out['jobs'].items()])
