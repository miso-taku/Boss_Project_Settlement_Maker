# F2: API クライアント（返信案生成 API 呼び出し）— タスクリスト

## 実装タスク

- [x] 調査・現状把握
  - [x] バックエンドの DTO 定義を確認（`backend/src/settlement_maker/interface/dto/reply_drafts.py`）
  - [x] 既存のフロントエンド構造を確認（`frontend/src/api/` の有無）
  - [x] Next.js の環境変数設定方法を確認

- [x] TypeScript 型定義の作成
  - [x] `frontend/src/api/types.ts` を作成
  - [x] `GenerateReplyDraftsRequest` 型を定義
  - [x] `ReplyDraftItem` 型を定義
  - [x] `GenerateReplyDraftsResponse` 型を定義
  - [x] `Priority` 型（"high" | "medium" | "low"）を定義

- [x] API クライアント関数の実装
  - [x] `frontend/src/api/replyDrafts.ts` を作成
  - [x] `generateReplyDrafts` 関数を実装
  - [x] 環境変数 `NEXT_PUBLIC_API_BASE_URL` を使用（デフォルト: `http://localhost:8000`）
  - [x] `fetch` API で POST リクエストを送信
  - [x] レスポンスを JSON としてパース
  - [x] TypeScript 型で返却

- [x] エラーハンドリングの実装
  - [x] カスタムエラークラス `ApiError` を作成（必要に応じて）
  - [x] HTTP エラー（4xx, 5xx）を適切に処理
  - [x] ネットワークエラーを適切に処理
  - [x] バリデーションエラー（422）を適切に処理

- [x] ユニットテストの実装
  - [x] `frontend/src/api/__tests__/replyDrafts.test.ts` を作成
  - [x] 正常系のテスト（モック fetch）
  - [x] 異常系のテスト（HTTP エラー、ネットワークエラー）

- [x] 環境変数の設定
  - [x] `.env.local.example` を作成（必要に応じて）
  - [x] `NEXT_PUBLIC_API_BASE_URL` の設定方法をドキュメント化（README 等）

## 検証・確認

- [x] lint/format
  - [x] `npm run lint` を実行してエラーがないことを確認（lintエラーなしを確認）
  - [x] 必要に応じて `npm run format` を実行

- [ ] テスト実行
  - [ ] `npm test` または `npm run test` を実行してテストが通過することを確認（F6 でテスト設定を追加予定のため、今回はテストファイル作成のみ）

- [ ] 動作確認（手動）
  - [ ] バックエンドサーバーを起動（`uv run uvicorn settlement_maker.interface.app:app --reload`）
  - [ ] フロントエンド開発サーバーを起動（`npm run dev`）
  - [ ] ブラウザの開発者ツールで API リクエストが正しく送信されることを確認（F3 以降で UI 実装後に確認可能な場合は、F3 以降で実施）

## ドキュメント更新

- [x] `./docs/implementation-tasklist.md` を更新
  - [x] F2 を「完了」に変更
  - [x] 完了日を記録
  - [x] 備考を記録
  - [x] 実装サマリーを更新（完了 14、フロントエンド完了 2）
  - [x] セクション別進捗を更新
  - [x] 更新履歴を追加

- [x] 必要に応じて `./docs/architecture.md` を更新（API クライアントの実装方針が一致していることを確認）

## 振り返り（モード3）

- [x] `requirements.md` の受け入れ条件が満たされたかチェック結果を追記
- [x] `tasklist.md` の残タスクがないか確認（未完があれば理由と次アクション）
- [x] `design.md` に結果と学びを追記（採用案の妥当性、想定外、改善点）

---
