# B4: 返信案生成ユースケース + AI呼び出し Port — 設計

## 方針

- **DDD 境界**: Application 層は Domain に依存し、外部 I/O（AI 呼び出し）は Port（抽象）経由のみとする。Infrastructure が後から Adapter で実装する（B5）。
- **責務分割**: Port は「何を渡して何を得るか」の契約のみ定義。ユースケースは「生成→チェック→作り直し」の順序と終了条件（OK または最大回数）を担当する。

## データフロー

```
[RequestText, MySituation]
    → GenerateReplyDraftsPort.generate() → list[ReplyDraft]（初稿）
    → CheckReplyDraftsPort.check()      → CheckResult（OK/NG + feedback）
    → (NG かつ 回数 < N) ReviseReplyDraftsPort.revise() → list[ReplyDraft]（修正版）
    → ループ until OK or 最大回数
    → list[ReplyDraft]（最終版）
```

## ドメイン追加

- **CheckResult**（domain/models.py）
  - `ok: bool` — True: 合格, False: 要修正
  - `feedback: str` — 指摘・改善点（NG 時）。OK の場合は空文字可
  - frozen dataclass。I/O 禁止の値オブジェクト。

## Port 定義（application/ports.py）

| Port | メソッド | 入力 | 出力 |
|------|----------|------|------|
| GenerateReplyDraftsPort | generate(request_text, my_situation) | RequestText, MySituation | list[ReplyDraft] |
| CheckReplyDraftsPort | check(drafts, request_text, my_situation) | list[ReplyDraft], RequestText, MySituation | CheckResult |
| ReviseReplyDraftsPort | revise(drafts, check_result, request_text, my_situation) | list[ReplyDraft], CheckResult, RequestText, MySituation | list[ReplyDraft] |

- いずれも `typing.Protocol` で定義。メソッド名を明示（generate / check / revise）し、B5 でクラス実装しやすくする。

## ユースケース（application/generate_reply_drafts.py）

- **関数**: `generate_reply_drafts(request_text, my_situation, *, generate_port, check_port, revise_port, max_revise_rounds=2)`
- **フロー**:
  1. generate_port.generate() で初稿を取得
  2. 最大 max_revise_rounds 回まで: check_port.check() → OK なら return / NG なら revise_port.revise() で修正版を取得し、次のループで再チェック
  3. 最大回数に達した場合も、その時点の list[ReplyDraft] を返却（打ち切り時も返信案は返す）

## 代替案と採用理由

- **Port を 1 つにまとめる案**: 生成・チェック・作り直しを 1 つの Port にまとめると、Application が「オーケストレーション」を持てず、Infrastructure にフローが漏れる。採用せず。3 Port で分離し、オーケストレーションは Application に集約。
- **ユースケースをクラスにする案**: 現状は依存注入が「関数のキーワード引数」で足りる。クラスにするとコンストラクタ注入で同じことができるが、現時点では関数で十分と判断。

## テスト戦略

- B4 ではユースケースの単体テストは未実装（B7 でドメイン/アプリケーション/API のテストを実施）。
- 既存の domain テスト（test_models.py）は 11 件すべてパスすることを確認済み。CheckResult のテストは B7 で追加可能。

## ドキュメント更新方針

- `./docs/implementation-tasklist.md`: B4 を「完了」にし、完了日・備考（CheckResult, ports.py, generate_reply_drafts.py）を記録。実装サマリー・セクション別進捗・更新履歴を更新。

## 全体タスク反映方針

- implementation-tasklist.md の B4 を完了。総タスク数 24 のうち完了 6、バックエンド 8 のうち完了 4（50%）。

---

## 結果と学び（モード3）

- **採用案の妥当性**: 3 Port + 1 ユースケース関数で、architecture 3.5 のフローをそのままコードに落とせた。Port は Protocol で定義し、B5 で PydanticAI を呼ぶ Adapter が実装しやすい形になっている。
- **想定外**: 特になし。
- **改善点**: B7 でユースケースのテストを追加する際、モック Port を渡して「生成→チェック OK で 1 回で返る」「チェック NG → 作り直し → チェック OK」等のシナリオを検証するとよい。
