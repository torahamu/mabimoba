# エリン調査ノート v8 — クラスLv1〜65 必要経験値表（2026-11-06）

## v8 の変更

- `growth/index.html` のクラス育成表を **Lv1〜65の65行**に変更。各到達Lvについて「前Lvからの必要EXP」「Lv1からの累積EXP」「必要な精霊の痕跡」「累積の痕跡」を表示。
- 1レベル刻みで現在Lvと目標Lvを指定できるように変更し、**EXPと痕跡を同時表示**。
- スマホではテーブル内だけ横スクロール。到達Lv列を左に固定。Lv25/35/40/45/55/65を強調。
- `data/class-exp.json` が新しい65行の正本。`scripts/rebuild_growth_v8.py` によりテーブル・JavaScript・CSSを再生成（再実行可能）。
- `data/class-traces.json` はv7の節目テーブルとの互換のため保持。新しい表・計算機は `class-exp.json` の65行を利用。

### 先行EXPの出典と不確かさ

韓国Season 0の2025年5〜6月のプレイヤー実測表に準拠し、日本版の公式EXP表ではありません。
採用した系列のLv1→65累計は **2,688,083,277 EXP・痕跡134,405個**。別系列には **3,137,751,367 EXP・約156,888個**、さらにLv64→65の単独EXPを **400,000,000** とする報告もあり、ページ内で明記しました。
「精霊の痕跡」は1個につきクラスEXP20,000の先行説明がありますが、端数の繰り越しや取得済み経験値で実際の消費数は変わる可能性があります。

**参考**：韓国Lv別経験値 [Adimpnem](https://adimpnem.tistory.com/149)、[Begchi](https://mabinogi.begchi.com/%EB%AA%A8%EB%B0%94%EC%9D%BC-%ED%81%B4%EB%9E%98%EC%8A%A4-%EA%B2%BD%ED%97%98%EC%B9%98-%ED%85%8C%EC%9D%B4%EB%B8%94-%EC%A0%95%EB%A0%B9%EC%9D%98-%ED%9D%94%EC%A0%81-%EC%86%8C%EB%AA%A8%EB%9F%89)、[台湾Lv1〜51実測](https://forum.gamer.com.tw/C.php?bsn=32564&snA=2853)。

### 差し替え方法

- **フルZIP**：解凍して既存GitHub Pagesのサイト直下へ上書き。
- **差分ZIP**：既存v7に上書き（変更ファイル6点）。
- v8の再生成: `python scripts/rebuild_growth_v8.py`。表示チェック: `python scripts/qa_v8_growth.py`（要PlaywrightとChromium）。

---

# エリン調査ノート v7 — ステータス・クラス育成・装備・戦闘判定（2026-11-06）

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

※ `build_v7.py` は通常は一度きり。既存indexとリンクへ上書きするため、繰り返し実行時は挿入済みカードを重複させないよう手動確認してください。サイトを配布・編集する場合は生成されたHTML・JSON・CSS・JSを直接更新して問題ありません。

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

# マビノギモバイル攻略ポータル v6 — 職業スキル公開情報調査（2026-11-02）

## 今回の調査・反映結果

**対象18職／掲載スキル・派生技116件／番号を資料で確認56件／個別タグ26件／対応ルーンの掲載関係114件**。

- 各職の日本語スキル名と基本効果をGameWithと照合して独自に要約しました。旧v5ではルーン改造説明だけだったスキルも補いました。
- 究極技の日本語名を追加しました。**各職①〜⑥すべての実機スクリーンショット確認ができたわけではありません**。先行Wikiに番号が載っていた職だけ表示し、そのほかは`—`を維持します。
- スキルタグの個別表は氷結術師、司祭、格闘家、剣術士、吟遊詩人を中心に確認できた一部だけ掲載しました。他職のタグは未確認です。**タグは日本Season 0実機未検証の先行情報です**。
- 氷結術師の「グレイシアカッター」「アイススパイク」など、出典によるタグの違いは**異説として別色表示**し、どれが正しいか断定していません。
- 日本語訳揺れ（クロスボウ使いの「スプレッディングボルト」→「スプレッドボルト」など）を整理し、元のルーン効果本文は改変せず残しました。
- 従来の18職ルーン採用率・戦闘指南・宝石・ペット・コンテンツ/Season 1ページ、530件ルーン図鑑、ダメージ計算、交換週数計算は維持しています。
- 確認できていない番号・タグ・派生技には注記を表示しています。出典は職別ページ下部および`data/job-skills.json`、`RESEARCH_STATUS.md`を参照してください。

### 編集・再生成

```bash
# ルーンDBを改訂したときだけ実施
python scripts/build_skill_data.py
# 公開情報で照合したスキル説明・番号・タグを再適用
python scripts/apply_research_v6.py
# HTML再生成と検証
python scripts/rebuild_jobs.py
python scripts/qa_v5.py
```

`build_skill_data.py`だけ実行すると今回追加した手動調査データが上書きされるため、必ず`apply_research_v6.py`を続けて実行してください。

---

# 旧版v5からの継続メモ — スキル×ルーン対応表

## v5の追加内容（2026-11-01）

- `jobs/*.html`（18クラス）に**スキル別解説・対応アクセサリールーンと効果**の一覧を追加。ページ内「スキル・改造」へジャンプできます。
- 既存のルーン図鑑530件から、日本版実装扱いのアクセサリールーンをスキル名で照合。**スキル名100件・対応ルーン114件**。同じルーンが複数スキルに影響する場合は両方に掲載しています。
- `frostmage.html` はスキル①〜⑥・タグの先行照合、`healer.html` は①〜⑥の番号の先行照合、`mage.html` は一部スロット番号の先行照合。司祭は全スキルが補助タグという先行情報を参考にタグを掲載。ルーン装着でタグや名称が変わる場合、日本ゲーム内説明を優先してください。
- **他の職はスキル別の正確な番号やタグが未照合**。架空の番号やタグは置かず、`—`、`個別タグ：要実機確認` と表示しています。究極技を含む全アクティブスキル・パッシブの網羅ではなく、「日本版ルーン説明に登場するスキル」を中心とした第1段階です。
- 全18職の日本語スキル名・説明の参照リンクにGameWithを追加。著作物を丸写しせず、スキル解説は独自の要約です。
- `data/job-skills.json`: スキル名・確認済み番号・タグ・概要・対象ルーンをまとめた生成データ。
- `data/skill-notes.json`: 独自のスキル概要メモを編集するファイル。
- `scripts/build_skill_data.py`: ルーン図鑑からスキルとの対応付けデータを再生成する補助スクリプト。

### 再生成手順

```bash
python scripts/build_skill_data.py
python scripts/rebuild_jobs.py
python scripts/qa_v5.py
```

`build_skill_data.py` は「日本版実装」とマークされているアクセサリールーンだけを対象にしています。後発Season 1/2ルーンを混ぜないためです。日本実機でルーンやスキルの効果が変わった場合は元の `runes/index.html` 埋込データ、`data/skill-notes.json`、`scripts/build_skill_data.py` の照合済み番号・タグを更新してください。

### 出典

- スキル名・役割：GameWith「マビノギモバイル」各職の評価とスキル一覧（2026-10-28参照） https://gamewith.jp/mabinogimobile/577051 ほか。
- ルーン名・固有効果：アリス氏「マビノギモバイル Wiki DB」（CC BY 4.0） https://mabinogimobile.nipponhashi.com/ja/runes/ 。従来v4由来の出典表示も維持しています。
- スキル強化の一般仕様：日本版NEXONゲームガイド https://mabinogimobile.nexon.co.jp/about/guide/3541623
- 氷結術師のタグ： https://mabinogimobile.nipponhashi.com/ja/guides/frostmage-gem-tags/
- ヒーラーのスキル番号： https://mabinogimobile.nipponhashi.com/ja/guides/healer-s0-build/

---

# エリン調査ノート — マビノギモバイル攻略ポータル v3

GitHub Pages で動作する静的サイト。日本版 Season 0 を主対象にした独立攻略ノートです。

## フォルダ構成

```text
index.html                 TOP
jobs/index.html            全18職・職業一覧
jobs/*.html                各職のスキル特化／宝石タグ／ペット／ルーン採用率
runes/index.html           530件の日本語ルーン図鑑
  └─ ?q=氷剣              特定ルーンの検索結果へ（クエリつき）
tools/damagecalc.html      ダメージ計算（SNOMET参考の非公式モデル）
assets/site.css            共通レスポンシブデザイン
assets/site.js             共通ナビゲーション
assets/jobs.js             職業の検索と系統フィルター
assets/rune.js             図鑑の検索、フィルター、48件ずつ表示
data/job-builds.json       台湾版のルーン採用率・採用候補（2026-11-01取得）
data/job-guides.json       各職の特化・タグ・ペット候補（出典を区別した編集データ）
scripts/rebuild_jobs.py    上記2JSONを使い、18職+一覧の19HTMLを再生成
_page-template.html        新規の記事用HTML雛形
```

`rune.html` と `damagecalc.html` は削除して `runes/index.html` と `tools/damagecalc.html` に移動しました。**以前のリンクは切れます**。すでにユーザーからURL互換を維持しなくてよい旨の指示があるため、旧ファイルのリダイレクトも置いていません。

## 公開・置き換え

1. ZIPをローカルで展開。
2. `torahamu/mabimoba` の **mainブランチのルート** にこのサイトのファイル・フォルダを配置。
3. **旧 `rune.html` と旧 `damagecalc.html` をリポジトリから削除**（移動済みのため）。既存の `tools/` 内で競合する別ファイルがある場合は消さないよう注意。
4. GitHub Pages を `Deploy from a branch` → `main` → `/(root)` で設定。

公開URL：
- ホーム `https://torahamu.github.io/mabimoba/`
- 全職 `https://torahamu.github.io/mabimoba/jobs/`
- ルーン図鑑 `https://torahamu.github.io/mabimoba/runes/`
- 計算機 `https://torahamu.github.io/mabimoba/tools/damagecalc.html`

GitHub ActionsのPagesデプロイ成功後に動作確認してください。ポータルは外部APIなしでも動きます（外部出典リンクは閲覧時にネット接続が必要）。

## 各職の編集

- `data/job-builds.json` の `jobs` に採用率とルーン名、推奨セットの補足 `note` を管理。
- `data/job-guides.json` の `jobs.<slug>` に `specialization`（基本3枠、固定枠、代替案）、`gems`（タグ候補と注記）、`pets`（個体候補と能力・注意）を管理。
- 修正したら `python scripts/rebuild_jobs.py` を実行。`beautifulsoup4` が必要です (`pip install beautifulsoup4`)。
- 職業個別ページの生成部分は `scripts/rebuild_jobs.py`。ルーン図鑑は別体の静的JSON埋め込みページです。
- CSSとナビは `assets/` に集約。新規の `guides/` などを追加する場合、`assets/site.js` のリンク配列を編集してください。

## 出典と確度

### ルーン名・効果

マビノギモバイル Wiki DB（アリス氏）、CC BY 4.0。
https://mabinogimobile.nipponhashi.com/ja/runes/
https://creativecommons.org/licenses/by/4.0/

530件のスナップショットです。日本語名、効果、状態、レアリティ等を保持しましたが、元データは自動更新しません。

### ルーン採用率

台湾愛爾琳網 https://erinn.tw/runes （2026-11-01時点のスナップショット）。
**日本版の採用率ではありません**。台湾ランキングの母数・対象期間や装備率の集計条件は出典側で確認してください。アクセサリー・防具は複数枠なので合計が100%にならず、「+」版の採用率と日本語図鑑の基本効果には差があります。

### 特化・宝石・ペット

- [18職クイックスタート・スキル特化・宝石タグ](https://mabinogimobile.nipponhashi.com/ja/guides/jp-launch-class-quickstart/)（2026-10-23更新、韓国S0期を参照した日本向け攻略記事）
- [Nexon Peak：同行ペットガイド](https://peak.nexon.com/ja/post/2760)（投稿者による攻略記事。公式発表の強さ順位ではありません）
- マビノギモバイル調査のユーザー実機・先行版調査メモ

職ごとの推薦は情報を組み合わせた**編集判断**です。日本S0の全職同条件DPS検証に基づく確定最適ビルドではありません。**ペットの採用率は取得していません**。白い子フクロウなど先行版の候補は日本での入手・効果を確認してください。日本版実機確認と地域差・Season 1/2の仕様は必ず区別してください。

## HTMLページの構成

職業ページは、概要 → ページ内ナビ → ルーン候補 → スキル特化 → 宝石タグ → ペット → **台湾ルーン採用率** → 出典、の順番。スマホの小さな画面でも用途別に確認できるようにしています。


## v4（2026-11-01）新機能
- `jobs/*.html` 全18職に「戦い方・オート併用」を追加。データは `data/combat-guides.json`。**実戦の候補であり確定DPS最適解ではない**。
- `content/index.html` 入口、`content/schedule.html` 日本実績／台湾+77日予想、`content/rune-sources.html` ドロップ・交換、`content/season1.html` 韓国S1の実装履歴。
- `tools/weeklyplanner.html` 任意の所持数・週獲得数から必要週数を試算。アビスの1,200消費→900購入にも対応。
- ソースデータ：`data/content.json`、`data/combat-guides.json`。ソースを変更した際は `python scripts/rebuild_jobs.py` で職業ページを再生成。コンテンツページは `scripts/build_content.py` で再生成できる構成へ今後整理（現版はHTML＋JSONのスナップショット）。
- `runes/index.html` と `tools/damagecalc.html` はv3から継続。日本語表記のみを表示。
- **注意**：韓国2025/11/13のタバルタス「専用証16/週→選択箱120証」は公式確認。日本版S1の開始日・報酬は未発表。台湾+77日の解放予測は公式予定ではない。
- HTMLデータの出典リンクは各ページ末尾／項目ごと。台湾の「使用率」は引き続き台湾の外部集計で、日本版使用率ではありません。


### v8.1 育成コスト計算のUI改善（2026-11-06）

- クラス共通のEXP/痕跡テーブルなのでクラス選択を削除。
- 初期値を現在Lv1、目標Lv65に変更。計算結果から職業名も削除。
- 既存のLv1〜65データおよびほかのページは変更なし。
