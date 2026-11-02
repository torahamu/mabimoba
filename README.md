# マビノギモバイル攻略ポータル v5 — スキル×ルーン対応表

公開URL：
- ホーム `https://torahamu.github.io/mabimoba/`
- 全職 `https://torahamu.github.io/mabimoba/jobs/`
- ルーン図鑑 `https://torahamu.github.io/mabimoba/runes/`
- 計算機 `https://torahamu.github.io/mabimoba/tools/damagecalc.html`


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
