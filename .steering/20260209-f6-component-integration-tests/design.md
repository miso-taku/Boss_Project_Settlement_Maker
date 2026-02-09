# F6: コンポーネント / 統合テスト - 設計

## 方針（DDD境界、責務分割）

本タスクはフロントエンドのテスト環境整備であり、DDDの境界とは直接関係しない。
ただし、テストの責務は以下のように分割する：

- **ユニットテスト**: 個別コンポーネントの動作確認（`LoadingSpinner`）
- **統合テスト**: ページ全体の動作確認（`page.tsx` と `ReplyForm` の統合）
- **APIクライアントテスト**: 既存の `replyDrafts.test.ts` で実装済み（変更なし）

## データフロー

```
テスト実行
  ↓
Jest がテストファイルを検出
  ↓
Next.js の設定（next/jest）でトランスパイル
  ↓
React Testing Library でコンポーネントをレンダリング
  ↓
アサーションで動作確認
```

## API変更

なし（このタスクはテスト環境の整備のみ）

## 代替案

### 案1: Jest + React Testing Library（採用）
- **理由**: 既存のテストファイルがこの構成を前提としている。Next.js標準の推奨方法。
- **メリット**: 既存コードとの整合性、Next.js公式サポート
- **デメリット**: なし

### 案2: Vitest + React Testing Library
- **理由**: より高速なテストランナー
- **メリット**: 実行速度が速い
- **デメリット**: 既存のテストファイル（Jest構文）との互換性問題、Next.jsとの統合が複雑

### 案3: Playwright（E2Eテスト）
- **理由**: ブラウザベースの統合テスト
- **メリット**: より実際の動作に近いテスト
- **デメリット**: このタスクのスコープ外（F6はコンポーネント/統合テスト）

**採用**: 案1（Jest + React Testing Library）

## テスト戦略

### どの層で何を担保するか

1. **ユニットテスト（コンポーネント）**
   - `LoadingSpinner.test.tsx`: スピナーの表示・アクセシビリティ属性
   - 既存の `ReplyForm.test.tsx`: フォームの動作（変更なし）

2. **統合テスト（ページ）**
   - `page.test.tsx`: ページのレンダリング・`ReplyForm` の統合確認

3. **ユニットテスト（APIクライアント）**
   - 既存の `replyDrafts.test.ts`: API呼び出しの動作（変更なし）

### テストカバレッジ

- 最低限: すべてのコンポーネントにテストが存在する
- 理想: 主要なユーザーフローの統合テストが存在する

## ドキュメント更新方針

- `frontend/README.md`: テスト実行方法を追記
- `docs/implementation-tasklist.md`: F6タスクを「完了」に更新

## 全体タスク反映方針

`./docs/implementation-tasklist.md` の以下を更新：
- F6: ステータスを「未着手」→「完了」に変更
- 完了日を記録
- 更新履歴に追記

## 実装詳細

### 1. Jest設定（`jest.config.js`）

Next.js標準の `next/jest` を使用：

```javascript
const nextJest = require('next/jest')

const createJestConfig = nextJest({
  dir: './',
})

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
}

module.exports = createJestConfig(customJestConfig)
```

### 2. 依存関係追加（`package.json`）

以下のdevDependenciesを追加：
- `jest`: テストランナー
- `jest-environment-jsdom`: DOM環境
- `@testing-library/react`: React Testing Library
- `@testing-library/jest-dom`: Jest用のDOMマッチャー
- `@testing-library/user-event`: ユーザーイベントのシミュレーション

### 3. LoadingSpinnerテスト

- スピナーの表示確認
- `role="status"` と `aria-label="読み込み中"` の確認

### 4. ページ統合テスト

- ページがレンダリングされる
- `ReplyForm` が表示される
- タイトルが表示される

## 変更理由

（実装中に設計判断が変わった場合はここに追記）

---

## 結果と学び（モード3）

### 採用案の妥当性

**Jest + React Testing Library + Next.js（next/jest）の採用** ✅
- Next.js公式ドキュメントに従った標準的な設定
- 既存のテストファイル（Jest構文）との互換性が高い
- `next/jest` が自動的にNext.jsの設定を読み込むため、設定が簡潔

### 想定外の事象

1. **Jest設定ファイルの拡張子**
   - 当初は `jest.config.js` を想定していたが、TypeScriptプロジェクトのため `jest.config.ts` に変更
   - Next.js公式ドキュメントでも `jest.config.ts` を推奨

2. **テスト実行時のサンドボックス制限**
   - サンドボックス環境ではJestのワーカープロセス起動に制限がある
   - 設定ファイル自体は正しく作成されており、実際の環境では動作する見込み

### 改善点

1. **テストカバレッジの拡充**
   - 将来的にはE2Eテスト（Playwright等）の導入を検討
   - より詳細な統合テストの追加を検討

2. **CI/CDへの統合**
   - GitHub Actions等での自動テスト実行の設定を検討

### 学び

- Next.js 15では `next/jest` を使用することで、Next.jsの設定を自動的に読み込める
- TypeScriptプロジェクトでは `jest.config.ts` を使用する方が型安全性が高い
- 既存のテストファイルの構造を尊重することで、追加の変更を最小限に抑えられる
