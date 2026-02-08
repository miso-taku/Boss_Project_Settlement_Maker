# 仕様変更: 返信案を 1 案に絞る — 設計

## 方針

- **契約は維持**: `POST /api/v1/reply-drafts` のレスポンスは `drafts: list[{ text: string }]` のままとする。要素数が 1 になるだけなので、既存の型・フロント実装（将来）はそのまま使える。
- **変更箇所**: (1) 永続ドキュメントの文言、(2) Infrastructure のプロンプト（生成・作り直しで「1件」に統一）、(3) テストのモックとアサーション（1件を期待）。

## データフロー

- 変更なし。依頼文＋自分の状況 → 生成 Port → 返信案リスト（**1 件**）→ チェック → 必要なら作り直し（**1 件**）→ 返却。

## API 変更

- **なし**。エンドポイント・リクエスト・レスポンスの型は同じ。レスポンスの `drafts` は要素数 1 のリストとなることをドキュメントで明記する。

## 変更内容（箇条書き）

### 永続ドキュメント

- **product-requirements.md**: 「複数の返信案」「2案以上」→「1案」「1件」。受け入れ条件 4.1 の「少なくとも2案以上」→「1案」。
- **functional-design.md**: 出力「複数（A/B/C）」→「1案」。返信案の数「少なくとも2案以上、目安3案」→「1案」。
- **architecture.md**: レスポンス説明で「返信案リスト」はそのまま、「1件」であることを追記。3.5 のフロー説明で「返信案リスト（1件）」と明記可能。
- **glossary.md**: 「返信案」の説明で「複数パターンを一度に表示」→「1案を表示」に変更。
- **implementation-tasklist.md**: 本仕様変更を「仕様変更タスク」として追記し、完了時にチェックする。

### バックエンド

- **pydantic_ai_adapters.py**
  - `PydanticAIGenerateAdapter`: システムプロンプト・ユーザープロンプトの「2〜3件」「複数パターン」→「1件」に変更。
  - `PydanticAIReviseAdapter`: 「件数は元のリストと同じに」→「1件で返す」に変更。
- **tests/integration/test_reply_drafts_api.py**
  - `MockGeneratePort`: 返すリストを 1 件（例: `ReplyDraft(text="返信案です。")`）に変更。
  - `test_post_reply_drafts_returns_200_and_drafts`: `len(data["drafts"]) == 2` → `== 1`、2件分の assert を 1 件に。
  - `test_post_reply_drafts_minimal_body_returns_200`: `len(data["drafts"]) >= 1` のままでも可（1 件返るので満たす）。
- **tests/unit/application/test_generate_reply_drafts.py**
  - `MockGeneratePort` のデフォルトを 1 件（例: `[ReplyDraft(text="初稿")]`）に変更。
  - 各テストの `assert len(result) == 2` を `== 1` に、`result[0].text` / `result[1].text` を 1 件用に修正。
  - `test_generate_reply_drafts_stops_after_max_revise_rounds`: 既に 1 件の結果で検証しているため、`len(result) == 1` はそのまま。モックの `MockGeneratePort` を 1 件に合わせる。
  - `test_generate_reply_drafts_zero_max_revise_rounds_returns_initial_drafts`: `len(result) == 2` → `== 1`、`result[0].text` のみ参照。

## 代替案と採用理由

- **API を `draft: { text }` 単体に変更する**: 破壊的変更になり、将来「複数案」に戻しづらい。リスト 1 件のままが安全。採用しない。
- **プロンプトのみ変更しドキュメントは触らない**: 仕様とドキュメントの整合が取れなくなる。ドキュメントも同時に更新する。採用: ドキュメント更新あり。

## テスト戦略

- 既存の unit / integration テストを「1件返る」前提に修正し、全テスト通過で完了とする。
- 新規テストは不要（振る舞いの変更のみ）。

## ドキュメント更新方針

- 上記のとおり product-requirements, functional-design, architecture, glossary, implementation-tasklist を更新する。
- ADR は今回の「1案に絞る理由」を残すかは任意（ユーザー要望ベースのため、implementation-tasklist の更新履歴で十分と判断）。

## 全体タスク反映方針

- implementation-tasklist.md に「仕様変更: 返信案を 1 案に絞る」を追記し、完了時にチェックを入れる。既存の B1〜B8 などの番号は変えず、新規行で「S1: 返信案 1 案に絞る（仕様変更）」のような形で追加する。

---

## 結果と学び（モード3）

- **採用案の妥当性**: API 契約（drafts は list）を維持したため、型・フロント実装に破壊的変更なし。プロンプトとテストの期待値のみの変更で完了。
- **想定外**: なし。ruff の E501/E402 は pydantic_ai_adapters.py に既存で、本タスクの変更対象外。
- **改善点**: なし。
