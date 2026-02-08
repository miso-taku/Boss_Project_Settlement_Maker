# B7: ドメイン / アプリケーション / API のテスト — 設計

## 方針

- **DDD 境界**: Domain / Application の振る舞いをテストで固定する。API 統合は TestClient + dependency overrides で Port をモックに差し替える。
- **テスト優先順位**: Domain Unit Test → Application Test → API 統合（development-guidelines 4 に従う）。

## データフロー（テスト観点）

- **Domain**: 値オブジェクトの生成・バリデーション（依頼文空拒否、残り時間負拒否、CheckResult の ok/feedback）をユニットテストで検証。
- **Application**: generate_reply_drafts にモック Port を渡し、1) チェック OK で初回生成結果が返る、2) チェック NG で revise が呼ばれ、最大 N 回後に返却される、を検証。
- **API**: TestClient で POST し、モック Port により 200 で固定の返信案リスト、422 でバリデーションエラーを検証（既存テストを維持）。

## テスト戦略

| 層 | 内容 | 場所 |
|----|------|------|
| Domain | RequestText, MySituation, Priority, ReplyDraft: 既存。CheckResult: 追加（ok=True/False, feedback の保持）。 | tests/unit/domain/test_models.py |
| Application | generate_reply_drafts: モック Generate/Check/Revise Port で、初回 OK で即返却・NG で revise 呼び出しを検証。 | tests/unit/application/test_generate_reply_drafts.py（新規） |
| API | POST /api/v1/reply-drafts: 既存の integration テストを維持。200/422 の契約を検証。 | tests/integration/test_reply_drafts_api.py |

## 代替案と採用理由

- **CheckResult を test_models.py に追加**: 既存のドメインテストと同じファイルで一貫性を保つ。採用。
- **Application テストを unit/application に新規作成**: レイヤごとにテストを分離。採用。
- **API 統合は既存のまま**: 既に Port を overrides でモックに差し替えており、契約を検証済み。不足があれば追加するのみ。採用。

## ドキュメント更新方針

- implementation-tasklist.md: B7 を完了にし、完了日・備考を記録。実装サマリー・セクション別進捗・更新履歴を更新。

## 全体タスク反映方針

- implementation-tasklist.md の B7 を完了。総タスク数 24 のうち完了 9、バックエンド 8 のうち完了 7。

---

## 結果と学び（モード3）

- **採用案の妥当性**: Domain に CheckResult テストを追加し、Application に generate_reply_drafts のモック Port テストを追加。API 統合は既存維持。テスト優先順位（Domain → Application → API）に従い整備済み。
- **想定外**: test_generate_reply_drafts_stops_after_max_revise_rounds で check_port.call_count の期待値を 3 としていたが、実装では max_revise_rounds=2 のときループ 2 回で check は 2 回のみ。2 に修正。max_revise_rounds=0 のときは check も revise も呼ばれないため call_count==0 に修正。
- **改善点**: なし。mypy は B8 で実施する想定（本タスクでは pytest と ruff で完了判定）。
