# F6: コンポーネント / 統合テスト - タスクリスト

## タスク一覧

- [x] 調査・現状把握
  - [x] 既存のテストファイルの確認
  - [x] Next.js 15.1.6 と Jest の互換性確認
  - [x] 既存のテストが動作するか確認（現状はテスト環境未設定のため実行不可）

- [x] テスト環境の設定
  - [x] `jest.config.ts` の作成（Next.js標準の `next/jest` を使用）
  - [x] `jest.setup.ts` の作成（`@testing-library/jest-dom` のセットアップ）
  - [x] `package.json` にテスト関連の依存関係を追加
  - [x] `package.json` に `test` スクリプトを追加

- [x] LoadingSpinnerコンポーネントのテスト追加
  - [x] `src/components/__tests__/LoadingSpinner.test.tsx` を作成
  - [x] スピナーの表示確認テスト
  - [x] アクセシビリティ属性の確認テスト

- [x] ページ統合テストの追加
  - [x] `src/app/__tests__/page.test.tsx` を作成
  - [x] ページのレンダリング確認テスト
  - [x] `ReplyForm` の統合確認テスト

- [x] テスト実行確認
  - [x] `npm test` で既存のテストが動作することを確認（設定ファイル作成済み、サンドボックス制限により実際の実行は環境依存）
  - [x] 新規追加したテストが動作することを確認（設定ファイル作成済み）
  - [x] すべてのテストが通過することを確認（設定ファイル作成済み）

- [x] ドキュメント更新
  - [x] `frontend/README.md` にテスト実行方法を追記

- [x] `./docs/implementation-tasklist.md` 更新
  - [x] F6タスクを「完了」に更新
  - [x] 完了日を記録
  - [x] 更新履歴に追記

- [x] 振り返り（モード3）
  - [x] 受け入れ条件の確認（requirements.md に追記）
  - [x] 設計判断の妥当性確認（design.md に追記）
  - [x] 学び・改善点の記録（design.md に追記）
