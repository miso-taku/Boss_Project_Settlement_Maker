# 設計（Design）

## 方針（DDD境界、責務分割）

- **UI改善のみ**: ドメインロジック・API契約は変更しない
- **段階的移行**: インラインスタイルからChakra UIへ段階的に移行
- **コンポーネント分割**: 必要に応じて小さなコンポーネントに分割（ただし過度な分割は避ける）

## データフロー（簡易）

```
[ユーザー入力]
  ↓
[ReplyForm (Chakra UI)]
  ↓
[API呼び出し] (変更なし)
  ↓
[返信案表示 (Chakra UI)]
  ↓
[コピー機能] (変更なし)
```

## UI変更（コンポーネント・レイアウト）

### Chakra UI導入
- `@chakra-ui/react` と `@emotion/react`, `@emotion/styled` をインストール
- `ChakraProvider` を `app/layout.tsx` に追加
- デフォルトテーマを使用（必要に応じてカスタマイズ可能）

### ReplyFormコンポーネント改善
- **入力エリア**: `Card` コンポーネントで囲む
- **フォームフィールド**: `FormControl`, `FormLabel`, `Textarea`, `Input`, `RadioGroup` を使用
- **アイコン**: `@chakra-ui/icons` から適切なアイコンを追加
  - 依頼文: `EditIcon` または `ChatIcon`
  - 残り時間: `TimeIcon` または `ClockIcon`
  - 優先度: `StarIcon` または `WarningIcon`
  - 制約: `InfoIcon` または `LockIcon`
- **ボタン**: `Button` コンポーネント（ローディング状態対応）
- **エラー表示**: `Alert`, `AlertIcon`, `AlertTitle`, `AlertDescription` を使用
- **返信案表示**: `Card`, `CardHeader`, `CardBody` を使用
- **コピー成功**: `useToast` フックでトースト通知

### ページレイアウト改善
- `Container` コンポーネントで最大幅を制御
- `Heading`, `Text` コンポーネントでタイポグラフィを統一
- レスポンシブ対応（`Stack`, `Box` の `spacing` プロパティ活用）

### ローディング表示
- Chakra UIの `Spinner` コンポーネントを使用（既存の `LoadingSpinner` を置き換え）

## API変更（エンドポイント、リクエスト/レスポンス概要、互換性）

- **変更なし**: API契約は変更しない

## 代替案（2〜3案）と採用理由

### 案1: Chakra UI導入（採用）
- **理由**: 
  - アクセシビリティが高い
  - コンポーネントが豊富
  - Next.jsとの統合が容易
  - TypeScriptサポートが充実

### 案2: Tailwind CSS導入
- **理由（不採用）**: 
  - より細かいカスタマイズが必要
  - コンポーネントライブラリではないため、より多くの実装が必要

### 案3: Material-UI導入
- **理由（不採用）**: 
  - デザインがより重い
  - Chakra UIの方が軽量で柔軟

## テスト戦略（どの層で何を担保するか）

### フロントエンド
1. **コンポーネントテスト**: 
   - ReplyFormのレンダリングテスト（Chakra UIコンポーネントの存在確認）
   - フォーム入力・送信のテスト（既存テストを更新）
   - エラー表示のテスト
   - コピー機能のテスト
2. **統合テスト**: 
   - ページ全体のレンダリングテスト
   - API呼び出しの統合テスト（既存テストを更新）

### バックエンド
- **変更なし**: テスト変更不要

## ドキュメント更新方針（./docs のどれが影響するか）

- `architecture.md`: 技術スタックにChakra UIを追記
- `implementation-tasklist.md`: UI改善タスクを追加

## 全体タスク反映方針（`./docs/implementation-tasklist.md` のどれに影響するか）

- セクション3（フロントエンド）に新しいタスクを追加:
  - F8: UI改善（Chakra UI導入）
