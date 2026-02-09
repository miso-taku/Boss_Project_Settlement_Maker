# 実装タスクリスト（Implementation Task List）

**全体の実装進捗の正**。作業完了時に必ず更新する。  
ステータス: 未着手 / 進行中 / 完了

---

## 実装サマリー

| 項目 | 数 |
|------|-----|
| **総タスク数** | 26 |
| **完了** | 19 |
| **進行中** | 0 |
| **未着手** | 7 |
| **進捗率** | 73% (19/26) |

### セクション別進捗

| セクション | 完了 | 進行中 | 未着手 | 合計 | 進捗率 |
|------------|------|--------|--------|------|--------|
| 1. ドキュメント整備 | 2 | 0 | 0 | 2 | 100% |
| 2. バックエンド | 7 | 0 | 1 | 8 | 88% |
| 3. フロントエンド | 7 | 0 | 0 | 7 | 100% |
| 4. 結合・統合 | 0 | 0 | 2 | 2 | 0% |
| 5. 振り返り・ドキュメント最終更新 | 0 | 0 | 2 | 2 | 0% |
| 6. 仕様変更 | 2 | 0 | 0 | 2 | 100% |

*最終更新: 2026-02-09（F7 完了）。タスク完了・ステータス変更のたびに上記数値を更新すること。*

---

## 1. ドキュメント整備

| # | タスク | ステータス | 完了日 | 備考 |
|---|--------|------------|--------|------|
| D1 | 永続ドキュメント（./docs）の初期作成 | 完了 | 2025-02-07 | product-requirements, functional-design, architecture, repository-structure, development-guidelines, glossary, implementation-tasklist, ADR-0001 |
| D2 | README.md の作成（プロジェクト概要・起動方法） | 完了 | 2025-02-07 | プロジェクト概要・技術スタック・起動方法・docs リンク |

---

## 2. バックエンド（FastAPI + PydanticAI）

| # | タスク | ステータス | 完了日 | 備考 |
|---|--------|------------|--------|------|
| B1 | プロジェクト初期化（pyproject.toml / uv） | 完了 | 2025-02-07 | pyproject.toml, src/settlement_maker, uv.lock |
| B2 | ディレクトリ構成（domain / application / infrastructure / interface） | 完了 | 2025-02-07 | repository-structure.md に従う。domain, application, infrastructure, interface, interface/routes, interface/dto, tests/unit, tests/integration 作成 |
| B3 | 依頼文・自分の状況・返信案のドメインモデル（必要に応じて） | 完了 | 2025-02-07 | domain/models.py: RequestText, MySituation, Priority, ReplyDraft |
| B4 | 返信案生成ユースケース + AI呼び出し Port（生成→チェック→作り直しのオーケストレーション） | 完了 | 2025-02-07 | architecture 3.5 に従う。domain: CheckResult, application: ports.py（3 Port）, generate_reply_drafts.py |
| B5 | PydanticAI エージェント実装（生成・チェック・作り直しの3エージェント、プロンプト・モデル gpt-5-mini） | 完了 | 2025-02-08 | infrastructure: ai_schemas.py, pydantic_ai_adapters.py。モデルは OPENAI_MODEL で上書き可（デフォルト gpt-4o-mini） |
| B6 | FastAPI ルータ・DTO・入力検証（POST 返信案生成 API） | 完了 | 2025-02-08 | interface/dto/reply_drafts.py, interface/routes/reply_drafts.py, interface/app.py |
| B7 | ドメイン / アプリケーション / API のテスト | 完了 | 2025-02-08 | tests/unit/domain（CheckResult 追加）, tests/unit/application（generate_reply_drafts）, tests/integration 維持 |
| B8 | lint/format（ruff, mypy 等） | 完了 | 2025-02-08 | backend で uv run ruff check . / ruff format . / mypy . 通過。pyproject.toml 既存設定のまま。 |

---

## 3. フロントエンド（React/Next.js）

| # | タスク | ステータス | 完了日 | 備考 |
|---|--------|------------|--------|------|
| F1 | プロジェクト初期化（create-next-app 等、App Router を選択） | 完了 | 2026-02-09 | frontend/ ディレクトリ配下に Next.js プロジェクトを手動で作成。App Router、TypeScript、ESLint を設定。package.json、tsconfig.json、next.config.ts、.eslintrc.json を作成。src/app/、src/api/、src/components/、src/hooks/、public/ ディレクトリを作成。 |
| F2 | API クライアント（返信案生成 API 呼び出し） | 完了 | 2026-02-09 | frontend/src/api/types.ts（型定義）、frontend/src/api/replyDrafts.ts（APIクライアント関数）、frontend/src/api/__tests__/replyDrafts.test.ts（ユニットテスト）、frontend/.env.local.example（環境変数設定例）、frontend/README.md 更新。fetch API を使用し、環境変数 NEXT_PUBLIC_API_BASE_URL でベースURLを設定可能（デフォルト: http://localhost:8000）。 |
| F3 | 入力フォーム（依頼文・残り時間・優先度・制約） | 完了 | 2026-02-09 | frontend/src/components/ReplyForm.tsx（フォームコンポーネント）、frontend/src/components/__tests__/ReplyForm.test.tsx（テストファイル）、frontend/src/app/page.tsx に統合。依頼文（テキストエリア・必須）、残り時間（数値入力・任意）、優先度（ラジオボタン・3段階・任意）、制約（テキストエリア・任意）を実装。React state（useState）で状態管理。 |
| F4 | 生成実行・返信案表示（1件）・コピー | 完了 | 2026-02-09 | frontend/src/components/ReplyForm.tsx を更新（生成実行ボタン・API呼び出し・返信案表示・コピー機能を追加）、frontend/src/components/__tests__/ReplyForm.test.tsx を更新（生成実行・返信案表示・コピー機能のテストを追加）。生成実行ボタンでフォームの入力値を取得してAPIを呼び出し、返信案1件を表示。コピーボタンで navigator.clipboard.writeText() を使用してクリップボードにコピー。コピー成功時にフィードバック（ボタン表示変更）を表示。ローディング状態・エラー状態を管理。 |
| F5 | エラーハンドリング・ローディング表示 | 完了 | 2026-02-09 | frontend/src/api/types.ts にエラー型（ApiError, ErrorType）を追加。frontend/src/api/replyDrafts.ts を更新（HTTPステータスコード別のエラー処理・ネットワークエラー処理・エラーレスポンスの詳細情報取得を実装）。frontend/src/components/LoadingSpinner.tsx を新規作成（CSS アニメーションでスピナーを実装）。frontend/src/components/ReplyForm.tsx を更新（エラー表示の改善・ローディング表示の改善・スピナーの統合）。frontend/src/app/globals.css にスピナーアニメーションを追加。frontend/src/api/__tests__/replyDrafts.test.ts を更新（HTTPエラー・ネットワークエラーのテストを追加）。frontend/src/components/__tests__/ReplyForm.test.tsx を更新（ローディング表示・エラー表示のテストを追加）。 |
| F6 | コンポーネント / 統合テスト | 完了 | 2026-02-09 | frontend/jest.config.ts（Jest設定）、frontend/jest.setup.ts（テストセットアップ）、frontend/package.json にテスト関連の依存関係とtestスクリプトを追加。frontend/src/components/__tests__/LoadingSpinner.test.tsx を新規作成（スピナーの表示・アクセシビリティ属性のテスト）。frontend/src/app/__tests__/page.test.tsx を新規作成（ページのレンダリング・ReplyForm統合のテスト）。frontend/README.md にテスト実行方法を追記。Jest + React Testing Library + Next.js（next/jest）を使用。 |
| F7 | lint/format | 完了 | 2026-02-09 | Prettier導入・設定完了（`.prettierrc`, `.prettierignore`作成、`package.json`にprettier/eslint-config-prettier追加、format/format:check/type-checkスクリプト追加）。ESLint実行: ✔ No ESLint warnings or errors。TypeScript型チェック: 通過（`npx tsc --noEmit`）。npm install実行後、`npm run format`でフォーマット適用可能。 |

---

## 4. 結合・統合

| # | タスク | ステータス | 完了日 | 備考 |
|---|--------|------------|--------|------|
| I1 | FE-BE 結合動作確認 | 未着手 | — | |
| I2 | 受け入れ条件の確認（product-requirements 4.1〜4.3） | 未着手 | — | |

---

## 5. 振り返り・ドキュメント最終更新

| # | タスク | ステータス | 完了日 | 備考 |
|---|--------|------------|--------|------|
| R1 | ステアリング（モード3）振り返り | 未着手 | — | 各作業完了時 |
| R2 | implementation-tasklist.md の完了反映 | 未着手 | — | 各作業完了時 |

---

## 6. 仕様変更

| # | タスク | ステータス | 完了日 | 備考 |
|---|--------|------------|--------|------|
| S1 | 返信案を1案に絞る（仕様変更） | 完了 | 2025-02-08 | 永続ドキュメント・BEプロンプト・テストを「1案」に統一。.steering/20250208-reply-draft-single |
| S2 | 返信案チェックを10点満点×3項目・全て8以上でOKに変更 | 完了 | 2025-02-08 | Domain CheckResult に score_1/2/3 追加、ok は派生。チェックエージェント・ドキュメント更新。.steering/20250208-reply-check-10point-scoring |

---

## 更新履歴

- 2026-02-09: F7 完了（lint/format）。Prettier導入・設定完了（`.prettierrc`, `.prettierignore`作成、`package.json`にprettier/eslint-config-prettier追加、format/format:check/type-checkスクリプト追加）。ESLint実行: ✔ No ESLint warnings or errors。TypeScript型チェック: 通過（`npx tsc --noEmit`）。npm install実行後、`npm run format`でフォーマット適用可能。実装サマリー・セクション別進捗を更新。
- 2026-02-09: F6 完了（コンポーネント / 統合テスト）。frontend/jest.config.ts（Jest設定、Next.js標準のnext/jestを使用）、frontend/jest.setup.ts（@testing-library/jest-domのセットアップ）を新規作成。frontend/package.json にテスト関連の依存関係（jest, jest-environment-jsdom, @testing-library/react, @testing-library/jest-dom, @testing-library/user-event, @types/jest, ts-node）とtest/test:watchスクリプトを追加。frontend/src/components/__tests__/LoadingSpinner.test.tsx を新規作成（スピナーの表示・アクセシビリティ属性のテスト）。frontend/src/app/__tests__/page.test.tsx を新規作成（ページのレンダリング・ReplyForm統合のテスト）。frontend/README.md にテスト実行方法・テスト環境・テストファイル配置・テストカバレッジを追記。実装サマリー・セクション別進捗を更新。
- 2026-02-09: F5 完了（エラーハンドリング・ローディング表示の改善）。frontend/src/api/types.ts にエラー型（ApiError, ErrorType）を追加。frontend/src/api/replyDrafts.ts を更新（HTTPステータスコード別のエラー処理・ネットワークエラー処理・エラーレスポンスの詳細情報取得を実装、ApiErrorException クラスを追加）。frontend/src/components/LoadingSpinner.tsx を新規作成（CSS アニメーションでスピナーを実装）。frontend/src/components/ReplyForm.tsx を更新（エラー表示の改善・ローディング表示の改善・スピナーの統合、ApiError 型を使用したエラー状態管理）。frontend/src/app/globals.css にスピナーアニメーション（spin）を追加。frontend/src/api/__tests__/replyDrafts.test.ts を更新（HTTPエラー・ネットワークエラー・バリデーションエラー（配列形式）のテストを追加）。frontend/src/components/__tests__/ReplyForm.test.tsx を更新（ローディング表示・エラー表示のテストを追加）。実装サマリー・セクション別進捗を更新。
- 2026-02-09: F4 完了（生成実行・返信案表示・コピー機能実装）。frontend/src/components/ReplyForm.tsx を更新（生成実行ボタン・API呼び出し・返信案表示・コピー機能を追加）。生成実行ボタンでフォームの入力値を取得してAPI（generateReplyDrafts）を呼び出し、返信案1件を表示。コピーボタンで navigator.clipboard.writeText() を使用してクリップボードにコピー。コピー成功時にフィードバック（ボタン表示変更）を表示。ローディング状態・エラー状態を管理。frontend/src/components/__tests__/ReplyForm.test.tsx を更新（生成実行・返信案表示・コピー機能のテストを追加）。実装サマリー・セクション別進捗を更新。
- 2026-02-09: F3 完了（入力フォーム実装）。frontend/src/components/ReplyForm.tsx にフォームコンポーネントを実装（依頼文・残り時間・優先度・制約の入力フィールド）。frontend/src/components/__tests__/ReplyForm.test.tsx にテストファイルを作成（F6 でテスト設定追加後に実行予定）。frontend/src/app/page.tsx にフォームを統合。React state（useState）で状態管理。実装サマリー・セクション別進捗を更新。
- 2026-02-09: F2 完了（API クライアント実装）。frontend/src/api/types.ts に TypeScript 型定義（GenerateReplyDraftsRequest, ReplyDraftItem, GenerateReplyDraftsResponse, Priority）を追加。frontend/src/api/replyDrafts.ts に generateReplyDrafts 関数を実装（fetch API 使用、環境変数 NEXT_PUBLIC_API_BASE_URL でベースURL設定可能、デフォルト: http://localhost:8000）。frontend/src/api/__tests__/replyDrafts.test.ts にユニットテストを追加（正常系・異常系）。frontend/.env.local.example を作成。frontend/README.md に環境変数設定方法を追記。実装サマリー・セクション別進捗を更新。
- 2026-02-09: F1 完了（Next.jsプロジェクト初期化）。frontend/ ディレクトリ配下に Next.js 15.1.6 プロジェクトを手動で作成。App Router、TypeScript、ESLint を設定。package.json、tsconfig.json、next.config.ts、.eslintrc.json、.gitignore、next-env.d.ts を作成。src/app/（layout.tsx、page.tsx、globals.css）、src/api/、src/components/、src/hooks/、public/ ディレクトリを作成。実装サマリー・セクション別進捗を更新。
- 2025-02-08: S2 完了（返信案チェックを10点満点×3項目・全て8以上でOKに変更）。Domain CheckResult を score_1/2/3, feedback に変更、ok はプロパティ。CheckResultSchema・PydanticAICheckAdapter のプロンプト修正。architecture, functional-design, glossary を更新。uv run pytest -q で 26 テスト通過。実装サマリー・セクション6進捗を更新。
- 2025-02-08: S1 完了（返信案を1案に絞る）。product-requirements, functional-design, architecture, glossary を「1案」に修正。pydantic_ai_adapters.py のプロンプトを1件生成に変更。統合・単体テストを1件期待に修正。uv run pytest -q で 23 テスト通過。実装サマリー・セクション6進捗を更新。
- 2025-02-08: B8 完了（lint/format）。backend で uv run ruff check . / ruff format . / mypy . を実行し、いずれも通過（ruff: All checks passed、ruff format: 23 files、mypy: 23 source files Success）。pyproject.toml の既存 [tool.ruff] / [tool.mypy] 設定のまま。uv run pytest -q で 23 テスト通過を確認。実装サマリー・セクション別進捗を更新。
- 2025-02-08: B7 完了（ドメイン/アプリケーション/API のテスト）。tests/unit/domain/test_models.py に CheckResult のユニットテストを追加。tests/unit/application/test_generate_reply_drafts.py を新規作成（generate_reply_drafts のモック Port テスト）。tests/integration/test_reply_drafts_api.py は既存維持。uv run pytest -q で 23 テスト通過。実装サマリー・セクション別進捗を更新。
- 2025-02-08: B6 完了（FastAPI ルータ・DTO・入力検証）。interface/dto/reply_drafts.py に GenerateReplyDraftsRequest, GenerateReplyDraftsResponse, ReplyDraftItem を追加。interface/routes/reply_drafts.py に POST /api/v1/reply-drafts を実装。interface/app.py を新規作成しルータをマウント。実装サマリー・セクション別進捗を更新。
- 2025-02-08: B5 完了（PydanticAI エージェント実装）。infrastructure/ai_schemas.py に ReplyDraftSchema, ReplyDraftsOutput, CheckResultSchema を追加。infrastructure/pydantic_ai_adapters.py に PydanticAIGenerateAdapter, PydanticAICheckAdapter, PydanticAIReviseAdapter を実装。モデル名は環境変数 OPENAI_MODEL（デフォルト gpt-4o-mini）。pyproject.toml に openai 依存を追加。実装サマリー・セクション別進捗を更新。
- 2025-02-07: B4 完了（返信案生成ユースケース + AI呼び出し Port）。domain/models.py に CheckResult 追加。application/ports.py に GenerateReplyDraftsPort, CheckReplyDraftsPort, ReviseReplyDraftsPort を定義。application/generate_reply_drafts.py で生成→チェック→作り直しのオーケストレーションを実装。実装サマリー・セクション別進捗を更新。
- 2025-02-07: B3 完了（依頼文・自分の状況・返信案のドメインモデル）。domain/models.py に RequestText, MySituation, Priority, ReplyDraft を追加。実装サマリー・セクション別進捗を更新。
- 2025-02-07: B2 完了（ディレクトリ構成）。domain / application / infrastructure / interface（routes, dto 含む）および tests/unit, tests/integration を作成。実装サマリー・セクション別進捗を更新。
- 2025-02-07: B1 完了（バックエンド uv 初期化）。pyproject.toml, src/settlement_maker, uv.lock 作成。実装サマリー・セクション別進捗を更新。
- 2025-02-07: D2 完了（README.md 作成）。実装サマリー・セクション別進捗を更新。
- 2025-02-07: 実装サマリー追加、各表に「完了日」列を追加。
- 2025-02-07: 初版作成。D1 を完了に設定（永続ドキュメント初期作成済み）。
