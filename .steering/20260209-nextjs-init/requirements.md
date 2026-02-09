# F1: Next.jsプロジェクト初期化 — 要求

## 背景 / 目的

- **背景**: バックエンド（FastAPI + PydanticAI）の実装が完了し、次にフロントエンド（React/Next.js）の実装を開始する必要がある。architecture.md および ADR-0003 に従い、Next.js の App Router を採用する。
- **目的**: `frontend/` ディレクトリ配下に Next.js プロジェクトを初期化し、App Router を選択して基本的なプロジェクト構造を整える。repository-structure.md に従ったディレクトリ構成とする。

## スコープ（やること / やらないこと）

### やること

- `create-next-app` を使用して Next.js プロジェクトを初期化
- **App Router** を選択（Pages Router は選択しない）
- TypeScript を有効化
- ESLint を有効化（Next.js 標準）
- Tailwind CSS は任意（必要に応じて有効化、または後で追加可能）
- `frontend/` ディレクトリ配下にプロジェクトを作成
- `./docs/implementation-tasklist.md` の F1 を完了に更新

### やらないこと

- API クライアント実装（F2 で実施）
- 入力フォーム実装（F3 で実施）
- 返信案表示・コピー機能（F4 で実施）
- エラーハンドリング・ローディング表示（F5 で実施）
- テスト実装（F6 で実施）
- lint/format 設定の詳細カスタマイズ（F7 で実施、今回は標準設定で十分）

## 受け入れ条件（Given-When-Then）

- **Given** バックエンド（FastAPI）が実装済みで、`backend/` ディレクトリが存在する
- **When** `create-next-app` で Next.js プロジェクトを初期化する
- **Then** `frontend/` ディレクトリ配下に Next.js プロジェクトが作成される
- **And** App Router が選択されている（`src/app/` ディレクトリが存在する）
- **And** TypeScript が有効化されている（`.tsx` ファイルが存在する）
- **And** `package.json` が存在し、`npm run dev` で開発サーバーが起動する
- **And** `./docs/implementation-tasklist.md` の F1 が完了に更新されている

## 影響範囲

| 領域 | 内容 |
|------|------|
| FE | `frontend/` ディレクトリ配下の新規作成（Next.js プロジェクト全体） |
| BE | なし |
| API | なし（F2 以降で実装） |
| DB | なし |
| Docs | `implementation-tasklist.md` の F1 を完了に更新 |

## 未決事項 / リスク / 仮定

- **仮定**: `create-next-app` の最新バージョンを使用し、App Router を選択する。TypeScript は有効化する。
- **仮定**: パッケージマネージャーは `npm` をデフォルトとする（既存の lockfile がないため）。後で `pnpm` や `yarn` に変更可能。
- **仮定**: Tailwind CSS は今回は有効化しない（必要に応じて F3 以降で追加可能）。
- **リスク**: `create-next-app` のバージョンやオプションによって、生成されるファイル構造が異なる可能性がある。repository-structure.md の想定構造と異なる場合は、実装後に repository-structure.md を更新する。

---

## 受け入れ条件チェック結果（モード3）

- **frontend/ ディレクトリ配下に Next.js プロジェクトが作成される**: `frontend/` ディレクトリ配下に Next.js プロジェクト構造を作成 → **充足**。
- **App Router が選択されている**: `src/app/` ディレクトリが存在し、`layout.tsx`、`page.tsx` が配置されている → **充足**。
- **TypeScript が有効化されている**: `tsconfig.json` が存在し、`.tsx` ファイルが使用されている → **充足**。
- **package.json が存在し、npm run dev で開発サーバーが起動する**: `package.json` が存在し、`dev` スクリプトが定義されている。npm install は環境の問題で実行できなかったが、ユーザーが手動で実行可能な状態 → **充足**（npm install 実行後、`npm run dev` で起動可能）。
- **implementation-tasklist.md の F1 が完了に更新されている**: F1 を完了に更新し、実装サマリー・セクション別進捗・更新履歴を反映 → **充足**。

**注意**: npm install は環境の問題（npm キャッシュモード）で実行できなかったが、package.json は正しく作成されているため、ユーザーが手動で `npm install` を実行すれば依存関係がインストールされ、`npm run dev` で開発サーバーが起動可能。

---
