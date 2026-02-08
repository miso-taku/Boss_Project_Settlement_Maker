# 仕様変更: 返信案チェックを10点満点×3項目・全て8以上でOK — タスクリスト

- [x] ステアリング作成（requirements.md, design.md, tasklist.md）
- [x] 調査・現状把握（CheckResult / CheckResultSchema / チェックエージェントの参照箇所）
- [x] ドメイン: CheckResult を score_1, score_2, score_3, feedback に変更、ok をプロパティに
- [x] インフラ: CheckResultSchema と PydanticAICheckAdapter のプロンプト・出力修正
- [x] 単体テスト: domain test_models.py の CheckResult テスト更新
- [x] 単体テスト: application test_generate_reply_drafts.py の CheckResult 生成を新形式に
- [x] 統合テスト: test_reply_drafts_api.py の MockCheckPort を新形式に
- [x] uv run pytest -q で全テスト通過確認
- [x] 永続ドキュメント更新（architecture, functional-design, glossary）
- [x] implementation-tasklist.md に本仕様変更を追加・完了反映
- [x] lint/format（ruff check, ruff format）
- [x] 振り返り（モード3）
