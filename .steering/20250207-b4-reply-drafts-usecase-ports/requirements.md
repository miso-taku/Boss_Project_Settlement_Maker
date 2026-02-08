# B4: 返信案生成ユースケース + AI呼び出し Port — 要求

## 背景 / 目的

- **背景**: implementation-tasklist B3 で依頼文・自分の状況・返信案のドメインモデル（RequestText, MySituation, Priority, ReplyDraft）が完了。次に Application 層で「返信案生成」のユースケースと、AI 呼び出しを抽象化する Port を用意する必要がある。
- **目的**: architecture 3.5（生成→チェック→作り直し）に従い、返信案生成ユースケースと AI 呼び出し Port（生成・チェック・作り直しの 3 Port）を実装し、オーケストレーションを Application 層に固定する。

## スコープ（やること / やらないこと）

### やること

- ドメインにチェック結果を表す型（CheckResult: OK/NG・指摘）を追加
- Application 層に AI 呼び出し Port を 3 つ定義（Protocol）
  - GenerateReplyDraftsPort: 依頼文＋自分の状況 → 返信案リスト（初稿）
  - CheckReplyDraftsPort: 返信案リスト＋依頼文・状況 → チェック結果
  - ReviseReplyDraftsPort: 返信案＋チェック指摘＋依頼文・状況 → 返信案リスト（修正版）
- 返信案生成ユースケースのオーケストレーション（生成 → チェック → 必要なら作り直し、最大 N 回）
- `./docs/implementation-tasklist.md` の B4 を完了に更新

### やらないこと

- PydanticAI エージェントの具体実装（B5 で実施）
- FastAPI ルータ・DTO・API 実装（B6 で実施）
- ユースケースの自動テスト（B7 で実施）

## 受け入れ条件（Given-When-Then）

- **Given** B3 のドメインモデル（RequestText, MySituation, ReplyDraft）が存在する
- **When** Application 層の Port とユースケースを実装する
- **Then** 3 つの Port（Protocol）が定義され、ユースケースが「生成→チェック→作り直し（最大 N 回）」のフローでオーケストレーションする
- **And** 最大作り直し回数 N で無限ループを防いでいる
- **And** Domain に CheckResult（ok, feedback）が存在する

## 影響範囲

| 領域 | 内容 |
|------|------|
| FE | なし |
| BE | domain/models.py（CheckResult 追加）, application/ports.py（新規）, application/generate_reply_drafts.py（新規）, application/__init__.py（export 追加） |
| API | なし（B6 で実施） |
| DB | なし |
| Docs | implementation-tasklist.md の B4 を完了に更新 |

## 未決事項 / リスク / 仮定

- **仮定**: 最大作り直し回数 N は 2 回（MAX_REVISE_ROUNDS）で固定。将来的に設定可能にしてもよい。
- **仮定**: Port は typing.Protocol で定義し、Infrastructure（B5）で Adapter として実装する。
- 未決事項なし。

---

## 受け入れ条件チェック結果（モード3）

- **Port 3 つ**: GenerateReplyDraftsPort, CheckReplyDraftsPort, ReviseReplyDraftsPort を application/ports.py に Protocol で定義 → **充足**。
- **オーケストレーション**: generate_reply_drafts() が生成→チェック→作り直し（最大 2 回）のフローで Port を呼び出す → **充足**。
- **CheckResult**: domain/models.py に ok, feedback の値オブジェクトを追加 → **充足**。
- **無限ループ防止**: max_revise_rounds でループ上限を設け、最終的な返信案リストを返却 → **充足**。
- **implementation-tasklist.md**: B4 を完了に更新し、サマリー・進捗・更新履歴を反映 → **充足**。
