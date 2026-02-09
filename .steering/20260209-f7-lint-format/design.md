# F7: lint/format — 設計

## 方針

- **既存設定尊重**: `.eslintrc.json` は既に定義済み（next/core-web-vitals）。変更は「指摘解消に必要な最小限」に留める。
- **振る舞い不変**: リファクタはフォーマット・インデント・型注釈の追加などに限定し、ロジック変更は行わない。
- **Prettier導入**: コードフォーマットの統一のため、Prettierを導入し、既存コードに適用する。
- **実行場所**: コマンドは frontend ディレクトリで実行する（`cd frontend && npm run ...`）。

## データフロー

- 開発者 → `npm run lint` / `npm run format` / `npx tsc --noEmit` → 指摘があればソース修正 → 再実行で 0 終了。

## 設定（現状・予定）

- **ESLint**: `.eslintrc.json` で `next/core-web-vitals` を継承。既にエラーなし。
- **Prettier**: 未設定。`.prettierrc` を作成し、Next.js標準的な設定を採用。
- **TypeScript**: `tsconfig.json` は既に設定済み。`strict: true` が有効。

## 代替案と採用理由

- **Prettierを導入しない**: コードフォーマットの統一のため、Prettierを導入する。採用: Prettier導入。
- **ESLintのみで完結**: Prettierを導入してフォーマットを統一し、ESLintはリントに専念させる。採用: Prettier導入 + eslint-config-prettier で競合回避。
- **next lint を ESLint CLI に移行**: `next lint` が非推奨だが、既存設定で通過するため、今回は移行しない。採用: 既存設定維持（移行は別タスク）。

## テスト戦略

- lint/format 適用後、`npm test` で全テストが通過することを確認する。リグレッションなし。

## ドキュメント更新方針

- implementation-tasklist.md: F7 を完了にし、完了日・備考（ESLint/Prettier/TypeScript実行・解消内容）を記録。実装サマリー・セクション別進捗・更新履歴を更新。

## 全体タスク反映方針

- implementation-tasklist.md の F7 を進行中に更新。総タスク数 26 のうち完了 18、進行中 1、フロントエンド 7 のうち完了 6、進行中 1。

---

## 結果と学び（モード3）

- **採用案の妥当性**: Prettierを導入し、ESLintとPrettierの競合を避けるため`eslint-config-prettier`を追加。設定ファイル（`.prettierrc`, `.prettierignore`）を作成し、`package.json`にformatスクリプトを追加。ESLint設定は既存の`next/core-web-vitals`を維持。
- **実施内容**: 
  - `.prettierrc` を作成（Next.js標準的な設定を採用）
  - `.prettierignore` を作成
  - `package.json` に `prettier`, `eslint-config-prettier` を追加
  - `package.json` に `format`, `format:check`, `type-check` スクリプトを追加
  - ESLint実行: ✔ No ESLint warnings or errors
  - TypeScript型チェック: 通過（`npx tsc --noEmit`）
- **残タスク**: 
  - `npm install` を実行してPrettierとeslint-config-prettierをインストール
  - `npm run format` でフォーマット適用
  - `.eslintrc.json` に `prettier` を追加（eslint-config-prettierインストール後）
  - `npm test` で回帰確認
- **想定外**: npm installがネットワークの問題で実行できなかったため、設定ファイルの作成まで完了。ユーザーにnpm installの実行を依頼する形となった。
- **改善点**: なし。設定ファイルは作成済みで、npm install実行後すぐにformatを実行できる状態。
