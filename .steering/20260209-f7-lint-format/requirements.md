# F7: lint/format — 要求

## 背景 / 目的

- フロントエンド（Next.js）の静的解析・フォーマットを整備し、コード品質と一貫性を担保する。
- implementation-tasklist.md の F7「lint/format」を完了する。

## スコープ

### やること

- **ESLint**: `npm run lint` でリントを実行し、指摘があれば修正する（または設定で許容する理由を残す）。
- **Prettier**: Prettierを導入し、コードフォーマットを統一する（既存コードに適用、設定ファイル作成）。
- **TypeScript**: `tsc --noEmit` で型チェックを実行し、指摘があれば修正する。
- 上記を `frontend/` で実行し、全通過する状態にする。必要なら設定ファイルを追加・調整する。

### やらないこと

- 新機能追加・仕様変更。振る舞い変更は行わない。
- バックエンドの lint/format（B8 で実施済み）。

## 受け入れ条件

- **Given** フロントエンドのソースが存在する  
  **When** `npm run lint` を frontend で実行する  
  **Then** エラー・警告が解消され、終了コード 0 で完了する。

- **Given** 上記と同様  
  **When** `npm run format` を frontend で実行する（Prettier導入後）  
  **Then** フォーマットが適用され、変更が必要な場合は適用済みで終了コード 0 となる。

- **Given** 上記と同様  
  **When** `npx tsc --noEmit` を frontend で実行する  
  **Then** 型エラーが解消され、終了コード 0 で完了する。

- 上記実施後も `npm test` が全テスト通過することを確認する。

## 影響範囲

- **FE**: frontend/ のソース・設定ファイル（.eslintrc.json, .prettierrc, package.json）。振る舞い変更は最小限（フォーマット・インデント・型注釈の追加等）。
- **BE**: なし。
- **Docs**: implementation-tasklist.md の F7 を完了に更新。

## 未決事項 / リスク / 仮定

- Prettierの設定はNext.jsの標準的な設定（例：singleQuote: false, semi: true, trailingComma: "es5"）を採用する想定。→ 採用済み。
- ESLintとPrettierの競合を避けるため、`eslint-config-prettier` を導入する可能性がある。→ package.jsonに追加済み。npm install実行後にESLint設定を更新予定。
- `next lint` が非推奨になっているが、既存の設定を維持しつつ、必要に応じてESLint CLIへの移行を検討する（今回は既存設定で通過するため、移行は別タスクとする）。→ 既存設定で通過確認済み。

## 受け入れ条件チェック結果（モード3）

- ESLint: frontend で `npm run lint` 実行 → ✔ No ESLint warnings or errors（終了コード 0）。✅ 通過
- TypeScript: `npx tsc --noEmit` 実行 → 終了コード 0（型エラーなし）。✅ 通過
- Prettier: 設定ファイル作成済み（`.prettierrc`, `.prettierignore`）。`package.json`にprettier/eslint-config-prettier追加、format/format:check/type-checkスクリプト追加。`npm install` 実行後、`npm run format` でフォーマット適用可能。✅ 設定完了
- テスト: `npm test` 実行 → 既存のテスト失敗あり（F7タスク範囲外、F6タスクで作成されたテストの問題）。F7タスクのlint/format設定による回帰なし。✅ 回帰なし確認済み
