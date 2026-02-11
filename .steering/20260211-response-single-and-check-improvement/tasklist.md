# タスクリスト（tasklist）

## ステアリング（モード1）

- [x] requirements.md 作成
- [x] design.md 作成
- [x] tasklist.md 作成

## 実装

### バックエンド

- [x] Domain: CheckResult を must_fix / nice_to_have に変更（feedback 削除）
- [x] Domain: score_sum 用のプロパティを追加
- [x] Application: generate_reply_drafts で score_sum 改善なしで終了する条件を追加
- [x] Infrastructure: CheckResultSchema を must_fix + nice_to_have に変更
- [x] Infrastructure: チェック・作り直し Adapter のプロンプトとマッピングを更新
- [x] Interface: DTO を draft 単数に変更、ルートで draft を返す
- [x] 単体テスト: domain (CheckResult), application (改善なし終了)
- [x] 統合テスト: レスポンスが draft を含むことを検証

### フロントエンド

- [x] types: GenerateReplyDraftsResponse を draft に変更
- [x] replyDrafts: レスポンス型を draft に合わせる
- [x] ReplyForm: response.draft を参照するよう変更
- [x] テスト: ReplyForm, replyDrafts のモックを draft に変更

### ドキュメント・振り返り

- [x] docs: architecture, functional-design, glossary を更新
- [x] implementation-tasklist.md に本作業を反映（S3 追加）
- [x] ステアリング（モード3）振り返り（design.md に追記）
