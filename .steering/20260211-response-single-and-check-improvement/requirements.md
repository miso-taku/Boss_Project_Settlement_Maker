# 要求（requirements）

## 背景・目的

- API レスポンスが「リスト」形式（`drafts`）のままなのに常に 1 件のみ返しており、契約と実装が一致していない。
- チェックが 8 点以下で合格しない場合、作り直しループでスコアが改善しないまま max_retries まで回り続ける可能性がある。
- チェックエージェントの指摘が 1 つの `feedback` 文字列のみで、必須修正と任意改善の区別がつかない。

上記を解消し、レスポンスを単数形に統一し、ループ終了条件を明確にし、チェック出力を必須修正・任意改善に分ける。

## スコープ

### やること

1. **API レスポンスを単数へ**
   - レスポンスを `draft: { text: string }` に変更（`drafts` リストを廃止）。

2. **チェックループの改善**
   - `max_retries = 2` は維持。
   - 加えて、直前のチェック結果の `score_sum`（score_1 + score_2 + score_3）と比較し、**改善しない場合（同じまたは悪化）はループを終了**する。

3. **チェックエージェント出力の変更**
   - `scores`: 3 項目の数値（従来の score_1, score_2, score_3 に相当）。
   - `must_fix`: 箇条書き（必須修正）。
   - `nice_to_have`: 箇条書き（任意改善）。
   - 従来の `feedback` 単一文字列は廃止し、上記 2 リストで表現する。

### やらないこと

- 返信案の複数件返却（1 件のまま）。
- 認証・履歴保存の追加。

## 受け入れ条件

- **Given** 依頼文と自分の状況を送信する **When** POST /api/v1/reply-drafts を呼ぶ **Then** レスポンスは `draft: { text: string }` を含み、`drafts` は含まない。
- **Given** チェックが NG で作り直しを行う **When** 作り直し後の score_sum が前回以下 **Then** ループは終了し、その時点の返信案を返す。
- **Given** チェックエージェントの出力 **When** 構造化される **Then** `scores`（3 数値）、`must_fix`（文字列リスト）、`nice_to_have`（文字列リスト）を持つ。

## 影響範囲

| 領域 | 内容 |
|------|------|
| BE Domain | CheckResult の feedback → must_fix, nice_to_have |
| BE Application | generate_reply_drafts のループ終了条件（score_sum 改善なしで終了） |
| BE Infrastructure | CheckResultSchema、チェック・作り直しプロンプト |
| BE Interface | DTO を draft 単数に、ルートで draft を返す |
| FE | types, replyDrafts, ReplyForm（draft 参照） |
| Docs | architecture, functional-design, glossary, implementation-tasklist |

## 未決事項・仮定

- なし。上記で確定して実装する。
