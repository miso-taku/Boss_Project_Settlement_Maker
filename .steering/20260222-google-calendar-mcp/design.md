# 設計（design）

## 方針

- **DDD 境界**: 予定取得は「自分の状況」を補完する副次的入力。Domain は既存の MySituation を維持し、Application に「予定取得 → 残り時間・制約の導出」ユースケースを追加する。MCP 呼び出しは Infrastructure（Port/Adapter）に閉じる。
- **MCP**: Pydantic AI の **MCPServerStdio** を使用。サブプロセスで MCP サーバー（Google Calendar 用）を起動し、`env` で `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` を渡す。
- **契約**: 既存 `POST /api/v1/reply-drafts` を拡張し、入力ソース（手動 / calendar）と、calendar 時の日付パラメータを追加する。破壊を避けるため、既存フィールドはそのまま残し、新フィールドで選択と日付を渡す。

## データフロー

### 手動入力（現状どおり）

```
[FE] 依頼文 + remaining_hours + priority + constraints
  → POST /api/v1/reply-drafts (situation_source=manual または省略)
[BE] → MySituation をそのまま構築 → 返信案生成フロー
```

### Google Calendar 取得

```
[FE] 依頼文 + situation_source=calendar + calendar_date=YYYY-MM-DD（省略時は今日）
  → POST /api/v1/reply-drafts
[BE]
  1. situation_source=calendar なら Calendar Port（MCP）で予定取得
  2. 取得結果から remaining_hours, constraints を導出（優先度は未設定または別パラメータ）
  3. MySituation(remaining_hours=導出値, priority=None, constraints=導出値) を構築
  4. 既存の返信案生成フローに渡す
```

代替案: 「予定取得」を別エンドポイント（例: `GET /api/v1/calendar/situation?date=YYYY-MM-DD`）にし、FE が先に呼んで画面に表示してから、返信案生成では手動と同様に body で送る。  
→ **採用案**: 1リクエストで完結するよう、POST の body で `situation_source` と `calendar_date` を渡し、BE で予定取得〜導出〜生成まで行う。シンプルで FE の状態管理も少ない。

## API 変更

- **エンドポイント**: `POST /api/v1/reply-drafts`（変更なし、body を拡張）
- **リクエスト body 追加案**
  - `situation_source`: `"manual"` | `"calendar"`（任意、デフォルト `"manual"`）。`"calendar"` のときは `remaining_hours` / `constraints` は無視し、`calendar_date` から導出する。
  - `calendar_date`: `"YYYY-MM-DD"`（任意）。`situation_source=calendar` のときのみ使用。省略時はサーバー日付の「今日」。
- **既存フィールド**: `request_text`, `remaining_hours`, `priority`, `constraints` はそのまま。`situation_source=manual` または省略時は従来どおり使用。
- **互換性**: 新フィールドは任意のため、既存クライアントは変更不要。FE は `situation_source` と `calendar_date` を送るよう拡張する。

## 残り時間・制約の導出ルール（仮定）

- **残り時間**: 対象日の業務時間は **固定 9:00–18:00（9時間）**。取得した予定の合計時間（分→時間）を引き、空き時間を残り時間とする。予定がなければ 9、予定が 2 時間なら 7。環境変数やリクエストでは変更しない（ユーザー回答 A）。
- **制約**: 取得した予定を「HH:MM–HH:MM 予定名」の形式で改行連結した文字列を `constraints` に設定する。例: `"10:00–11:00 定例\n14:00–15:00 打ち合わせ"`。
- **優先度**: カレンダー取得時は `priority` は送信しない（None）。必要なら FE で取得後に手動で上書きするフィールドを残す。

## MCP（MCPServerStdio）の使い方

- **採用 MCP**: 環境変数で `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` を直接受け取る **mcp-google** を採用（ユーザー回答 B-3。@nspady/google-calendar-mcp は JSON ファイル必須のため不採用）。
- **接続**: `pydantic_ai.mcp.MCPServerStdio(command, args, env=..., timeout=...)`。Agent の `toolsets=[server]` に渡す。
- **起動例**: `command='npx', args=['-y', 'mcp-google']`、`env` に `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` を渡す（.env から読み取り）。
- **利用形態**: 返信案生成エージェントとは別に、「予定取得専用」の Agent を用意し、`list-events` ツールを呼び出して予定一覧を取得。その結果をパースして remaining_hours / constraints を計算する。
- **ライフサイクル**: 予定取得のたびに MCPServerStdio のサブプロセスを起動するか、リクエスト間で再利用するかは実装で決定。stdio はコンテキストマネージャで `async with server` して開始・終了する。

## テスト戦略

- **Domain**: 変更なし。既存の MySituation のまま。
- **Application**: 予定取得ユースケースのユニットテスト（Calendar Port をモックし、返却イベントから MySituation が期待どおり構築されることを検証）。
- **Infrastructure**: MCP 接続・ツール呼び出しは結合テストまたは手動確認。CI では Google 認証なしでスキップするオプションを検討。
- **Interface**: DTO に `situation_source`, `calendar_date` を追加。統合テストで `situation_source=calendar` 時はモック Port で導出結果が返信案生成に使われることを確認。
- **FE**: 入力ソース切替・カレンダー日付入力・生成実行の E2E またはコンポーネントテスト。

## ドキュメント更新方針

- **functional-design.md**: 自分の状況の入力方法に「手動」と「Google Calendar 取得」を追記。データフローに calendar 分岐を追加。
- **architecture.md**: MCP（MCPServerStdio）利用、導出ルール、環境変数（GOOGLE_*）、API の新パラメータを追記。
- **glossary.md**: 「自分の状況」の取得元として Google Calendar / 予定取得を追記。
- **implementation-tasklist.md**: 本機能のタスクを追加し、完了時にチェックする。

## 全体タスクリスト反映方針

- `./docs/implementation-tasklist.md` に「Google Calendar MCP で予定取得・手動/カレンダー選択」のようなタスクを 1 件追加し、完了時にステータスを「完了」に更新する。

---

## 振り返り（モード3）

- **採用案**: mcp-google を MCPServerStdio で起動し、direct_call_tool("list-events", { timeMin, timeMax, maxResults }) で予定を取得。ToolResult は list/dict/str のいずれかになるため _extract_events_from_tool_result で共通パース。残り時間は業務時間 9–18 固定から予定時間を引いて算出。制約は「HH:MM–HH:MM 予定名」の改行連結。
- **実施内容**: GetCalendarSituationPort と get_my_situation_from_calendar を追加。CalendarMCPAdapter を infrastructure/calendar_mcp_adapter.py に実装。DTO に situation_source, calendar_date を追加。ルートを async 化し、situation_source=calendar 時に calendar_port を注入して予定取得。FE で入力元ラジオと対象日 date 入力を追加。docs と implementation-tasklist（S4）を更新。
- **未実施・要確認**: 実機での mcp-google 認証（初回 OAuth ブラウザ）と list-events 戻り値形式の実機確認。フロントの Jest は環境により EPERM でスキップ。

## 代替案と採用理由

| 案 | 内容 | 採用理由 |
|----|------|----------|
| A | POST の body で situation_source + calendar_date を渡し、BE で一括処理 | 1 リクエストで完結し、FE がシンプル。採用。 |
| B | 予定取得を別 GET エンドポイントにし、FE で取得→表示→生成で 2 回呼ぶ | 取得結果のプレビューはしやすいが、2 回往復と状態管理が増える。今回は不採用。 |
| C | 残り時間を「今から次の予定まで」で計算 | 実装は簡単だが、「今日の稼働可能時間」の方が依頼返信の文脈に合うと判断。業務時間ベースを採用。 |
