# タスクリスト（Task List）

## 実装タスク

- [x] 調査・現状把握（既存UIの確認）
- [x] ステアリングファイル作成（requirements.md, design.md, tasklist.md）
- [ ] Chakra UIのインストール（@chakra-ui/react, @emotion/react, @emotion/styled, @chakra-ui/icons）
- [ ] ChakraProviderのセットアップ（app/layout.tsx）
- [ ] ReplyFormコンポーネントのChakra UI化
  - [ ] フォームフィールドの置き換え（FormControl, FormLabel, Textarea, Input, RadioGroup）
  - [ ] アイコンの追加
  - [ ] カード型レイアウトの適用
  - [ ] ボタンの改善（Buttonコンポーネント、ローディング状態）
  - [ ] エラー表示の改善（Alertコンポーネント）
  - [ ] 返信案表示の改善（Cardコンポーネント）
  - [ ] コピー成功時のToast通知
- [ ] ページレイアウトの改善（Container, Heading, Text）
- [ ] LoadingSpinnerコンポーネントの置き換え（Chakra UIのSpinner）
- [ ] レスポンシブ対応の確認・調整
- [ ] テストの更新
  - [ ] ReplyForm.test.tsxの更新（Chakra UIコンポーネント対応）
  - [ ] page.test.tsxの更新
  - [ ] LoadingSpinner.test.tsxの更新（または削除）
- [ ] lint/format実行
- [ ] 動作確認（開発サーバーでの確認）
- [ ] ./docs更新
  - [ ] architecture.md（Chakra UI追記）
  - [ ] implementation-tasklist.md（F8タスク追加）
- [ ] ステアリング（モード3）振り返り
