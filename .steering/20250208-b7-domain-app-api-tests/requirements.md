# B7: ドメイン / アプリケーション / API のテスト — 要求

## 背景 / 目的

- B3〜B6 でドメインモデル・ユースケース・PydanticAI アダプター・FastAPI ルータを実装済み。
- 本タスクでは **ドメイン・アプリケーション・API** のテストを整備し、仕様をテストで固定する（TDD の「テストが仕様」を満たす）。

## スコープ

### やること

- **Domain Unit Test**: 既存の test_models.py を補完する。不足している CheckResult のテストを追加する。
- **Application Test**: generate_reply_drafts ユースケースのテストを追加する。Port はモックに差し替え、生成→チェック→作り直しのオーケストレーションを検証する。
- **API 統合テスト**: 既存の test_reply_drafts_api.py を維持・必要なら補足する。Port を overrides でモックに差し替え、200/422 の契約を検証する。

### やらないこと

- Infrastructure（PydanticAI アダプター）の単体テスト（外部 API 呼び出しのため、統合テストまたは E2E で検証する想定）。本タスクではモックで API 層を検証する。
- フロントエンドのテスト（F6 で実施）。

## 受け入れ条件

- **Given** ドメインモデル（RequestText, MySituation, Priority, ReplyDraft, CheckResult）の仕様  
  **When** tests/unit/domain/test_models.py を実行する  
  **Then** 全テストがパスし、依頼文空・残り時間負・CheckResult の ok/feedback 等の振る舞いがテストで固定されている。

- **Given** generate_reply_drafts の仕様（生成→チェック OK で即返却、NG で revise を最大 N 回）  
  **When** Application 層のユニットテストを実行する  
  **Then** モック Port を用いてオーケストレーションが期待通りであることが検証される。

- **Given** POST /api/v1/reply-drafts の契約（200: 返信案リスト、422: バリデーションエラー）  
  **When** tests/integration/test_reply_drafts_api.py を実行する  
  **Then** 全テストがパスする。

- `uv run pytest -q` でバックエンドの全テストが通る。

## 影響範囲

- **BE**: tests/unit/domain（CheckResult テスト追加）、tests/unit/application（新規、generate_reply_drafts テスト）、tests/integration（既存維持）。
- **FE**: なし。
- **Docs**: implementation-tasklist.md を B7 完了で更新。

## 未決事項 / リスク / 仮定

- 既存の integration テストは B6 時点で既に実装済みのため、不足しているのは Domain の CheckResult と Application のユースケーステストとする。

## 受け入れ条件チェック結果（モード3）

- ドメインモデル（RequestText, MySituation, Priority, ReplyDraft, CheckResult）のテスト: test_models.py に CheckResult の ok/feedback テストを追加し、全ドメインテストがパス。
- generate_reply_drafts のオーケストレーション: test_generate_reply_drafts.py でモック Port を用い、初回 OK で即返却・NG で revise 呼び出し・max_revise_rounds で打ち切り・max_revise_rounds=0 で check 未呼び出しを検証。全テストパス。
- POST /api/v1/reply-drafts の契約: 既存 test_reply_drafts_api.py が 200/422 を検証済み。変更なしで維持。
- uv run pytest -q: 23 passed。
