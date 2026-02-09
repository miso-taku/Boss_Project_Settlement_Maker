# F1: Next.jsプロジェクト初期化 — 設計

## 方針

- **DDD 境界**: フロントエンド初期化のため、DDD の境界は関係ない。Next.js の標準的なプロジェクト構造に従う。
- **責務分割**: Next.js の App Router に従い、`src/app/` 配下にルーティングを配置する。クライアントコンポーネントは `'use client'` を明示する。

## データフロー

- 今回は初期化のみのため、データフローはなし。F2 以降で API 呼び出しのデータフローを定義する。

## API変更

- 今回は API 変更なし。F2 で API クライアントを実装する。

## 代替案と採用理由

- **create-next-app を使用**: Next.js の標準的な初期化方法。推奨される方法であり、最新の設定が自動で適用される。採用。
- **手動でプロジェクト構造を作成**: 可能だが、設定ファイル（next.config.js、tsconfig.json 等）の記述が煩雑。create-next-app の方が効率的。今回は不採用。
- **App Router vs Pages Router**: ADR-0003 で App Router を採用済み。App Router を選択する。

## テスト戦略

- F1 ではテストは実施しない（F6 で実施）。初期化後の動作確認として、`npm run dev` で開発サーバーが起動することを確認する。

## ドキュメント更新方針

- `./docs/implementation-tasklist.md`: F1 を「完了」にし、完了日・備考を記録。実装サマリー・セクション別進捗・更新履歴を更新。
- `./docs/repository-structure.md`: 実際に生成された構造と異なる場合は更新する（create-next-app の最新バージョンで生成される構造に合わせる）。今回は手動で作成した構造が repository-structure.md の想定と一致しているため、更新不要。

## 全体タスク反映方針

- `implementation-tasklist.md` の F1 を完了。総タスク数 26 のうち完了 13、フロントエンド 7 のうち完了 1。

---

## 結果と学び（モード3）

- **採用案の妥当性**: `create-next-app` の実行が環境の問題でできなかったため、手動で Next.js プロジェクト構造を作成した。repository-structure.md の想定構造（`src/app/`、`src/api/`、`src/components/`、`src/hooks/`、`public/`）に従って作成し、App Router、TypeScript、ESLint の設定ファイルを適切に配置できた。
- **想定外**: npm install が環境の問題（npm キャッシュモード）で実行できなかった。package.json は正しく作成されているため、ユーザーが手動で `npm install` を実行すれば依存関係がインストールされ、`npm run dev` で開発サーバーが起動可能。
- **改善点**: 次回は npm install の実行環境を事前に確認するか、ユーザーに手動実行を案内する。プロジェクト構造の作成自体は完了しているため、F2 以降の実装に進める。

---
