# B4: 返信案生成ユースケース + AI呼び出し Port — タスクリスト

- [x] 調査・現状把握（architecture 3.5, implementation-tasklist B4, domain/models.py 確認）
- [x] ドメイン追加（CheckResult: ok, feedback を domain/models.py に追加、domain/__init__.py に export）
- [x] Application 層 Port 定義（application/ports.py: GenerateReplyDraftsPort, CheckReplyDraftsPort, ReviseReplyDraftsPort）
- [x] 返信案生成ユースケース実装（application/generate_reply_drafts.py: generate_reply_drafts、生成→チェック→作り直しオーケストレーション）
- [x] application/__init__.py で generate_reply_drafts と 3 Port を export
- [x] 既存テスト実行確認（tests/unit/domain/test_models.py 11 件パス）
- [x] ./docs/implementation-tasklist.md 更新（B4 完了、サマリー・進捗・更新履歴）
- [x] 振り返り（モード3: 受け入れ条件チェック結果を requirements.md、結果と学びを design.md に追記）

## 成果物一覧

| ファイル | 内容 |
|----------|------|
| backend/src/settlement_maker/domain/models.py | CheckResult 追加 |
| backend/src/settlement_maker/domain/__init__.py | CheckResult を __all__ に追加 |
| backend/src/settlement_maker/application/ports.py | 新規。3 Port（Protocol）定義 |
| backend/src/settlement_maker/application/generate_reply_drafts.py | 新規。generate_reply_drafts()、MAX_REVISE_ROUNDS=2 |
| backend/src/settlement_maker/application/__init__.py | generate_reply_drafts, 3 Port を export |
| docs/implementation-tasklist.md | B4 完了、進捗 6/24・バックエンド 4/8、更新履歴追記 |
