#!/usr/bin/env python3
"""韓国 S0後半～S1初期のクラス調整：日本語の調査ノートから静的HTMLを再生成する。"""
from pathlib import Path
import json, html
P=Path(__file__).resolve().parents[1]
J=json.loads((P/'data/job-builds.json').read_text(encoding='utf-8'))['jobs']
CL={x['slug']:x for x in J}
CL['lightning']={'slug':'lightning','name':'電撃術師','family':'魔法系','icon':'⚡','role':'2025年6月19日に韓国S0へ追加'}
S={
 '2025-04-24':('韓国公式 4/24','https://mabinogimobile.nexon.com/News/Update/2839181'),
 '2025-05-08':('韓国公式 5/8','https://mabinogimobile.nexon.com/News/Update/2871156'),
 '2025-05-29':('韓国公式 5/29','https://mabinogimobile.nexon.com/News/Update/2919137'),
 '2025-06-19':('韓国公式 6/19','https://mabinogimobile.nexon.com/News/Update/2958152'),
 '2025-07-17':('韓国公式 7/17','https://mabinogimobile.nexon.com/News/Update/3038276'),
 '2025-07-31':('韓国公式 7/31','https://mabinogimobile.nexon.com/News/Update/3064411'),
 '2025-08-21':('韓国公式 8/21','https://mabinogimobile.nexon.com/News/Update/3100670'),
 '2025-09-04':('韓国公式 9/4','https://mabinogimobile.nexon.com/News/Update/3123745'),
 '2025-09-25':('韓国公式 9/25','https://mabinogimobile.nexon.com/News/Update/3147463'),
 '2025-10-23':('韓国公式 10/23点検','https://mabinogimobile.nexon.com/News/Notice/3190410'),
 '2025-10-30':('韓国公式 10/30','https://mabinogimobile.nexon.com/News/Update/3201526'),
}
R=[]
def add(c,d,t,title,note,why=''):
 assert c in CL and d in S and t in ('強化','弱体化','仕様変更','不具合修正','新職追加','調整'),(c,d,t)
 R.append({'class':c,'date':d,'phase':'S0' if d<'2025-09-25' else 'S1','type':t,'title':title,'detail':note,'impact':why,'source':S[d][1]})
# --- 韓国 S0 の序盤・中盤 ---
add('rogue','2025-04-24','新職追加','盗賊系3職が登場','盗賊・格闘家・デュアルブレイドが同日に実装。韓国サービス開始日の評価には、この3職自体が含まれていません。','初期の職業ランキングと比較するときの前提が変わります。')
add('fighter','2025-04-24','新職追加','格闘家が登場','盗賊系追加により、新たなコンボ型近接職が選択可能に。')
add('dualblade','2025-04-24','新職追加','デュアルブレイドが登場','盗賊系の追加職として実装。')
add('healer','2025-05-08','強化','回復だけでない戦闘・支援性能へ','ウィングオブエンジェルの対敵ダメージが大幅上昇。バイタルブーストの追加回復対象に移動速度上昇を付与。蘇生習得後は味方回復・追加攻撃命中で自身の与ダメージが徐々に伸びる効果も追加。','旧「純ヒーラー」評価をそのまま当てはめられない転換点です。')
add('healer','2025-05-08','強化','波・心拍系の回復改善','生명의鼓動に「波」「心拍」ルーンを適用したときの回復量を増加。リンク中は低HPの味方を優先して対象選択し、リンクの接続距離も延長。')
add('priest','2025-05-08','強化','聖なる力の回収と槍の回転率を改善','「燃える光」習得後、強打が命中すると神聖力を回復し、ホーリースピアの残りCTを短縮。救済の光の敵へのダメージも大幅上昇し、リンク距離を延長。','神聖力をただ溜めるだけでなく、強打命中を絡めた回転が改善。')
add('monk','2025-05-08','強化','信念の要塞の対敵火力','信念の要塞の敵へのダメージが大幅に増加。業火へ生存タグが追加。')
add('warrior','2025-05-08','仕様変更','闘志とブレイドスマッシュの手触り','闘志へ強化されたブレイドスマッシュは敵をその場でダウンさせるよう変更。強打や追加攻撃の命中でも闘志を生成するよう変更。')
add('crossbow','2025-05-29','弱体化','当時突出していたガスティングボルトを調整','強化ボルトを多く撃つほど、その弾のクリティカル率が下がる仕様に変更。スライディングステップのCTを延長（旧新の秒数は告知未記載）。','初期韓国で強かった職が後に調整された代表例。ルーン「連鎖」の連鎖雷クリティカルはこの減衰の対象外。')
add('crossbow','2025-05-29','不具合修正','連鎖ルーンとバスターショット','連鎖付きガスティングボルトの3連射目にスキルLv効果が乗らない不具合を修正。バスターショット使用時の後退を廃止。')
add('rogue','2025-05-29','強化','毒の継続ダメージを強化','ポイズンアタックのパッシブによる毒ダメージを増加（具体的な倍率は公式告知に記載なし）。')
add('dualblade','2025-05-29','仕様変更','活気パッシブが主力技と究極技へ乗る','従来の「連打→次の強打増加」から「連打→次の強化スキルおよび究極技増加」へ変更。スプリットスラッシュ／スプリットダウンは突進機能追加・射程延長。','複数のスキルに恩恵が広がり、接敵性能も向上。')
add('dualblade','2025-05-29','不具合修正','強化・移動スキルとオート動作','一部の強化スキルに強化ルーンが効かない問題と体型依存の入力遅延を修正。アシストモードの使用順も変更。')
add('mage','2025-05-29','不具合修正','エレメンタルマスターと隕石','エレメンタルマスターのダメージ増幅が正しく乗らない問題を修正。隕石ルーンでのメテオストライクに究極ゲージ獲得とメディテーションが働かない不具合も修正。')
add('frostmage','2025-05-29','強化','氷結（凍結）効果を新規導入','アイシクルマークの単体にしか印を付けられない制約を撤廃。氷属性の直接攻撃で凍結スタックを付け、一定回数で大ダメージ。低HPの敵には防御無視の即時ダメージも発動。','韓国サービス初期の氷魔と、5月末以降の氷魔は基本ギミック自体が別物。')
add('frostmage','2025-05-29','強化','クリスタルエッジ高速化と凍結連携','クリスタルエッジの使用速度を大幅上昇、後隙を短縮、CT計測を初撃時から開始。マナの激流が乗らない問題を修正。氷剣のクリスタルソードとオーロラのフローズングローブにも凍結付与を追加。','手数・ルーン相性・オート時の回転が大きく改善。')
add('frostmage','2025-05-29','強化','アイススパイク／究極技の改善','アイススパイクの攻撃係数を調整。アブソリュートゼロにブレイク3ゲージ相当を追加。凍結ギミックの追加に合わせた組み替え。')
add('bard','2025-05-29','強化','演奏ダメージとバフ維持','フィーバーが演奏スキルのダメージも増幅。戦場の歌の持続が10秒→30秒へ延長。即興演奏の「勇猛」獲得条件にメロディショック使用を追加。','支援更新頻度と演奏の攻撃性能が改善。')
add('warrior','2025-05-29','強化','アマランスキックと迎撃','アマランスキックの攻撃係数を調整、使用時ガード状態に変更、補助タグ追加。突撃ルーンで追加される貫きの増幅条件に無防備を追加。')
add('dancer','2025-06-19','仕様変更','喝采追撃が直接ダメージに','アドリブの強化効果発動時にCTをリセットし、テンポ2段階で即強化。喝采の追撃が「間接→直接ダメージ」に変更。','スキル・ステータスによる加算判定が変わるため、古いDPS議論に注意。')
add('dancer','2025-06-19','調整','フィナーレの熱気係数を再配分','フィナーレによる熱気の追加攻撃力係数を2倍へ、最大スタックは半減。前ステージとの単純倍率比較はできません。')
add('fighter','2025-06-19','仕様変更','応急処置の発動条件を追加','被弾時、最大HPの50%以下で攻撃力15%相当を回復、発動制限10秒と明示。常時発動の回復とは異なる。')
add('dualblade','2025-06-19','仕様変更','スプリット系に移動タグを追加','スプリットスラッシュ／ダウンと「熱傷」ルーン適用時に移動タグ追加。移動系宝石の評価に影響。')
add('mage','2025-06-19','不具合修正','マナインフィニティがリセットする対象を改善','マナインフィニティのCTリセットがマナストーム／増幅ルーンに効かない問題を修正。ファイアボールの全スタックも即時充填するよう変更。')
add('frostmage','2025-06-19','強化','クリスタルエッジのモーションを再加速','スキルの実行モーションを以前より速く変更。5月の調整から続く操作時間短縮。')
add('lightning','2025-06-19','新職追加','電撃術師がS0途中に追加','6月19日に新しい魔法系転職として実装。韓国2025年3～5月の初期ランキングに雷が存在しないのは当然です。','台湾・日本への実装時期とは区別。')
add('archer','2025-07-17','強化','主要7スキルのダメージ+10%','アロ―リボルバー、マグナムショット、サイドステップ、ホークショット、エスケープステップ、灼熱の軌跡、多発射撃のダメージを一律10%増（ルーン改造後の技も対象）。')
add('priest','2025-07-17','不具合修正','翼ルーンの射出回数を修正','ディヴァインウィングに翼ルーン適用時、9秒間で6発の投射を撃つよう修正。')
add('dualblade','2025-07-31','強化','活気・風の刃をさらに強化','活気の「連打時の強化スキル威力増加」20%→30%。風の刃の通常攻撃時追加リソース獲得確率20%→25%。')
add('rogue','2025-07-31','強化','隠密攻撃の発動条件と隠身火力を再設計','スニークアタックを「ブレイク時10秒の通常攻撃+30%追加」から「初撃／隠身解除時7秒の追加攻撃率+15%」に変更。隠身の追撃ダメージが約+472.5%、間接→直接ダメージへ変更。','ブレイク依存から開幕・隠身解除中心へ。数値だけでなく発動機会が変わります。')
add('rogue','2025-07-31','強化','アドレナリンの攻撃速度','オーバーチャージ時の攻撃速度補正20%→40%。')
add('archer','2025-07-31','仕様変更','射程と位置取りを改善','通常攻撃10→12m、サイドステップ12→15m。アローリボルバー／マグナムショット使用時の後退を廃止。灼熱の軌跡の追加攻撃を直接ダメージへ修正。')
add('longbow','2025-07-31','強化','究極技補正の適用漏れを修正','デススティンガー、デッドリーショット、ドラゴンベインに究極技ステータスが乗っていなかった問題を修正。ハートシーカーのノックバック5→1.8m。','攻撃力だけでは見えないスキルの有効打と安定性の改善。')
add('longbow','2025-07-31','仕様変更','ブレイクタイプ変更・押し出し抑制','デススティンガーとデッドリーショットのブレイクをブロー→スタンへ。超音波ルーン付きハートシーカーが敵を押し出さないよう変更。')
add('musician','2025-07-31','強化','星のソナタと終焉、集中攻撃','星のソナタの連携猶予10→12秒。凶声ルーン付き「第3楽章：終焉」のダメージ約+117.4%。「第3楽章：激情の嵐」は対象が少ない場合余った攻撃を対象へ集中。','多対少・単体のダメージが従来と大きく変わります。')
add('mage','2025-07-31','不具合修正','マナインフィニティ下のファイアボール重複','究極技後のファイアボールが同一対象に重複命中しない不具合を改善。重複時のダメージ比率50%を明記。')
add('priest','2025-07-31','不具合修正','ホーリースピアに詠唱速度を適用','キャスト速度上昇がホーリースピアに乗らない不具合を修正。')
add('monk','2025-07-31','不具合修正','連携スキルの向き','「殺到」「雷霆打」を使う際、標的と違う方向へ発動することがある問題を修正。')
add('dualblade','2025-08-21','強化','フューリー・ハリケーンを強化','グライディング／ライトニングフューリーがクリティカル時に追撃し、連打タグ追加。3960ハリケーンは移動速度+30%、旋回時間と攻撃周期を半減。','多段攻撃と移動しながらの削りが強化。')
add('dualblade','2025-08-21','強化','ハウリング系に耐久と耐妨害','ハウリングゲイル／テンペスト使用中に被ダメージ50%減とノックバック無効化を追加。')
add('mage','2025-08-21','強化','アイスダガーの基本設計を変更','詠唱1秒→0.5秒、マナ20→7。追撃投射を再入力なしで周囲の敵に発射する方式に変え、凍結付与のタイミングを最終撃→初撃へ移動。','操作負担・燃費・状態異常付与が大幅改善。')
add('mage','2025-08-21','強化','霜の棘・山崩れ・隕石を強化','霜の棘の投射ダメージ+100%、隕石着弾即時ダメージ+50%。山崩れは12秒間の元素ダメージ+10%追加、射程7.5→10m。','「旧韓国魔法使いが弱かった」という評価は特にこの日以前か確認したい。')
add('mage','2025-08-21','強化','エレメンタルハーモニー／DoTを改善','ファイアボール・アイスダガーの元素調和DoT+50%、隕石・霜の棘の該当DoT+250%。ライトニングの落雷ルーンによる感電DoT+25%。')
add('rogue','2025-08-21','仕様変更','スニークアタックの開幕判定改善','隠身へ入ったときにも追加攻撃率上昇効果が発動。毒霧ルーン付きポイズントラップの直接攻撃にも毒属性を付与。')
add('crossbow','2025-08-21','強化','バスターショットに移動速度バフ','使用後5秒、移動速度+10%。強化ボルト装填キャンセル時の消失問題も修正。')
add('bard','2025-08-21','強化','楽想生成とCT循環を改善','ストリングショットで現在と異なる楽想を等確率取得。楽想獲得ごとにバズテイルCT-1秒、和音ルーン付きトリプルストロークCT-2秒。')
add('bard','2025-08-21','強化','勝利のセレモニーとオート','勝利のセレモニーのシナジーダメージ増加10%→15%。アシストモードでは「死んだふり」を自動使用しない仕様へ。','支援量と半オートの事故防止が改善。')
add('healer','2025-08-21','強化','自己回復・HP比例攻撃・設置火力','生命の鼓動で自分自身も回復。プロテクションが敵に付与する弱体に「敵の残HPが多いほど与ダメ増」を追加。光群ルーンはリンク中でも標的付近に範囲攻撃の光結晶を追加。','ヒーラー＝回復専門ではなく、攻撃補助と自己耐久が上昇。')
add('healer','2025-08-21','不具合修正','転移パッシブのルーン連携','誓約・包容などの効果が転移パッシブを正しく受けられない／追加シールドが吸収しない問題を修正。')
add('priest','2025-08-21','強化','聖戦パッシブに神聖力消費時の最終補正','神聖力1消費につきスキルの最終ダメージ+1%。弱化発動時は10秒で神聖力40回復。ディヴァインウィングにブレイク0.5ゲージ相当（翼付きは投射1発0.25）を追加。','次月のS1で+1%→+0.8%へ下方修正される点に注意。')
add('monk','2025-08-21','強化','化身中の火力と悟り発動率','化身中の「殺到」「雷霆打」ダメージ増加25%→100%、悟りパッシブ発動率30%→60%。信念の要塞内のノックバック耐性も改善。','S0後半だけで強化状態の価値が大きく変わりました。')
add('dancer','2025-08-21','強化','喝采の内部CTとアンコールを改善','喝采付きアドリブの追撃バフ重複問題を修正し、内部CTを除去してスキル1回につき1回発動。アンコールをアクティブスキルLv合計に応じ最大300%ダメージへ強化、使用中移動速度+30%。','多人数PTの採用評価は8月前後で結論が変わり得ます。')
add('dancer','2025-08-21','強化','ウィンドミルとピルエット','ウィンドミル使用中のノックバック無効化。ピルエットの強化ルーン効果が正しく反映されない問題も修正。')
add('firemage','2025-09-04','仕様変更','標的消失時のスキル継続','フレイムキャノン／ラピッドファイアの途中で標的が消えても旧方向へ継続。クロスファイアは旧標的位置へ発射。','移動ボスや雑魚切替時の手動・オートの取りこぼしを軽減。')
add('mage','2025-09-04','不具合修正','テレキネシスのオート停止を修正','クラス特化アシスト中にテレキネシスが使われず戦闘が停止する問題を修正。')
add('bard','2025-09-04','不具合修正','弱点露出の消費判定を修正','ストリングショット／サプライズショットの弱点露出が間接ダメージで消費されないよう変更。')
add('musician','2025-09-04','不具合修正','永遠の旋律のCT短縮対象','残りCT0.5秒以下のスキルをランダムCT短縮の対象に選ばないよう修正。')
# --- 韓国 Season 1 開始の公式変更 ---
add('warrior','2025-09-25','強化','ブレイク延長専用のクエイク追加','ブレイク対象へクエイクを使用し、ブレイク継続時間とその間の被ダメージを増やす。戦場の咆哮の強化持続8→25秒、覇気ルーンのダメージ+36.4%、復讐心10→15秒。','盾役・ブレイク支援の役割が明確化。')
add('greatsword','2025-09-25','強化','肩当て・踏みつけのCT短縮','ショルダーチャージとストンプのCT12→9秒（それぞれ25%短縮）。報復のHP消費条件は料理効果適用前のHP基準へ変更。','近接回転率とHP管理の安定に関わる。')
add('swordmaster','2025-09-25','調整','集中弱体化と主要攻撃の大規模上方','集中のクリダメ+50%→+30%。一方、鋼鉄楔+44%、鞘打ち／圧迫+40%、秘剣・鋼鉄楔+40%、秘剣・鞘打ち+30%、一閃+21%、落花+37.5%。落花にブレイク+1と集中30回復を追加。','パッシブは下方、主力スキルやリソース回収は上方。総DPSの単純合算は不可。')
add('archer','2025-09-25','仕様変更','弱点貫通の新パッシブと多発射撃改修','攻撃時25%で最終ダメ+20%の弱点貫通を追加。多発射撃を40ヒットで解放し、その後の命中で威力増。ホークショットの標的中は弱点貫通を確定適用。多発射撃の同一対象への重複ダメージには大幅減衰。','単体と範囲で運用が違い、以前の多発射撃評価と単純比較できない。')
add('crossbow','2025-09-25','強化','速度パッシブの対象変更と火薬強化','クイックアタックが攻撃速度上昇→スキル使用速度上昇に変更。火薬ルーンのバスターショット範囲ダメ+50%／粉塵+300%、ヘルファイア矢+50%／爆発+75%。','5月のガスティングボルト調整後も、火薬寄りの別ルートが強化。')
add('longbow','2025-09-25','強化','鋭い矢の出血をスキル命中で発動','発動条件を通常攻撃命中→スキル攻撃命中へ。発動間隔-1秒、出血ダメージ+100%、強打・補助タグ追加。','手動でスキルを回すほど出血が更新されやすくなります。')
add('mage','2025-09-25','弱体化','雷主体のダメージと究極回収を調整','ライトニングのダメージ-22%、感電DoT-25%。ライトニングおよび落雷ルーンの究極ゲージ獲得量-30%。アイスダガー／霜の棘のタグは生存→妨害へ変更、テレキネシス範囲+10%。','8月の氷・火系の強化と9月の雷系弱体化が重なり、3属性間の比重が変化。')
add('firemage','2025-09-25','強化','熱気獲得と火柱の火力向上','ラピッドファイア＋火種ルーンの熱気基本獲得10→15。ファイアストーム＋火柱ルーンのダメージ+53.8%。熱風ルーンの熱気基本獲得10→20。','熱気の立ち上がりと範囲主力の出力が改善。')
add('frostmage','2025-09-25','調整','面攻撃・クリスタルエッジを増強','フリージングフィールド+53.8%、冬+41.2%、グレイシアカッター／北風+42.8%。クリスタルエッジ初撃+66.6%、2撃+50%、3撃+40%。究極強化フィールドと通常フィールドの重複ダメージを許可。','5月のモーション改善と組み合わせると旧韓国データと大きく異なります。')
add('frostmage','2025-09-25','弱体化','凍結パッシブを引き下げ','刺すような冷気（사무치는 냉기）のダメージ-53.4%、アイシクルマークの凍結ダメージ-25%。凍結に必要なスタック20→25。','氷魔全体の与ダメージが一律+40%以上になったわけではありません。')
add('frostmage','2025-09-25','仕様変更','ブレイク延長アイシクルシャックル追加','ブレイク中の敵に氷槍で追撃してブレイク時間を延長。ブレイク中の追加被ダメージ効果も付与。','韓国S1の日付は9/25。ただし台湾S0には先行搭載の報告があるため、JP新要素とは限らない。')
add('lightning','2025-09-25','調整','過充電・超越の運用を再調整','落雷のダメージ-10%、過充電1スタックの与ダメージ+10→+9%。破壊の閃光へ過充電の増幅を重ねて適用。超越中はスタック増減を停止し、発動時点のスタックを保持、終了時に消滅。','単純ナーフではなく、究極技前のスタック準備を重視する仕様へ。')
add('healer','2025-09-25','強化','誓約・光群の継続ダメージを大幅増','誓約付きライフリンクの持続ダメージ+500%、光群付きサモンルミナスの持続ダメージ+263%。抑圧ルーンの跳躍距離10→15m。リンクのアシスト挙動も修正。','支援一辺倒ではなく、攻撃ルーン運用の評価を変える修正。')
add('priest','2025-09-25','調整','聖戦を弱体化、蘇生を強化','聖戦の神聖力1消費ごとのダメージ増加を1→0.8%へ。ケルティッククロスの蘇生を10→20秒に延長し、救済の光にも蘇生を追加（シナジーダメージ+10%、毎秒HP0.5%回復）。','瞬間火力は下がる方向、パーティ支援は上昇。')
add('monk','2025-09-25','強化','光輝と業火のルーン火力を上方','化身＋光輝ルーンの起動ダメージ+90.9%、治癒＋業火ルーンの対象ダメージ+36.6%。','旧「火力が低い」評価と比較するとルーン前提が異なります。')
add('bard','2025-09-25','調整','勇猛の賛歌弱体・対価として別ルーン強化','勇猛の賛歌の演奏増幅+30→+15%。死んだふり中の被ダメ-40%、欺瞞ルーンのサプライズショット+75%、機転ルーンの反撃+81%。','最高支援量だけを比較した古いTier表には注意。')
add('musician','2025-09-25','仕様変更','演奏集中とオートの挙動改善','第3楽章：激情の嵐の攻撃が対象に集中しやすくなる変更。アシスト射程・クライマックス発動条件の不具合修正。','7月の単体集中変更と合わせ、操作や敵人数で差が出る。')
add('dancer','2025-09-25','強化','テンポとフィナーレのダメージ枠を変更','テンポが「スキルダメージ増加」→「最終ダメージ増加」に変更。フィナーレの熱気消費1単位あたりダメージを+100%。熱気保有時はスキル使用速度+10%。','最終ダメージ枠になり、他補正と相互作用が変化。')
add('dancer','2025-09-25','仕様変更','アンコールの耐性・タグ追加','アンコールに連打・移動タグ、発動中にノックバック無効／ブレイク無効を追加。')
add('rogue','2025-09-25','強化','ブリッツラッシュを倍増','ブリッツラッシュの連続ヒット部と最後の一撃をそれぞれ+100%。ポイズンアタックの連打・補助タグ追加。','究極技ダメージの寄与が大きく変わります。')
add('fighter','2025-09-25','強化','コンボ猶予と各主力技を大幅強化','連携・コンボ入力猶予5→10秒。チャージングフィスト各段階+150%、スクリューアッパー+50%、スラストキック+50%、スタンプキック＋跳躍ルーン+50%、バーストパンチ+30%。','S0初期の低評価をひっくり返し得る大型修正。')
add('fighter','2025-09-25','強化','射程と自己回復を拡大','バーストパンチ射程1.65→3m、前半段の範囲半径1.5→3m。応急処置回復量は攻撃力の15→20%。衝撃波に強打タグ追加。','近接の当てやすさ・生存性が上がり、理論火力以上に実戦差が出ます。')
add('dualblade','2025-09-25','強化','ファイナルヒットを大幅強化','ファイナルヒットの連撃ダメージ+50%、最後の一撃+50%。','5月～8月の段階的な強化を踏まえて評価すべき究極技。')
# --- S1初期：launch 後の見逃せない追加変更 ---
add('mage','2025-10-23','強化','メディテーションに詠唱速度連携を追加','持続マナ回復の発動間隔をキャスト速度に応じて短縮。キャストスキルのCTがキャスト速度に応じて加速し、速度判定はスキル使用時に決定される。','速度装備・超自然+等との組み合わせは、この日以前と以後で仕組みが違います。')
add('mage','2025-10-23','不具合修正','ウーレ・岩石系のCT加速不具合','雷鳴／岩石ルーン適用時にマナストームのCT加速が働かない問題を修正。究極技終了後にメディテーションの継続回復が消える不具合も修正。')
add('warrior','2025-10-30','強化','ブレイドスマッシュ／貫きの火力','崩壊ルーン付きブレイドスマッシュ+20%、圧倒の補正を攻撃力→最終ダメージへ変更。極点ルーン付き突き+30%、ブレイドインパクト+30%。','戦士を「タンクだけ」と見る初期評とは異なります。')
add('warrior','2025-10-30','強化','ガード性能を改善','盾打ち／アマランスキックのガード開始から5秒スーパーアーマー。ガード成功時の軽減25→50%、移動・チャージ中に動作が固まる問題を改善。')
add('firemage','2025-10-30','強化','インフェルノが大幅上方','1段階炎ビーム+100%、2段階炎ビーム+200%、2段階爆発+100%。チャネリング周期ごとに熱気6を生成し、さらに熱気の持続回復バフを獲得。','S1開始時の火柱強化に続く大幅な火力と燃費の改善。')
add('firemage','2025-10-30','仕様変更','バーニングソウルの増幅枠変更','バーニングソウルの増幅が攻撃力上昇→最終ダメージ上昇に変更。青炎ルーン付きフレイムキャノンの範囲2→3m。')
add('priest','2025-10-30','強化','ホーリースピアを確定クリティカルへ','通常時も光芒ルーン付きも確定クリティカル。クリティカル率に応じた追加ダメージを付与。サンクチュアリCTをディヴァインウィング／ケルティッククロス使用ごとに-1秒。','日本で司祭が想定以上に火力を出すなら重要な変更候補。')
add('priest','2025-10-30','強化','ケルティッククロスの審判ルーンを強化','審判ルーン付きケルティッククロスの基本攻撃+33.3%、回復範囲も拡大。')
add('bard','2025-10-30','強化','即興演奏+で強化持続延長','バズテイル、戦闘交響曲、勝利のセレモニーのバフ持続+6秒。複数演奏スキル+10%、無我ルーン付き戦闘交響曲で確定究極の楽想を獲得。','PT支援の更新負担が軽減。CT短縮そのものが+6秒間続くわけではない。')
add('musician','2025-10-30','強化','カデンツァを大幅強化','基本DoT+287%、演奏ダメージ+284%。最大6回演奏で終了し、①～⑤のスキル使用でその枠のダメージ+25%（15秒／3重複）、⑥で最終ダメ+5%（15秒／3重複）。','単体火力・パーティ支援・スキル順が大きく変わる修正。')
add('musician','2025-10-30','仕様変更','セレナーデ＋魅惑ルーンのチャネリング','魅惑ルーン付きセレナーデはチャネリング3.5秒、発動周期0.7秒へ。')
# Meta / professional caveats
INSIGHT={
 'warrior':'5/8の闘志・迎撃→S1のブレイク延長→10/30のガード／ダメージ枠強化。早期の「盾役だけ」の評判では今の手触りを説明しきれません。',
 'greatsword':'9/25のCT25%短縮が主な確認済み数値変更。HP条件の判定仕様にも注目。その他の時期に変更が無かったと断定する意味ではありません。',
 'swordmaster':'S1の集中-20ポイントと主要技の大幅強化が同時に入っています。単純に「ナーフ」「バフ」のどちらかへ分類するのは不正確。',
 'archer':'7/17の主力一律+10%、7/31の射程強化、9/25の弱点貫通＋多発射撃再設計の連続変更が重要。',
 'crossbow':'5/29のガスティング調整で初期の突出を抑え、9/25には火薬／ヘルファイアを再強化。評価時期とビルドが合わないと判断が逆転します。',
 'longbow':'7/31の究極補正適用、9/25の出血パッシブの大改修。単体ボスへの継続的な性能を見直す必要があります。',
 'mage':'8/21の氷・火寄り強化、9/25の雷寄り下方、10/23の詠唱速度→CT連携追加と、わずか2か月間で構成評価が何度も変わっています。',
 'firemage':'9/25の熱気生成・火柱強化に10/30のインフェルノ大型強化。短時間戦と長期戦での評価を分けると理解しやすい。',
 'frostmage':'5/29の凍結導入と高速化、9/25の主力強化・凍結下方を両方見るのが重要。韓国初期の評価をそのまま日本へ流用できません。',
 'lightning':'6/19に初登場、9/25の過充電・超越変更。韓国3～5月の評価データは存在しません。',
 'healer':'5/8の攻撃寄り支援、8/21の自己回復と追加火力、9/25の攻撃ルーンDoT強化。ヒーラー＝回復専業の印象は更新が必要です。',
 'priest':'5/8と8/21に神聖力回転を強化、9/25に聖戦補正を抑え、10/30にホーリースピア確定クリティカル。10月末以前の比較は別世代です。',
 'monk':'5/8・8/21・9/25の各段階で火力が伸びています。特に8/21の化身中+25→+100と9/25の光輝+90.9%が重要。',
 'bard':'5/29の30秒バフ、8/21のCT循環、9/25の勇猛下方、10/30の支援更新改善。PT支援量と本人DPSを混ぜないで評価。',
 'musician':'7/31の終焉+117.4%、9/25の集中攻撃、10/30のカデンツァ大型強化。遠距離支援だけでなく火力評価も変化。',
 'dancer':'6/19追撃判定変更、8/21喝采CT撤廃、9/25最終ダメージ枠化。パーティ人数・バフ消費速度で強さが変わります。',
 'rogue':'7/31の隠身追撃+472.5%と9/25のブリッツラッシュ+100%が大きい。初期低評価と比較するなら必須の履歴。',
 'fighter':'9/25のコンボ猶予倍増と主要スキル大幅強化が決定打。S0の古い評価を日本へ持ち込むと最も誤りやすい職の一つ。',
 'dualblade':'5/29→7/31→8/21→9/25の四段階の強化。韓国S0序盤の評判をそのまま使うのは危険。'
}
assert len(CL)==19 and len(INSIGHT)==19
for r in R: assert len(r['detail'])>10
out={'metadata':{'title':'韓国S0後半〜S1初期 全19職バランス調整史','last_verified':'2026-11-07','region':'韓国','scope':'2025-04-24〜2025-10-30','caveat':'KR公式パッチ。日本実装の個別差分ではない。取得できた主要変更を抽出したもので全微修正を網羅しない。','sources':[{'date':d,'label':label,'url':url} for d,(label,url) in S.items()]},'classes':[{'slug':c['slug'],'name':c['name'],'family':c['family'],'icon':c.get('icon','✦'),'insight':INSIGHT[c['slug']],'changes':sorted([x for x in R if x['class']==c['slug']],key=lambda x:x['date'])} for c in [*J,CL['lightning']] ]}
(P/'data/class-balance-history.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
e=html.escape
# Build static HTML; JS only for optional filtering, no dependencies/API needed.
parts=[]
parts.append('''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#09111e"><meta name="description" content="2025年韓国版マビノギモバイルのS0後半～S1初期、全19職のパッチノートを時系列に対比。日本語要約と韓国公式原文を掲載。"><title>韓国S0後半～S1初期 全19職のバランス調整履歴｜エリン調査ノート</title><link rel="stylesheet" href="../assets/site.css"><link rel="stylesheet" href="../assets/class-balance-history.css"><script defer src="../assets/site.js"></script><script defer src="../assets/class-balance-history.js"></script></head><body><div id="siteNav" data-current="balance" data-root="../"><a href="../index.html">ホーム</a></div><main class="portal-wrap"><section class="job-hero"><div class="portal-kicker">KR PATCH ARCHIVE · 2025.04–10</div><h1 class="portal-page-title">韓国S0後半～S1初期<br>全19職 バランス調整履歴</h1><p class="portal-lead">「韓国では弱かった職が、日本では意外と強い」の理由を探すための時系列資料。韓国の公式パッチを日本語に要約し、<strong>変更前後の数値・操作感・ルーン連携</strong>を職業別に整理。</p><p class="balance-scope">対象：2025年4月24日～10月30日／S1開始日：2025年9月25日／19職（電撃術師を含む）</p></section>
<div class="job-warning"><strong>重要：</strong>これは<strong>韓国版での変更履歴</strong>です。日本版が「韓国S1状態」と感じられても、同じアップデート内容を同日にすべて反映した証拠にはなりません。変更数値は韓国当時の値であり、現在の日本版数値・最強職ランキングではありません。スキル・ルーン名の一部は日本語仮訳です。</div>
<nav class="content-jumps"><a href="index.html">職業攻略一覧</a><a href="../content/season1.html">S1コンテンツ年表</a><a href="../guides/rune-transcend.html">S1ルーン仕様</a><a href="#common">共通の戦闘変更</a><a href="#sources">出典一覧</a></nav>
<section class="portal-panel balance-overview"><h2>まず押さえる5つの転換点</h2><div class="balance-milestones"><div><b>5/29 · S0中盤</b><p>氷魔の凍結追加・速度改善／デュアルのパッシブ改修／石弓の突出調整</p></div><div><b>7/31 · S0後半</b><p>盗賊の隠身追撃+472.5%／楽師「終焉」+117.4%／弓の射程・デュアル再強化</p></div><div><b>8/21 · S0最終盤</b><p>魔法使いの氷/火寄り強化、ヒーラー自己回復、修道士化身、ダンサー喝采、デュアル高速化</p></div><div><b>9/25 · S1開始</b><p>全19職の大型調整。格闘家+150%など、雷魔術と氷魔パッシブには下方も</p></div><div><b>10/23・10/30 · S1初期</b><p>魔法使いメディテーションに詠唱速度連携／司祭槍確定クリ／火炎インフェルノ／楽師カデンツァ</p></div></div><p class="balance-note">強化率は原文に書かれたスキル倍率の増分。例「+150%」は当該攻撃の改修であって、職全体のDPSが2.5倍という意味ではありません。</p></section>
<section class="portal-panel" id="common"><h2>全職に影響するS1の共通変更</h2><p><b>2025年9月25日：</b>ブレイク済みの敵に対して一定のブレイク延長が可能になる「ブレイクエクステンド」を追加。複数人使用時には延長効率が減衰し、被ダメ増加は重複しません。さらに、ダメージ増加の相互計算と各ブレイク種別の増幅を調整。従来低かった魅惑・恐怖系を含むブレイク性能を見直しています。</p><p>したがって、<strong>S0とS1のDPS順位は、個別スキルの変更だけでは比較できません。</strong>ブレイク頻度・タグ・新★8ルーン・パーティ構成も変化しています。</p><a class="balance-source" href="https://mabinogimobile.nexon.com/News/Update/3147463" target="_blank" rel="noopener noreferrer">韓国公式9/25パッチノート ↗</a></section>
<section class="portal-panel"><h2>職業・時期・修正内容で絞り込み</h2><div class="balance-filters"><label>職業<select id="balanceClass"><option value="all">19職すべて</option>''')
for c in out['classes']: parts.append(f'<option value="{e(c["slug"])}">{e(c["name"])}</option>')
parts.append('''</select></label><label>時期<select id="balancePhase"><option value="all">S0＋S1</option><option value="S0">S0後半のみ</option><option value="S1">S1開始～10月</option></select></label><label>種別<select id="balanceType"><option value="all">すべて</option><option value="強化">強化</option><option value="弱体化">弱体化</option><option value="調整">強化・弱体化混在</option><option value="仕様変更">仕様変更</option><option value="不具合修正">不具合修正</option><option value="新職追加">新職追加</option></select></label><label>検索<input type="search" id="balanceSearch" placeholder="例：詠唱 クリティカル 冬" autocomplete="off"></label></div><p id="balanceCount" class="balance-count" aria-live="polite"></p><button type="button" class="balance-reset" id="balanceReset">フィルター解除</button></section>
<nav class="balance-job-jumps" aria-label="職業へ移動">''')
for c in out['classes']: parts.append(f'<a href="#class-{e(c["slug"])}">{e(c["name"])}</a>')
parts.append('</nav><div id="balanceList">')
for c in out['classes']:
 ch=c['changes'];parts.append(f'<section class="balance-class portal-panel" id="class-{e(c["slug"])}" data-class="{e(c["slug"])}"><div class="balance-class-head"><span class="balance-icon">{e(c["icon"])}</span><div><div class="balance-family">{e(c["family"])} · {len(ch)}件の主要変更</div><h2>{e(c["name"])}</h2></div><a class="balance-job-link" href="{e(c["slug"])}.html" {"aria-disabled=\"true\"" if c['slug']=='lightning' else ''}>職業攻略 ↗</a></div><p class="balance-takeaway">{e(c["insight"])}</p><div class="balance-events">')
 for x in ch:
  cls={'強化':'up','弱体化':'down','調整':'mix','仕様変更':'change','不具合修正':'fix','新職追加':'new'}[x['type']]
  imp=f'<p class="balance-impact"><b>実戦への意味：</b>{e(x["impact"])}</p>' if x['impact'] else ''
  parts.append(f'<article class="balance-event" data-phase="{x["phase"]}" data-type="{e(x["type"])}"><div class="balance-event-meta"><time datetime="{x["date"]}">{x["date"]}</time><span class="balance-tag {cls}">{e(x["type"])}</span><span class="balance-tag season">KR {x["phase"]}</span></div><h3>{e(x["title"])}</h3><p>{e(x["detail"])}</p>{imp}<a class="balance-source" target="_blank" rel="noopener noreferrer" href="{e(x["source"])}">韓国公式パッチ原文 ↗</a></article>')
 parts.append('</div></section>')
parts.append('''</div><section class="portal-panel" id="sources"><h2>韓国公式 出典一覧</h2><p>職業カードの「韓国公式パッチ原文」から、該当日のオリジナル告知を開けます。変更は日本語で要約しており、全文翻訳ではありません。公式告知に存在しない倍率を補ったり、未検証の日本版反映状況を断定したりしていません。</p><ul class="balance-source-list">''')
for d,(label,url) in S.items(): parts.append(f'<li><time datetime="{d}">{d}</time> <a target="_blank" rel="noopener noreferrer" href="{e(url)}">{e(label)} ↗</a></li>')
parts.append('''</ul><h3>収録方針と限界</h3><p>韓国2025年4月～10月の主要な数値調整・挙動変更・ビルドを左右する不具合修正を抽出。衣装・演出・単なる文言修正などは原則省略。各日付の修正を<strong>完全に網羅した監査資料ではありません</strong>。掲載のない時期に調整が無かったという意味でもありません。</p><p>雷は2025年6月19日に韓国S0へ追加。S1の10月16日に追加された暗黒術師は、19職の「S0から比較」範囲には含めていません。日本版の正式な現在値を検証する場合はゲーム内表示を最優先してください。</p></section><footer class="portal-foot">個人研究サイト／調査更新 2026-11-07。韓国NEXON公式パッチを日本語要約。各国実装の差分・DPS順位は未断定。</footer></main></body></html>''')
(P/'jobs/balance-history.html').write_text(''.join(parts),encoding='utf-8')
css='''/* 独立：KR職業バランス調整史 */
.balance-scope,.balance-note{color:#abc2d6;font-size:.92rem;line-height:1.7}.balance-scope{margin-top:12px}.balance-milestones{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}.balance-milestones>div{padding:14px;border:1px solid #34516b;border-radius:13px;background:#142337}.balance-milestones b{color:#86dfff}.balance-milestones p{font-size:.88rem;line-height:1.65;margin:.6rem 0 0}.balance-filters{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:13px}.balance-filters label{font-size:.87rem;font-weight:700;color:#abd8ec;display:grid;gap:6px}.balance-filters input,.balance-filters select{width:100%;min-width:0;box-sizing:border-box;border-radius:10px;padding:12px 14px;background:#15263b;color:#fff;border:1px solid #3a607b;font-size:1rem}.balance-reset{border:1px solid #3e6d84;background:#1a3b4e;color:#dcf7ff;border-radius:10px;padding:10px 14px;cursor:pointer}.balance-count{color:#9ee7d9;font-weight:700}.balance-job-jumps{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0}.balance-job-jumps a{padding:8px 11px;border:1px solid #32516c;border-radius:100px;color:#d9ebf4;text-decoration:none;font-size:.85rem;background:#162a3e}.balance-job-jumps a:hover,.balance-job-jumps a:focus{border-color:#79d8ef}.balance-class{margin-bottom:18px;scroll-margin-top:90px}.balance-class-head{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.balance-icon{font-size:1.7rem}.balance-class-head h2{margin:0}.balance-family{font-size:.83rem;color:#9db9ca}.balance-job-link{margin-left:auto;color:#85dfe7;text-decoration:none;font-size:.85rem}.balance-takeaway{background:#173345;border-left:4px solid #59b7cb;border-radius:6px;padding:12px 14px;line-height:1.75}.balance-events{display:grid;gap:11px}.balance-event{padding:17px;border:1px solid #314c65;border-radius:12px;background:#101e2f}.balance-event-meta{display:flex;gap:8px;align-items:center;flex-wrap:wrap;color:#bad2e4;font-size:.85rem}.balance-event h3{margin:9px 0 7px;font-size:1.07rem}.balance-event p{line-height:1.78;font-size:.94rem;margin:5px 0 9px}.balance-tag{font-size:.75rem;padding:2px 7px;border-radius:6px;background:#34445a;color:#e3f1ff}.balance-tag.up{background:#134b44;color:#a2f3cb}.balance-tag.down{background:#522b3b;color:#ffc6d1}.balance-tag.mix{background:#55462b;color:#ffdb9b}.balance-tag.fix{background:#28445c;color:#b1e0ff}.balance-tag.new{background:#35496d;color:#ddd7ff}.balance-impact{color:#c8e8ed}.balance-source{display:inline-block;color:#83dce8;font-size:.84rem;margin-top:5px;text-decoration:underline;text-underline-offset:3px}.balance-source-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:6px 18px}.balance-source-list li{line-height:1.7}.balance-source-list a{color:#81dfec}.balance-class[hidden],.balance-event[hidden]{display:none!important}@media(max-width:700px){.balance-filters{grid-template-columns:1fr}.balance-milestones{grid-template-columns:1fr}.balance-class-head{align-items:flex-start}.balance-job-link{flex-basis:100%;margin-left:0}.balance-event{padding:12px}.balance-job-jumps a{font-size:.79rem}}'''
(P/'assets/class-balance-history.css').write_text(css,encoding='utf-8')
js='''(function(){const by=id=>document.getElementById(id),cls=by('balanceClass'),phase=by('balancePhase'),typ=by('balanceType'),q=by('balanceSearch'),count=by('balanceCount'),panels=[...document.querySelectorAll('.balance-class')];function update(){let jobs=0,changes=0;const search=q.value.trim().toLocaleLowerCase();panels.forEach(p=>{let n=0;p.querySelectorAll('.balance-event').forEach(ev=>{const ok=(phase.value==='all'||ev.dataset.phase===phase.value)&&(typ.value==='all'||ev.dataset.type===typ.value)&&(!search||(p.querySelector('h2').textContent+' '+ev.textContent).toLocaleLowerCase().includes(search));ev.hidden=!ok;if(ok)n++});p.hidden=n===0||(cls.value!=='all'&&p.dataset.class!==cls.value);if(!p.hidden){jobs++;changes+=n}});count.textContent=`表示：${jobs}職・${changes}件の主要変更`;};[cls,phase,typ].forEach(x=>x.addEventListener('change',update));q.addEventListener('input',update);by('balanceReset').addEventListener('click',()=>{cls.value='all';phase.value='all';typ.value='all';q.value='';update()});if(location.hash.startsWith('#class-')){const key=location.hash.slice(7);if(panels.some(p=>p.dataset.class===key)){cls.value=key;}}update()})();'''
(P/'assets/class-balance-history.js').write_text(js,encoding='utf-8')
# source of truth link repair: electrification in S0 was not present in existing v8 job pages
b=(P/'jobs/balance-history.html').read_text(encoding='utf-8');b=b.replace('<a class="balance-job-link" href="lightning.html" aria-disabled="true">職業攻略 ↗</a>','<span class="balance-job-link">個別攻略：準備中</span>');(P/'jobs/balance-history.html').write_text(b,encoding='utf-8')
# Global nav (keep compact; new item is actionable)
nav=P/'assets/site.js';s=nav.read_text(encoding='utf-8');s=s.replace("['jobs/index.html','職業別攻略','jobs'],","['jobs/index.html','職業別攻略','jobs'],['jobs/balance-history.html','韓国の職業調整','balance'],");nav.write_text(s,encoding='utf-8')
# Add card on home next to existing job content
p=P/'index.html';s=p.read_text(encoding='utf-8');anchor='  <a class="home-card home-job-feature"';k=s.index(anchor)
card='''  <a class="home-card" href="jobs/balance-history.html"><div class="icon" aria-hidden="true">◷</div><div class="label">KR HISTORY · 19 CLASSES</div><h2>韓国S0～S1 職業調整史</h2><p>5月末・8月・S1開始・10月までの公式パッチを職業別に比較。旧評価と現在の強さが違う理由を追う。</p><div class="go">19職の変更履歴を読む →</div></a>\n'''
s=s[:k]+card+s[k:];p.write_text(s,encoding='utf-8')
# content hub cross-link
p=P/'content/index.html';s=p.read_text(encoding='utf-8');s=s.replace('<a href="../guides/rune-transcend.html">S1ルーン超越</a>','<a href="../guides/rune-transcend.html">S1ルーン超越</a><a href="../jobs/balance-history.html">韓国S0～S1職業調整</a>');s=s.replace('''<a href="season1.html"><span>🔮</span>''','''<a href="../jobs/balance-history.html"><span>⚔️</span><h2>韓国19職のS0→S1調整史</h2><p>時系列・職別・強化/弱体/仕様変更のパッチ比較。</p><b>詳しく見る →</b></a><a href="season1.html"><span>🔮</span>''');p.write_text(s,encoding='utf-8')
# Add unobtrusive link to each job (non-lightning)
for c in J:
 p=P/f'jobs/{c["slug"]}.html';s=p.read_text(encoding='utf-8')
 if 'balance-history.html' not in s:
  marker='<main class="portal-wrap">';s=s.replace(marker, marker+f'<div class="balance-entry-link" style="margin:8px 0 16px"><a href="balance-history.html#class-{c["slug"]}">韓国S0～S1のこの職の調整履歴 ↗</a></div>',1);p.write_text(s,encoding='utf-8')
# Add link from jobs index into header
p=P/'jobs/index.html';s=p.read_text(encoding='utf-8');marker='<main class="portal-wrap">';s=s.replace(marker,marker+'<div class="balance-entry-link" style="margin:8px 0 16px"><a href="balance-history.html">韓国公式パッチで見る全19職の変遷（S0後半～S1初期） ↗</a></div>',1);p.write_text(s,encoding='utf-8')
print('classes',len(out['classes']),'changes',len(R),'html',round((P/'jobs/balance-history.html').stat().st_size/1024),'KB')
print('by class',[(c['name'],len(c['changes'])) for c in out['classes']])
