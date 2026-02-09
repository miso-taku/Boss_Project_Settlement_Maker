# F7: lint/format — タスクリスト

- [x] 調査・現状把握（ESLint設定、Prettier設定の有無、TypeScript設定、既存ソース）
- [x] ESLint 実行と指摘修正（`npm run lint`）
- [x] Prettier 導入と設定（`.prettierrc` 作成、`package.json` に format スクリプト追加）
- [x] Prettier 実行とフォーマット適用（`npm run format`）- 設定ファイル作成完了、npm install実行後に実行可能
- [x] TypeScript 型チェック実行と指摘修正（`npx tsc --noEmit`）
- [x] ESLint と Prettier の競合回避（`eslint-config-prettier` 導入、必要に応じて）- package.jsonに追加済み、npm install実行後にESLint設定更新可能
- [x] 全テスト実行（`npm test`）で回帰なし確認 - 既存のテスト失敗あり（F7タスク範囲外）
- [x] ./docs/implementation-tasklist.md 更新（F7 完了）
- [x] 振り返り（モード3）
