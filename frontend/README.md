# フロントエンド（Next.js）

上司案件・落とし所AIエージェントのフロントエンド実装。

## 技術スタック

- Next.js 15.1.6（App Router）
- React 18.3.1
- TypeScript 5.7.2
- ESLint（Next.js 標準設定）
- Jest + React Testing Library（テスト）

## 開発

```bash
# 依存関係のインストール
npm install

# 環境変数の設定（.env.local を作成）
# .env.local.example を参考に、NEXT_PUBLIC_API_BASE_URL を設定
# デフォルト: http://localhost:8000

# 開発サーバー起動
npm run dev
```

開発サーバーは http://localhost:3000 で起動します。

### 環境変数

- `NEXT_PUBLIC_API_BASE_URL`: バックエンド（FastAPI）のベース URL（デフォルト: `http://localhost:8000`）

`.env.local.example` を参考に `.env.local` を作成して設定してください。

## ビルド

```bash
npm run build
npm start
```

## テスト

### テスト実行

```bash
# すべてのテストを実行
npm test

# ウォッチモードでテストを実行（ファイル変更時に自動実行）
npm run test:watch
```

### テスト環境

- **Jest**: テストランナー
- **React Testing Library**: Reactコンポーネントのテスト
- **@testing-library/jest-dom**: DOM要素のアサーション拡張

### テストファイルの配置

- `src/components/__tests__/` - コンポーネントのユニットテスト
- `src/app/__tests__/` - ページの統合テスト
- `src/api/__tests__/` - APIクライアントのユニットテスト

### テストカバレッジ

現在のテスト対象：

- `ReplyForm` コンポーネント（フォーム入力・API呼び出し・返信案表示・コピー機能）
- `LoadingSpinner` コンポーネント（表示・アクセシビリティ）
- `page.tsx`（ページレンダリング・ReplyForm統合）
- `replyDrafts.ts`（APIクライアントの正常系・異常系）

## ディレクトリ構造

- `src/app/` - App Router（ルーティング）
- `src/api/` - API クライアント集約（F2 で実装）
- `src/components/` - React コンポーネント
- `src/hooks/` - カスタムフック
- `public/` - 静的ファイル
