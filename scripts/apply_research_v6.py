#!/usr/bin/env python3
"""Apply manual, attributed 2026-11-02 research after build_skill_data.py.
This is intentionally an overlay: the rune database remains the source of rune text,
while independently checked active skill names, basic effects and limited tags are attached.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'data/job-skills.json'
obj=json.loads(p.read_text(encoding='utf8'))
D=obj['jobs']
GW='https://gamewith.jp/mabinogimobile/'
ULT={
'warrior':('ブレイドインパクト','敵の密集地点へ跳躍して衝撃波で攻撃し、短時間のHP上昇と被ダメージ軽減を得る。','https://www.pc-support-help.com/2026/10/17/mabinogi-mobile-warrior-skills/'),
'greatsword':('必死の一撃','地面を崩す大範囲攻撃を行い、戦闘テンポを最大まで高めて攻撃力強化を得る。',GW+'577047'),
'swordmaster':('一閃','集中状態に入り、直線上の敵を高速で斬り抜ける。終了後は疾風態勢につながる。',GW+'577046'),
'archer':('灼熱の軌跡','火の矢を放って全スキルの待機時間をリセットし、一定時間の攻撃を火矢へ強化する。',GW+'577048'),
'crossbow':('ヘルファイア','多数のボルトを撃ったのち爆発ボルトで広域攻撃し、強化ボルト弾倉を装填する。',GW+'577050'),
'longbow':('デススティンガー','強烈な矢と大量の矢を同時発射して広域制圧し、敵を押し戻して衰弱を付ける。',GW+'577049'),
'mage':('マナインフィニティ','スキルの待機時間をリセットし、一定時間キャスト速度とマナ回復を引き上げる。',GW+'577189'),
'firemage':('インフェルノ','前方へ炎の光線を放出する究極技。終了時に爆発と継続火炎領域を作り、バーニングソウルを高段階にする。',GW+'577052'),
'priest':('救いの光','味方への継続回復と周囲への光波を付与。光波は敵にダメージを与え、味方に回復・蘇生の強化を与える。',GW+'577129'),
'monk':('信念の要塞','聖域を作り、範囲内の味方へ被ダメージ軽減とブレイク・ノックバック耐性を付与する。',GW+'577130'),
'bard':('バトルシンフォニー','演奏で味方の与ダメージを高め、ブレイクを防ぎながらスキルの待機時間を短縮する。',GW+'577501'),
'dancer':('フィナーレ','テンポと公演の熱気を最大化し、消費した熱気の回数に応じて強力な終撃を放つ。',GW+'577483'),
'musician':('カデンツァ','即興演奏で周囲へ攻撃し、同じスロットの演奏や最終ダメージを強化する。',GW+'577503'),
'rogue':('ブリッツラッシュ','高速で敵を斬って周囲にも範囲攻撃し、スローイングボム・奇襲のクールタイムをリセットする。',GW+'577168'),
'fighter':('オーバードライブ','一定時間スキルのクールタイムを大幅に短縮し、チェーンとコンボを集中して発動できる。',GW+'577484'),
'dualblade':('ファイナルヒット','高速の連続斬撃で一体へ集中攻撃し、対象が倒れると近くの敵へ攻撃を継続する。',GW+'577191')}
for slug,(name,description,source) in ULT.items():
 objj=D[slug]; existing=next((s for s in objj['skills'] if s['name']==name),None)
 if existing is None:
  existing={'name':name,'slot':6,'tags':[],'description':description,'runes':[]}
  objj['skills'].append(existing)
 else:
  existing['slot']=existing.get('slot') or 6
  existing['description']=existing.get('description') or description
 existing['kind']='究極技';existing['description_source']=source
# Normalize a class-name translation while preserving its original rune attachment.
for skill in D['crossbow']['skills']:
 if skill['name']=='スプレッディングボルト':
  skill['name']='スプレッドボルト'
  skill['translation_note']='旧図鑑内の「スプレッディングボルト」と同一の技と推定。日本語スキル名はGameWithに準拠。'
  skill['description']='扇形に強化ボルトを発射し、前方の複数の敵へ範囲ダメージを与える。'
for skill in D['priest']['skills']:
 if skill['name']=='ディバインウィング':
  skill['name']='ディヴァインウィング'
  skill['description']='対象へ鳥形の光を放つ支援攻撃。リンカーで接続した相手へ届き、敵と味方に異なる効果を与える。'
# Add source-backed skill mechanics to current rune-derived descriptions (independently summarized).
DESCRIPTIONS={
 'warrior':{
  'ラピッドスラッシュ':'敵へ一気に接近し連続斬撃。闘志最大時に攻撃回数とスキル使用速度が伸びる。',
  'ブレイドスマッシュ':'前方の敵を剣で薙ぎ払い転倒させる。闘志最大時は全周囲へ高速で攻撃する。',
  '突き':'敵へ突進する剣技。ルーン「突撃」を付けると高威力の「貫き」に切り替わる。',
  '戦場の雄叫び':'周囲の敵を挑発し、攻防の支援と闘志獲得に使用する。',
 },
 'greatsword':{
  'スピニングスラッシュ':'周辺の敵を素早く斬る。剣の構えが後ろなら動作が速くなり戦闘テンポも得る。',
  'ライジングスマッシュ':'斬り上げて範囲の敵を浮かせる。前構えでは素早く使えて戦闘テンポを得る。',
  '大剣術':'溜めた戦闘テンポを消費して強力な一撃を放つ主力技。',
  'ショルダーアタック':'勢いよく敵へ接近して押し戻す。構えでストンプと切り替わる。',
 },
 'swordmaster':{'鋼のくさび':'敵へ突き込み、確率で秘剣へ直ちにつなぐ。集中状態では発動率が高まる。',
  '鞘アタック':'鞘で強打した後に剣で斬りつける。',
  'ソードダンス':'前方を連続斬撃。集中状態ではクールタイムが大きく減る。',
  '秘剣':'直前に使った剣技を強化して再使用する。使用順が火力を左右する。',
  '看破':'敵の攻撃へ備え、条件成立時に敵の背後へ回ってカウンターする。発動中は被ダメージを軽減する。'},
 'archer':{'アローリボルバー':'矢を連射する。通常攻撃・スキル命中で待機時間が短縮し、疾風中は近くの敵にも命中。',
  'マグナムショット':'強い一矢で前方を薙ぎ払う。疾風中は詠唱が短くなる。',
  'サイドステップ':'敵の攻撃をかわしながら矢を放つ回避射撃。'},
 'crossbow':{'ガスティングボルト':'強化ボルトを連射して大ダメージを与える。連射するほど命中時クリ率に減衰がある。',
  'バスターショット':'衝撃波のあるボルトで前方範囲攻撃し、強化ボルトを装填する。',
  'ショックエクスプロージョン':'ボルトの爆発で敵をスタンさせ、強化ボルト弾倉を補給する。',
  'スライディングステップ':'後方へ滑りながら複数の矢を撃ち、弾倉を装填。被ダメージ軽減も得る。'},
 'longbow':{'シェルブレイカー':'速射の最後の矢で被ダメージ増加の弱体化を敵へ与える。',
  'ハートシーカー':'チャージする狙撃技。主力の強打としての運用を想定。'},
 'firemage':{'ラピッドファイア':'小さな炎球を連射して灼熱を付与。別スキルの爆発を条件に一度だけ高速で再発動できる。',
  'ファイアストーム':'敵を引き寄せる炎の渦で攻撃して灼熱を付与。消滅時に爆発して炎を残す。',
  'エクスプロージョン':'熱気を全て消費し、灼熱がある敵や残った炎を一気に爆発させる。',
  'フラッシュオーバー':'熱気を消費しながら連続して火炎の波動を放つ。',
 },
 'healer':{'ライフリンク':'短押しで敵へ継続ダメージ、長押しで味方へ継続回復と与ダメージ強化。連結先で機能が変わる。'},
 'priest':{'サモンリンカー':'短押しは敵への持続攻撃・被ダメージ増、長押しは味方への継続回復・与ダメージ増。',
  'ディヴァインウィング':'光を放つ支援技。リンカーで接続した対象にも働きかける。',
  'ケルティッククロス':'移動する光のシンボルで攻撃し、神聖力の循環を助ける。',
  'サンクチュアリ':'回復と神聖力管理に関わる聖域を設置する。',
  'ホーリースピア':'神聖力を消費して巨大な光の槍を落とし、敵への継続攻撃と味方への回復エリアを作る。'},
 'monk':{'殺到':'光の拳で直線を連打し、光の真言を得る。真言中は攻撃時に周囲の味方も回復。',
  '霹靂打':'敵を強打して力の真言を得る。真言中は追加攻撃が発生する。',
  '守護陣':'神聖力を消費して敵を攻撃し、味方へバリアを展開する。',
  '治癒':'神聖力を消費して低HPの味方を回復。対象周囲の敵にも攻撃する。',
  '化身':'真言を一斉に発動し、通常攻撃とスキルを強化する。'},
 'bard':{'ストリングショット':'連鎖攻撃と弱点露呈デバフ。演奏スキル後に使うと発動が速い。',
  'メロディーショック':'演奏と連携する近距離攻撃。目眩中の敵へ追加ダメージ。',
  'トリプルストローク':'演奏で敵に目眩を付け、すでに目眩の敵には恐怖の継続攻撃を追加。',
  'バーズテイル':'楽想により曲が変化し、味方の回復・攻撃速度の支援と敵への範囲攻撃を行う。'},
 'dancer':{'ナチュラルターン':'敵が遠ければ突進し、近ければ背後へ回って攻撃。優雅状態でリズム生成が増える。',
  'ウィンドミル':'周囲を回転攻撃。動作中はブレイクされず、情熱状態ならリズムを追加生成。',
  'アドリブ':'即興ステップで攻撃しリズムを追加で得る。'},
 'musician':{'演奏:アルペジオ':'星明かりの弾で幻惑を付与し、防御低下と持続ダメージを与える。',
  '演奏:セレナーデ':'演奏中に敵へ持続攻撃し、中断時に強打とスタンを与える。',
  '技巧:クライマックス':'蓄積した弱体化が多いほどダメージの大きいフィニッシュ技。'},
 'rogue':{'スローイングボム':'爆弾で周囲を攻撃し、当たった敵の被ダメージを上げる。オーバーチャージで強化。',
  'スクリューダガー':'周囲を連打し、オーバーチャージで追撃を増やす。毒の爆破と連動する。',
  '奇襲':'敵の背後へ回り込み刺す。オーバーチャージ時に傷を付与する。',
  'ポイズントラップ':'毒の領域を設置して中毒と鈍足を付与する。',
  '隠密':'敵の注意を外して潜み、直後の直接攻撃を強めてスタンさせる。'},
 'fighter':{'チャージングフィスト':'チャージ段階で威力が増す接近攻撃。チェーン連携の起点。',
  'スラストキック':'蹴りによる第1段階チェーン技。次のアッパーやストンプへつなげる。',
  'バックステップ':'敵から離れて被弾を避け、次のチェーン技の威力を高める。',
  'バーストパンチ':'敵を打ち抜く強打・コンボ攻撃。高威力の連携で使う。',
  'サマーソルト':'3段まで連携する蹴り。移動しながら単体に連撃を重ねる。'},
 'dualblade':{'スプリットスラッシュ':'敵へ素早く接近して二刀で刺し、敵の近接防御を一時的に無視する。',
  'スプリットダウン':'スプリットスラッシュの強化系。防御無視効果をさらに重ねる。'},
}
for slug,updates in DESCRIPTIONS.items():
 for skill in D[slug]['skills']:
  if skill['name'] in updates:
   skill['description']=updates[skill['name']]
   skill['description_source']=D[slug]['source_gamewith']
# Actual slots and per-skill tags: cross-checked where public guides enumerate by number;
# source_class kept explicit, many other skills intentionally have null slots/empty tags.
VERIFIED={
 'priest':{'サモンリンカー':(1,['連打','補助']),'ディヴァインウィング':(2,['補助','妨害']),
 'ケルティッククロス':(3,['連打','補助','妨害']),'サンクチュアリ':(4,['補助','召喚']),
 'ホーリースピア':(5,['強打','補助']),'救いの光':(6,['連打','補助','生存'])},
 'fighter':{'チャージングフィスト':(1,['強打','移動','妨害']),'スラストキック':(2,['強打','妨害']),
 'バックステップ':(3,['移動','生存','補助']),'バーストパンチ':(4,['強打','補助']),
 'サマーソルト':(5,['強打','移動']),'オーバードライブ':(6,['生存','補助'])},
 'warrior':{'ブレイドインパクト':(6,[])},
}
SOURCES={'priest':'https://www.mabiwiki.com/classes/priest','fighter':'https://www.mabiwiki.com/classes/fighter',
'warrior':'https://www.pc-support-help.com/2026/10/17/mabinogi-mobile-warrior-skills/'}
for slug,rows in VERIFIED.items():
 for skill in D[slug]['skills']:
  if skill['name'] in rows:
   skill['slot'],skill['tags']=rows[skill['name']]
   skill['slot_source']=SOURCES[slug]
   if skill['tags']:skill['tag_source']=SOURCES[slug]
# In the earlier guide, some frost mage tags were disputed by other JP community sources.
# Retain old tags as corroborated where possible, and add disputed ones separately.
for skill in D['frostmage']['skills']:
 if skill['name']=='アイススパイク':
  skill['disputed_tags']=['生存','補助']
  skill['tag_dispute']='「生存」「補助」を挙げる別の日本語先行資料あり。基本タグ/ルーン装着後タグのいずれかは日本実機で要確認。'
  skill['tag_source']='https://gamerch.com/mabinogimobile/1019868'
 if skill['name']=='グレイシアカッター':
  skill['disputed_tags']=['妨害']
  skill['tag_dispute']='グレイシアカッターは妨害タグも報告あり。北風による元素タグへの変更は未確定。'
  skill['tag_source']='https://mabinogimobile.nipponhashi.com/ja/guides/frostmage-gem-tags/'
# Additional slots available in pre-JP/other-season community tables. These are NOT
# claimed as JP S0 screenshots; tags are omitted where the table uses role labels.
ADDITIONAL_SLOTS={
 'swordmaster':{
  '鋼のくさび':(1,['強打','補助']),'鞘アタック':(2,['強打','妨害']),
  'ソードダンス':(3,['強打','連打']),'秘剣':(4,[]),
  '看破':(5,['強打','移動','生存']),'一閃':(6,['強打','移動','補助'])},
 'greatsword':{
  'ライジングスマッシュ':(2,[]),'ショルダーアタック':(3,[]),
  'スラッシュ':(4,[]),'大剣術':(5,[])},
 'bard':{
  'ストリングショット':(1,['補助','妨害']),
  'メロディーショック':(2,['強打','妨害','移動']),
  'トリプルストローク':(3,[]),'バーズテイル':(4,[]),
  'バトルシンフォニー':(6,['連打','生存','補助'])},
}
ADDITIONAL_SOURCE={
 'swordmaster':'https://mabi.games-wiki.com/classes/swordmaster',
 'greatsword':'https://mabi.games-wiki.com/classes/greatsword-warrior',
 'bard':'https://mabi.games-wiki.com/classes/bard',
}
for slug,updates in ADDITIONAL_SLOTS.items():
 D[slug]['slot_table_source']=ADDITIONAL_SOURCE[slug]
 for skill in D[slug]['skills']:
  if skill['name'] in updates:
   number,tags=updates[skill['name']]
   skill['slot']=number
   if tags:skill['tags']=tags
   skill['slot_source']=ADDITIONAL_SOURCE[slug]
   if tags:skill['tag_source']=ADDITIONAL_SOURCE[slug]

# Class name and S0 source distinctions.
for slug,job in D.items():
 for skill in job['skills']:
  skill.setdefault('kind','基本スキル')
  if skill.get('slot')==6: skill['kind']='究極技'
  if slug=='fighter' and skill['name'] in ('ストンプキック',):
   skill['kind']='チェーン派生技'
  if slug=='greatsword' and skill['name']=='ストンプ':
   skill['kind']='構えで切替'
  if slug=='dualblade' and skill['name'] in ('スプリットダウン','ライトニングフューリー','ハウリングテンペスト','ライジングクレセント'):
   skill['kind']='強化・派生技'
  if slug=='warrior' and skill['name']=='シールドバッシュ（旧・別表記の可能性）':
   skill['translation_note']='シールドバッシュ／シールドラッシュの表記に差があります。ルーン「突進」の効果文とゲーム内を照合してください。'
 job['skills'].sort(key=lambda s:(s['slot'] if s['slot'] is not None else 99,s['name']))
# Published aliases reflect JP player-facing names instead of only the rune database.
obj['updated']='2026-11-02'
obj['method']='GameWith JP skill mechanics paraphrased + Japanese community skill slot/tag tables for confirmed classes + pre-existing CC BY4.0 rune catalog. S0/S1 mixed source caution.'
obj['research_sources']=[
 {'label':'GameWith 18職スキル一覧','url':'https://gamewith.jp/mabinogimobile/577051','note':'各職source_gamewithを参照。基本効果は独自要約'},
 {'label':'剣術士：番号とタグ（先行）','url':'https://mabi.games-wiki.com/classes/swordmaster','note':'日本訳差・Season差に注意'},
 {'label':'大剣戦士：一部番号（先行）','url':'https://mabi.games-wiki.com/classes/greatsword-warrior','note':'一部番号のみ'},
 {'label':'吟遊詩人：番号とタグ（先行）','url':'https://mabi.games-wiki.com/classes/bard','note':'日本訳差・Season差に注意'},
 {'label':'司祭：番号とタグ','url':'https://www.mabiwiki.com/classes/priest','note':'韓国先行のタグを含む。日本S0は要確認'},
 {'label':'格闘家：番号とタグ','url':'https://www.mabiwiki.com/classes/fighter','note':'日本未実装ルーンの記載は利用せず、スキル名/タグのみ参考'},
 {'label':'氷魔タグ比較','url':'https://gamerch.com/mabinogimobile/1019868','note':'氷魔のタグに表記差あり'},
 {'label':'ルーンDB','url':'https://mabinogimobile.nipponhashi.com/ja/runes/','note':'CC BY 4.0 由来の効果文・日本語名スナップショット'}]
p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('research applied:',[(j['class'],len(j['skills'])) for j in D.values()])
