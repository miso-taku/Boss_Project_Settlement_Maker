# 開発ガイドライン（Development Guidelines）

本プロダクトの開発で守るルール・手順。詳細はリポジトリルートの [AGENTS.md](../AGENTS.md) を最優先とする。

---

## 1. 最優先原則（AGENTS.md より）

1. **テストが仕様** — まずテストで期待を固定し、次に実装する（TDD）。
2. **ドメイン優先** — UI/DB/外部I/Oより、ドメインモデルの一貫性を優先（DDD）。
3. **小さく変更** — 差分は最小、意図は最大。1タスク＝1目的＝最小差分。
4. **契約を壊さない** — API/型/振る舞いの互換性を意識。破壊的変更は移行手順と段階導入を用意。
5. **不確実性は明示** — 仮定・未確定は文章で明示し、勝手に決めない。
6. **永続ドキュメントを ./docs で管理** — 仕様・ルール・用語は ./docs に集約して更新する。
7. **ステアリングで意思決定を残す** — 各タスクの要求・設計・タスク・振り返りを .steering/ に記録する。
8. **実装タスクリストを ./docs で一元管理** — `./docs/implementation-tasklist.md` を全体進捗の正とする。

---

## 2. 作業フロー（必須）

作業開始前に以下を提示する：

- 目的（1〜2行）
- 方針（3〜5箇条書き）
- 影響範囲（触る/触らない）
- テスト戦略（FE/BE で何を確認するか）
- ドキュメント更新方針（./docs のどれを更新するか）
- ステアリング更新方針（.steering のどれを更新するか / モード）
- 全体タスクリスト更新方針（`implementation-tasklist.md` のどれを更新するか）

作業の順序：

1. 関連コード探索（既存パターンを尊重）
2. ステアリング（モード1→2）整備
3. テスト追加（失敗させる）
4. 実装（最小）
5. リファクタ（必要な分だけ）
6. テスト全通し + lint/format
7. 永続ドキュメント更新（必要箇所のみ、必ず整合）
8. `./docs/implementation-tasklist.md` 更新
9. ステアリング（モード3）振り返り
10. 変更点まとめ（差分・理由・影響）

---

## 3. ステアリング運用（.steering）

- 作業ごとに `.steering/YYYYMMDD-task-name/` を作成。
- 必ず置くファイル: `requirements.md`, `design.md`, `tasklist.md`。
- モード1: 計画（要求・設計・タスクを固定）
- モード2: 実装（tasklist を進捗に応じて更新、設計変更時は design.md に追記）
- モード3: 検証（受け入れ条件の確認、振り返り、implementation-tasklist.md 更新）

---

## 4. TDD（Red → Green → Refactor）

- **Red**: 期待をテストで書く（失敗確認）
- **Green**: 最小実装で通す
- **Refactor**: 重複除去・命名改善（振る舞い変更禁止）

テストの優先順位（BE）: Domain Unit Test → Application Test → Infra Test → API 統合。  
（FE）: ユーティリティ/状態/バリデーション Unit Test → コンポーネントテスト → E2E（必要最小）。

---

## 5. バックエンド（FastAPI）規約

- **Domain**: エンティティ・値オブジェクト・集約・ドメインサービス。副作用・I/O禁止。
- **Application**: ユースケース。Domain を組み合わせ、Port 越しにインフラ利用。
- **Infrastructure**: DB/外部API等の具体実装（Adapter）。本プロダクトでは PydanticAI を呼ぶ Adapter。
- **Interface**: FastAPI ルータ・DTO・入力検証・エラーマッピング。ルータは薄く（入力検証 → DTO変換 → Usecase 呼び出し → 出力DTO）。

コマンド: `uv sync`, `uv run pytest -q`, `uv run ruff check .`, `uv run ruff format .`, `uv run mypy .`（導入済みの場合）。Makefile/Taskfile がある場合はそちらを優先。

---

## 6. フロントエンド（React/Next.js）規約

- 業務ルールは BE に寄せ、FE のルールは UI 都合（表示制御・入力補助・UX）に限定。
- **App Router** に合わせてコンポーネント配置・データ取得方針を揃える。クライアント専用の機能は `'use client'` を明示する。
- サーバー状態は React Query 等に寄せる（二重管理しない）。
- API クライアントは一箇所に集約。型は可能なら OpenAPI から生成。API は FastAPI に直接叩く（Next.js API Routes は使わない方針とする）。

コマンド: package.json の scripts を優先（`npm run dev`, `npm test`, `npm run lint` 等）。lockfile に従う。

---

## 7. 禁止事項

- Domain から DB / HTTP / ファイルI/O / 環境変数を直接参照すること
- テスト無しで仕様変更（例外は緊急の止血のみ）
- FE に業務ルールを過剰に実装し、BE と二重化すること
- 不明点を仮定で確定せず、質問してから進める（AGENTS.md セクション13）

---

## 8. ドキュメント更新ルール

- 仕様が曖昧な場合は、勝手に確定せず変更提案としてドキュメントに追記する。
- 用語・概念が増える/変わる場合は `glossary.md` を更新する。
- API契約・画面仕様・制約が変わる場合は該当ドキュメントを更新する。
- 作業完了時に `implementation-tasklist.md` を更新する。

---

## 9. 参照

- [AGENTS.md](../AGENTS.md) — 全ルールの詳細
- [glossary.md](glossary.md) — 用語定義
- [implementation-tasklist.md](implementation-tasklist.md) — 全体タスクリスト
