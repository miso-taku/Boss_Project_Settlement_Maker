# 設計（design）

## 方針

- **API 契約**: レスポンスを `draft: { text: string }` に統一。破壊的変更のため、FE/BE を同時に更新する。
- **DDD**: CheckResult はドメインの値オブジェクトとして must_fix / nice_to_have を持つ。Revise はこれらを結合してプロンプト用の指摘文を生成する。
- **ループ終了**: max_revise_rounds に加え、直前の score_sum 以上でない場合は「改善なし」とみなし、その時点の drafts を返して終了する。

## データフロー

1. POST /api/v1/reply-drafts → 依頼文・状況
2. Generate → 返信案 1 件（list[ReplyDraft] の 1 要素）
3. Check → CheckResult(scores, must_fix, nice_to_have)、ok でなければ score_sum を計算
4. 前回の score_sum ありかつ 今回の score_sum <= 前回 → ループ終了、現在の draft を返す
5. そうでなければ Revise → 指摘（must_fix + nice_to_have）をプロンプトに渡す → 修正版 1 件
6. 最大 max_revise_rounds または改善なしで終了 → レスポンスは `draft: { text }` に変換

## API 変更

- **エンドポイント**: POST /api/v1/reply-drafts（変更なし）
- **レスポンス（200）**
  - 変更前: `{ "drafts": [ { "text": "..." } ] }`
  - 変更後: `{ "draft": { "text": "..." } }`
- **互換性**: 破壊的変更。FE は draft を参照するよう同時に修正する。

## チェック結果の構造

### Domain (CheckResult)

- `score_1`, `score_2`, `score_3`: int（0–10）（変更なし）
- `must_fix`: tuple[str, ...]（イミュータブル、空可）
- `nice_to_have`: tuple[str, ...]（イミュータブル、空可）
- `ok`: 全スコア >= 8（変更なし）
- プロンプト用の指摘文が必要な場合は、Application または Adapter で must_fix と nice_to_have を結合して文字列化する。

### Infrastructure (CheckResultSchema)

- `score_1`, `score_2`, `score_3`: int（0–10）
- `must_fix`: list[str]（必須修正の箇条書き）
- `nice_to_have`: list[str]（任意改善の箇条書き）

## ループ終了条件（Application）

- `previous_score_sum: int | None = None` をループ外で初期化。
- 各ループで:
  1. check 実行 → check_result
  2. もし check_result.ok → return drafts
  3. current_score_sum = score_1 + score_2 + score_3
  4. もし previous_score_sum is not None かつ current_score_sum <= previous_score_sum → return drafts（改善なしで終了）
  5. previous_score_sum = current_score_sum
  6. drafts = revise(...)
  7. 最大回数に達したら次で return

## テスト戦略

- Domain: CheckResult の must_fix / nice_to_have の生成・ok 判定のユニットテストを追加・修正。
- Application: 改善なしで終了するケースのユニットテストを追加。既存のモックは CheckResult の生成を must_fix/nice_to_have に合わせる。
- Integration: レスポンスが `draft` を含み `drafts` を含まないことを検証。
- FE: types, API クライアント、ReplyForm のテストで `draft` を期待するように修正。

---

## 振り返り（モード3）

- **採用案の妥当性**: レスポンスを draft 単数にしたことで API 契約と実装が一致した。CheckResult の must_fix / nice_to_have により作り直しプロンプトで必須・任意を区別できる。score_sum 改善なしで終了する条件により、8点以下が続く場合の無駄なループを防げた。
- **実施内容**: Domain CheckResult を must_fix / nice_to_have に変更し score_sum プロパティを追加。Application で previous_score_sum を保持し current_score_sum <= previous_score_sum で終了。Infrastructure の CheckResultSchema とチェック・作り直しプロンプトを更新。API DTO とルートを draft 単数に変更。FE の types / ReplyForm / テストを draft に合わせて更新。docs（architecture, functional-design, glossary）と implementation-tasklist（S3）を更新。
- **想定外**: なし。

## ドキュメント更新

- architecture.md: レスポンスを draft 単数に、チェック出力を scores / must_fix / nice_to_have に記述。
- functional-design.md: データフロー・出力仕様の記述を更新。
- glossary.md: チェック結果の用語を must_fix / nice_to_have に合わせる。
- implementation-tasklist.md: 本作業の完了を反映。
