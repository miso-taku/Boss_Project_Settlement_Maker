# B3: 依頼文・自分の状況・返信案のドメインモデル — タスクリスト

- [x] 調査・現状把握（architecture 3.1, glossary, repository-structure, domain/ 構成確認）
- [x] ドメインモデル定義（domain/models.py: Priority, RequestText, MySituation, ReplyDraft）
- [x] domain/__init__.py でエクスポート（__all__ に追加）
- [x] ./docs/implementation-tasklist.md 更新（B3 完了、サマリー・進捗・更新履歴）
- [x] ユニットテスト追加（tests/unit/domain/test_models.py: 11 件、事後対応）
- [x] ステアリング記録（本フォルダ requirements.md / design.md / tasklist.md）

## 成果物一覧

| ファイル | 内容 |
|----------|------|
| backend/src/settlement_maker/domain/models.py | 新規。Priority, RequestText, MySituation, ReplyDraft |
| backend/src/settlement_maker/domain/__init__.py | RequestText, MySituation, Priority, ReplyDraft を export |
| tests/unit/domain/__init__.py | 新規（ドメイン単体テスト用） |
| tests/unit/domain/test_models.py | 新規。Priority / RequestText / MySituation / ReplyDraft のユニットテスト 11 件 |
| docs/implementation-tasklist.md | B3 完了、進捗 5/24・バックエンド 3/8、更新履歴追記 |
| .steering/20250207-b3-domain-models/ | 本ステアリング（requirements.md, design.md, tasklist.md） |
