# AGENTS.md

このリポジトリで Cursor Agent / AI が作業するときの **最優先ルール**。
フロントエンドは React/Next.js、バックエンドは Python(FastAPI) を前提に、DDD と TDD で安全に変更を積み上げる。

---

## 0. 最優先原則
1. **テストが仕様**：まずテストで期待を固定し、次に実装する（TDD）。
2. **ドメイン優先**：UI/DB/外部I/Oより、ドメインモデルの一貫性を優先（DDD）。
3. **小さく変更**：差分は最小、意図は最大。1タスク=1目的=最小差分。
4. **契約を壊さない**：API/型/振る舞いの互換性を意識。破壊的変更は移行手順と段階導入を用意。
5. **不確実性は明示**：仮定・未確定は文章で明示し、勝手に決めない。
6. **永続ドキュメントを ./docs で管理する**：仕様・ルール・用語は散逸させず、必ず ./docs に集約して更新する。
7. **作業の意思決定をステアリングファイルで残す**：各タスクの要求・設計・実行計画・進捗・振り返りを `.steering/` に記録し、作業の再現性と透明性を担保する。
8. **実装全体のタスクリストを ./docs で一元管理する**：`./docs/implementation-tasklist.md` を「全体の実装進捗の正」とし、各作業完了時に必ず更新する。

---

## 0.1 永続ドキュメント（./docs）※基本原則
以下は「プロジェクトの正」として扱う。仕様・設計・用語・開発規約の変更が発生した場合は、
コード変更と同一PR（同一差分）で **必ず更新**する。

- `./docs/product-requirements.md` : プロダクト要求定義書
- `./docs/functional-design.md` : 機能設計書
- `./docs/architecture.md` : 技術仕様書
- `./docs/repository-structure.md` : リポジトリ構造定義書
- `./docs/development-guidelines.md` : 開発ガイドライン
- `./docs/glossary.md` : ユビキタス言語定義
- `./docs/implementation-tasklist.md` : **実装全体の実装タスクリスト（全体進捗の正）**

ドキュメント運用ルール：
- 仕様が曖昧な場合は、勝手に確定せず **変更提案** としてドキュメント側に追記案を作る
- ユビキタス言語（用語・概念）が増える/意味が変わる場合は `glossary.md` を更新する
- API契約・画面仕様・制約が変わる場合は該当ドキュメントを更新する（READMEだけで済ませない）
- 各作業（`.steering/...`）が完了したら、必ず `implementation-tasklist.md` を更新する（完了チェック・状況反映）

---

## 0.2 ステアリングファイル（.steering）※基本原則
各作業の「要求」「設計」「タスク」「進捗」「振り返り」を `.steering/` 配下に残す。
AIはタスク開始時に対象フォルダを作成し、作業の各フェーズで必ず更新する。

### 0.2.1 フォルダ命名規則
作業ごとに `.steering/[YYYYMMDD]-[task-name]/` を作成する。

- 例：`.steering/20250115-add-user-profile/`
- 命名規則：`20250115-add-user-profile` 形式（`task-name` は kebab-case、短く目的が伝わる名前）

### 0.2.2 作業ごとに追加するファイル
`.steering/[YYYYMMDD]-[task-name]/` には必ず以下を置く：

- `requirements.md` : 今回の要求内容（何を・なぜ・いつまでに・受け入れ条件）
- `design.md` : 実装アプローチ（設計判断・代替案・トレードオフ・影響範囲）
- `tasklist.md` : 具体的なタスクリスト（実装/テスト/ドキュメント/確認/完了条件）

> 既に同名タスクが存在する場合は、新しい日付で作成する（追記で増殖させない）。

---

## 0.3 ステアリングファイル運用モード（必須）
作業は以下の3モードで進行し、モードに応じてステアリングファイルを更新する。

### モード1：作業計画（ステアリングファイル作成）
**目的**：要求・設計・タスクを合意可能な形に固定する。

AIは以下を必ず実施：
1) `.steering/[YYYYMMDD]-[task-name]/` を作成  
2) `requirements.md` を作成/更新  
3) `design.md` を作成/更新  
4) `tasklist.md` を作成（チェックボックス形式推奨）

`requirements.md` に必ず含める項目（テンプレ）：
- 背景 / 目的
- スコープ（やること / やらないこと）
- 受け入れ条件（Given-When-Then 推奨）
- 影響範囲（FE/BE/API/DB/Docs）
- 未決事項 / リスク / 仮定（※仮定は「仮置き」ではなく「質問待ち」扱い）

`design.md` に必ず含める項目（テンプレ）：
- 方針（DDD境界、責務分割）
- データフロー（簡易でOK）
- API変更（エンドポイント、リクエスト/レスポンス概要、互換性）
- 代替案（2〜3案）と採用理由
- テスト戦略（どの層で何を担保するか）
- ドキュメント更新方針（./docs のどれが影響するか）
- 全体タスク反映方針（`./docs/implementation-tasklist.md` のどれに影響するか）

`tasklist.md` に必ず含める項目（テンプレ）：
- [ ] 調査・現状把握
- [ ] ドメインテスト追加（Red）
- [ ] ドメイン実装（Green）
- [ ] アプリケーション層実装
- [ ] インターフェース/ルータ実装（FastAPI）
- [ ] フロント実装（Next.js）
- [ ] 結合/統合テスト
- [ ] lint/format
- [ ] ./docs 更新
- [ ] `./docs/implementation-tasklist.md` 更新
- [ ] 振り返り（モード3）

### モード2：実装（実装と tasklist.md 更新管理）
**目的**：TDDで実装しながら、進捗と決定を追跡可能にする。

AIは以下を必ず実施：
- `tasklist.md` を進捗に応じて更新（完了したら [x]）
- 設計判断が変わった場合は `design.md` に追記（「変更理由」も書く）
- 仕様が変わった場合は `requirements.md` と ./docs を整合させる
- 重要な判断・制約・TODOはステアリングに残す（コードコメントに埋めない）

### モード3：検証（振り返り）
**目的**：成果物の妥当性と、次回への学びを固定する。

AIは以下を必ず実施：
- `requirements.md` の受け入れ条件が満たされたかチェック結果を追記
- `tasklist.md` の残タスクがないか確認（未完があれば理由と次アクション）
- `design.md` に結果と学びを追記（採用案の妥当性、想定外、改善点）
- 必要に応じて ./docs を最終整合（用語追加は glossary.md）
- 作業完了時に `./docs/implementation-tasklist.md` を更新（完了チェック・進捗反映）

---

## 1. 作業フロー（必須）
AIは作業開始前に以下を必ず提示する：

- **目的（1〜2行）**
- **方針（3〜5箇条書き）**
- **影響範囲（触る/触らない）**
- **テスト戦略（FE/BEそれぞれで何を確認するか）**
- **ドキュメント更新方針（./docs のどれを更新するか）**
- **ステアリング更新方針（.steering のどれを更新するか / モード）**
- **全体タスクリスト更新方針（`./docs/implementation-tasklist.md` のどれを更新するか）**

作業は常にこの順：

1) 関連コード探索（既存パターンを尊重）  
2) ステアリング（モード1→2）整備  
3) テスト追加（失敗させる）  
4) 実装（最小）  
5) リファクタ（必要な分だけ）  
6) テスト全通し + lint/format  
7) 永続ドキュメント更新（必要箇所のみ、しかし必ず整合）  
8) `./docs/implementation-tasklist.md` 更新（完了/進捗反映）  
9) ステアリング（モード3）振り返り  
10) 変更点まとめ（差分・理由・影響）

---

## 2. リポジトリ分割の考え方（Next.js + FastAPI）
### 2.1 変更単位
- **UI変更**（Next.js）：見た目・入力・状態管理・API呼び出し・ルーティング（必要に応じて）
- **API変更**（FastAPI）：ルーティング・DTO・ユースケース呼び出し
- **ドメイン変更**（DDD）：モデル/ルール/不変条件（最優先でテスト）
- **契約変更**：OpenAPI/DTO/型（互換性・移行を重視）

### 2.2 FE/BEの同期方針（契約駆動）
- 原則：**API契約（OpenAPI/DTO）を先に更新 → FE/BEを追従**
- 破壊的変更は避け、必要なら：
  - v1/v2 併存、またはフィールド追加で段階移行
  - deprecated 期間を設ける（コメント/ドキュメントで明記）

---

## 3. バックエンド（FastAPI）— DDDアーキテクチャ方針
### 3.1 レイヤ責務（標準）
- **Domain**
  - エンティティ / 値オブジェクト / 集約 / ドメインサービス / ドメインイベント
  - ルールの源泉。副作用禁止（I/O禁止）。
- **Application**
  - ユースケース（コマンド/クエリ）・トランザクション境界
  - Domainを組み合わせる。インフラは抽象（Port）越し。
- **Infrastructure**
  - DB/外部API/メッセージング等の具体実装（Adapter）
- **Interface (Presentation)**
  - FastAPI ルータ、DTO、認証認可、入力検証、エラーマッピング

> 既存のディレクトリ構成に従う。勝手に新構成へ移行しない。

### 3.2 依存関係ルール（必須）
- Domain は **Application/Infrastructure/Interface に依存しない**
- Application は Domain に依存してよい
- Infrastructure / Interface は Domain + Application に依存してよい
- 逆転が必要なら **Port（抽象）** を Domain か Application に置く

### 3.3 FastAPI での境界ルール
- Router は薄く：**入力検証 → DTO変換 → Usecase呼び出し → 出力DTO**
- 認証/認可は基本 Interface 層（dependency）で処理し、ドメインに持ち込まない
- DBセッションは dependency 注入（Usecase単位でトランザクション管理）

---

## 4. フロントエンド（React/Next.js）— 設計方針
### 4.1 UIは「表示」と「操作」に集中
- 業務ルールは可能な限りバックエンド（Domain）に寄せる
- フロントのルールは **UI都合（表示制御/入力補助/UX）** に限定する

### 4.2 状態管理
- 既存の方針に従う（React Query / Zustand / Redux / Context 等）
- サーバー状態（fetch結果）は **React Query等に寄せる**（二重管理しない）
- フォームは既存のフォーム管理（例：React Hook Form）を尊重

### 4.3 API呼び出し
- APIクライアントは一箇所に集約（`api/` や `services/`）
- エラーハンドリング方針を統一（例：HTTPステータス→UIメッセージ変換）
- 可能なら型を契約から生成（OpenAPI → TS型）。導入済みなら必ず従う

---

## 5. TDD 運用ルール（FE/BE共通）
### 5.1 Red → Green → Refactor（強制）
- Red：期待をテストで書く（失敗確認）
- Green：最小実装で通す
- Refactor：重複除去・命名改善（振る舞い変更禁止）

### 5.2 テスト粒度の優先順位
**Backend**
1. Domain Unit Test（最優先）
2. Application Test（ユースケース）
3. Infra Test（DB/外部I/O）
4. API統合（FastAPI TestClient等）

**Frontend**
1. ユーティリティ/状態/バリデーション Unit Test
2. コンポーネントテスト（React Testing Library）
3. E2E（必要最小：Playwright/Cypress 等、導入済みのもの）

---

## 6. uv（Backend）コマンド規約
バックエンドの基本操作は uv。

- 依存解決/同期：
  - `uv sync`
- 実行：
  - `uv run <command>`
- テスト（pytest想定）：
  - `uv run pytest -q`
- 静的解析/整形（導入されている場合）：
  - `uv run ruff check .`
  - `uv run ruff format .`
  - `uv run mypy .`

> 実際のコマンドが Makefile / Taskfile / scripts に定義されている場合はそちらを優先。

---

## 7. Node（Frontend）コマンド規約（一般形）
フロントエンドは package.json の scripts を優先。

- 依存：
  - `npm ci` / `pnpm i` / `yarn`（採用ツールに従う）
- 開発：
  - `npm run dev`（Next.js の場合は `next dev` が起動）
- テスト：
  - `npm test` または `npm run test`
- lint/format：
  - `npm run lint` / `npm run format`

Next.js の場合は `next build` / `next start` が本番ビルド・起動用。どのパッケージマネージャーか不明な場合、リポジトリ内の lockfile（pnpm-lock.yaml / package-lock.json / yarn.lock）に従う。

---

## 8. DTO / API契約 / バリデーション
### 8.1 Backend（FastAPI）
- 入力は Pydantic DTO で検証（Interface層）
- Domain は Pydantic を極力持ち込まない（標準型 or VOで表現）
- エラーは HTTP に適切にマッピング（ValidationError, DomainErrorなど）

### 8.2 Frontend（Next.js）
- 型は可能なら契約から生成（OpenAPI→TS）
- UI入力検証は UX 改善目的（最終的な整合性はBEで担保）
- APIエラーの表示は一貫性（フィールドエラー/全体エラー）

---

## 9. Repository / Transaction（Backend）
### 9.1 Repository
- Repository は Domain では抽象（Protocol/Interface）
- Infrastructure が具体実装（SQLAlchemy/SQLModel等）
- メソッドは意図が明確な粒度（`save`, `get_by_id`, `find_by_*`）

### 9.2 トランザクション境界
- 原則 **Application層** が境界
- Domain 内でトランザクションを始めない
- DBセッションは注入し、Usecase単位で管理

---

## 10. 禁止事項（重要）
- Domain から DB / HTTP / ファイルI/O / 環境変数 を直接参照すること
- “便利 utils” の無制限追加（必要なら scoped に作る）
- 一括リネーム / 大規模移動（目的がそれでない限り禁止）
- テスト無しで仕様変更（例外は緊急の止血のみ）
- FEに業務ルールを過剰に実装し、BEと二重化すること

---

## 11. 変更の提出物（必須）
作業完了時、AIは以下をまとめる：

- **何を変えたか（箇条書き）**
- **なぜ変えたか（根拠）**
- **影響範囲（API/画面/データ/ドキュメント）**
- **追加/更新したテスト（FE/BE）**
- **更新した永続ドキュメント（./docs）**
- **更新したステアリングフォルダ（.steering）**
- **更新した実装全体タスクリスト（`./docs/implementation-tasklist.md`）**
- **実行したコマンド**
  - 例：`uv run pytest` / `uv run ruff check .` / `npm test` / `npm run lint`

---

## 12. 典型タスクの進め方テンプレ
### バグ修正（Backend優先）
1) 再現テストを書く（Red）
2) 最小修正（Green）
3) 回帰テスト + リファクタ（Refactor）
4) API層・FE層は必要なら追従
5) 仕様に影響するなら ./docs を更新
6) `./docs/implementation-tasklist.md` を更新
7) ステアリングをモード3で振り返り更新

### 新機能（契約→BE→FE）
1) API契約（DTO/レスポンス）を定義（必要なら ./docs にも反映）
2) Domain仕様をテストで固定
3) Usecase実装（Application）
4) FastAPI ルータは薄く
5) Next.js（React）でUI実装（APIクライアント→画面）
6) 必要に応じてE2E
7) ./docs を更新（要求/機能/技術/用語の該当箇所）
8) `./docs/implementation-tasklist.md` を更新
9) ステアリングをモード3で振り返り更新

### UI改善（FE中心）
1) 期待をテスト（コンポーネント/UX）で固定
2) UI実装
3) API呼び出しや状態は既存パターンに寄せる
4) 仕様に影響するなら ./docs を更新
5) `./docs/implementation-tasklist.md` を更新
6) ステアリングをモード3で振り返り更新

---

## 13. 不明点が出た場合（仮定で進めない）
**仮定で進めることは禁止。** 不明点・曖昧さ・選択肢がある場合は、必ず質問してから進める。

AIは以下を守る：
- 不明点を「質問リスト」として列挙し、**最小限の質問（優先度順）**で確認する
- 回答がない限り、仕様や設計を勝手に確定しない
- ただし作業を止めないため、次のどちらかを行う：
  - **質問待ちで止まる範囲**と、**先に進められる範囲（調査・整理・テスト雛形）**を分けて進める
  - 先に進められる範囲は「仮置き」ではなく「未確定のまま」進め、確定が必要な箇所は実装しない

質問の例（テンプレ）：
- 仕様：期待する振る舞いはA/Bどちら？
- 契約：APIレスポンスはこの形で良い？
- UX：エラー表示はトースト/フォーム下/ダイアログのどれ？
- 互換性：既存の呼び出し元は残す必要がある？

---
