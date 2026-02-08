# ADR-0003: フロントエンドを React から React/Next.js（App Router）へ変更

## メタデータ

| 項目 | 値 |
|------|-----|
| ステータス | Accepted |
| 日付 | 2025-02-07 |
| 決定者 | プロダクトオーナー |
| 関連 | architecture.md、repository-structure.md、AGENTS.md、doc-update-summary-react-to-nextjs.md（本 ADR に統合） |

---

## コンテキスト

フロントエンドを当初の **React** から **React/Next.js** に仕様変更する。Next.js を採用するにあたり、ルーティング方式（App Router と Pages Router）の選択、および永続ドキュメント全体の整合を取るための修正一覧を残す必要がある。

---

## 決定事項

### 1. フロントエンド技術の変更

**決定**: **React から React/Next.js に変更する**

- UI は引き続き React で実装し、フレームワークとして Next.js を採用する。
- 技術スタック表・システム構成図・各ドキュメントの「フロントエンド」表記を「React/Next.js」に統一する。

### 2. ルーティング方式

**決定**: **Next.js の App Router を採用する**

- ルーティングは **App Router** とする（Pages Router は採用しない）。
- ディレクトリ構成は `app/` 配下に `layout.tsx`、`page.tsx` 等を置く形式とする。
- クライアント専用の機能は `'use client'` を明示する。

### 3. ADR の管理場所

**決定**: **ADR は `docs/adr/` で管理する**

- `docs/` 直下に `adr/` フォルダを設け、既存の ADR（0001, 0002）を `docs/adr/` に移動する。
- 新規 ADR も `docs/adr/` に配置する。本 ADR（0003）はその一覧の一部とする。

---

## 結果・影響

- **技術**: フロントエンドは React/Next.js（App Router）。create-next-app で初期化し、App Router を選択する。
- **ドキュメント**: 本 ADR の「付録: ドキュメント修正一覧」に従い、永続ドキュメント・AGENTS.md・README を更新する。
- **リポジトリ構造**: `docs/adr/` を新設し、`adr-*.md` は `docs/adr/*.md` に集約する。他ドキュメント内の ADR 参照は `adr/adr-0001-...` 等に更新する。

---

## 付録: ドキュメント修正一覧

フロントエンドを React/Next.js（App Router）に変更する際に更新が必要なドキュメントと修正内容。実施時は本一覧に従って修正する。

### 修正対象ファイル一覧

| ファイル | 修正箇所の概要 |
|----------|----------------|
| docs/architecture.md | 技術スタック表・システム構成図・セクション4全体・開発環境（**App Router 採用**を明記） |
| docs/product-requirements.md | スコープ（技術）・影響範囲 |
| docs/repository-structure.md | ルート直下コメント・frontend セクション・**App Router のディレクトリ例**・docs に adr/ を追加 |
| docs/implementation-tasklist.md | セクション3見出し・F1（**create-next-app、App Router 選択**） |
| docs/development-guidelines.md | セクション6見出し・規約（**App Router・`'use client'`**） |
| docs/glossary.md | FE の定義 |
| docs/adr/adr-0001-*.md | 決定事項への追記（ADR-0003 参照） |
| AGENTS.md | 冒頭・セクション2・4・7・8・12 |
| README.md | 技術スタック表・フロントエンド起動方法 |

### 1. docs/architecture.md

- **技術スタック表**: フロントエンドを「React/Next.js」とし、備考に「App Router 採用」を記載。
- **システム構成**: `[React (FE)]` → `[Next.js (FE)]`。
- **セクション4見出し**: 「フロントエンド（React/Next.js）アーキテクチャ」。本文で App Router 採用・SSR/CSR 役割・環境変数（`NEXT_PUBLIC_*`）を記載。
- **開発・実行環境**: Next.js の `npm run dev`（`next dev`）、`npm run build`（`next build`）に言及。

### 2. docs/product-requirements.md

- **スコープ**: フロントエンドを「React/Next.js」に変更。
- **影響範囲**: FE を「Next.js（React）UI（…）」に変更。

### 3. docs/repository-structure.md

- **ルート直下**: frontend のコメントを「フロントエンド（Next.js）」に。
- **docs/ 構成**: `adr/` フォルダを追加し、`adr/adr-*.md` を記載。
- **セクション4**: 見出しを「frontend/（Next.js）」に。ディレクトリ例は **App Router** に統一。

  ```
  frontend/
  ├── package.json
  ├── (pnpm-lock.yaml | package-lock.json | yarn.lock)
  ├── next.config.js  # または next.config.mjs / next.config.ts
  ├── src/
  │   ├── app/                    # App Router
  │   │   ├── layout.tsx
  │   │   ├── page.tsx
  │   │   └── ...
  │   ├── api/                    # API クライアント集約
  │   ├── components/
  │   ├── hooks/
  │   └── ...
  ├── public/
  └── ...
  ```

### 4. docs/implementation-tasklist.md

- **セクション3見出し**: 「フロントエンド（React/Next.js）」。
- **F1**: 「プロジェクト初期化（create-next-app 等、**App Router を選択**）」。

### 5. docs/development-guidelines.md

- **セクション6見出し**: 「フロントエンド（React/Next.js）規約」。
- **規約**: App Router に合わせてコンポーネント配置・データ取得方針を揃える。クライアント専用は `'use client'` を明示。API は FastAPI に直接叩く（Next.js API Routes は使わない方針を記載可）。

### 6. docs/glossary.md

- **FE**: 「本プロダクトでは React/Next.js」に変更。

### 7. docs/adr/adr-0001-*.md

- スコープ・成果物の決定に「2025-02-07 付でフロントエンドを React/Next.js（App Router）に変更。詳細は ADR-0003 参照」を追記（当時の決定はそのまま残す）。

### 8. AGENTS.md

- 冒頭: 「フロントエンドは React/Next.js」に変更。
- セクション2見出し: 「Next.js + FastAPI」。2.1 で UI 変更に「ルーティング（必要に応じて）」を追加。
- セクション4見出し: 「フロントエンド（React/Next.js）」。
- セクション7: Next.js の `next dev` / `next build` / `next start` に一言追記可。
- 8.2: 「Frontend（Next.js）」。
- セクション12・タスクリストテンプレ: 「フロント実装（Next.js）」「Next.js（React）でUI実装」。

### 9. README.md

- **技術スタック表**: フロントエンドを「React/Next.js」に。
- **フロントエンド**: 見出しを「フロントエンド（Next.js）」にし、`npm run dev` で Next.js 開発サーバ（`next dev`）が起動する旨を記載。

### 追加で検討するとよい記述

- **architecture.md**: 単一画面のため SPA 的利用でよいか／将来的な SSR/SSG の有無。API ベースURL は `NEXT_PUBLIC_*` で渡す旨。
- **development-guidelines.md**: `'use client'` の範囲、Next.js API Routes は使わず FastAPI に直接叩く方針。

### 修正不要または任意

- **docs/functional-design.md**: 「FE」表記のみのためそのままで可。
- **docs/adr/adr-0002-*.md**: API 契約の記述のみのため修正は任意。
- **idea.md**: 技術スタックに「React」とあれば「React/Next.js」にすると一貫する。

---

## 参照

- [architecture.md](../architecture.md) — 技術仕様・フロントエンド節
- [repository-structure.md](../repository-structure.md) — リポジトリ・docs/adr 構成
- [doc-update-summary-react-to-nextjs.md](../doc-update-summary-react-to-nextjs.md) — 本 ADR への誘導（簡易版）
- [ADR-0001](adr-0001-上司案件落とし所AIエージェント要件決定.md) — 要件決定（FE 技術の変更は ADR-0003 で追記）
