# 要求（requirements）

## 背景・目的

- 現状、自分の状況（残り時間・制約）は手動入力のみ。
- Google Calendar から予定を取得し、そこから「残り時間」と「制約」を導出できるようにすることで、ユーザーは手動入力かカレンダー取得のいずれかを選べるようにする。
- MCP サーバー経由で Google Calendar を参照し、Pydantic AI の **MCPServerStdio** を使用する。

## スコープ

### やること

1. **入力ソースの選択**
   - UI で「手動入力」と「Google Calendar から取得」を選択できるようにする。
   - 手動選択時: 従来どおり残り時間・優先度・制約をフォームで入力。
   - Google Calendar 選択時: 指定日（初期は「今日」を想定）の予定を MCP 経由で取得し、BE で残り時間・制約を導出して返信案生成に利用する。

2. **バックエンド**
   - MCP クライアントを **Pydantic AI の MCPServerStdio** で接続する。
   - 利用する MCP サーバーは Google Calendar 用（例: `npx -y @nspady/google-calendar-mcp` 等、実装時に採用するパッケージを確定）。
   - 環境変数 `GOOGLE_CLIENT_ID` と `GOOGLE_CLIENT_SECRET` は .env に追加済みとして、BE から MCP サブプロセスに渡す。
   - 予定取得結果から「残り時間」「制約」を導出するロジックを Application または Infrastructure に実装する（導出ルールは design で定義）。

3. **API・契約**
   - 依頼文は従来どおり必須。
   - 自分の状況について「手動」の場合は既存の `remaining_hours` / `priority` / `constraints` をそのまま送信。
   - 「Google Calendar」の場合は、取得対象日（例: `date` または `calendar_date`）を送信し、BE が MCP で予定取得 → 残り時間・制約を導出 → 既存の返信案生成フローに渡す。
   - 既存の `POST /api/v1/reply-drafts` を拡張するか、新エンドポイントを追加するかは design で決定。

4. **フロントエンド**
   - 入力ソース選択（手動 / Google Calendar）の UI を追加。
   - Google Calendar 選択時は、日付指定（任意で今日固定でも可）と「取得」実行で、BE から導出された残り時間・制約を表示し、その状態で返信案生成を実行できるようにする。

### やらないこと

- ユーザー認証・ログイン（デモのまま）。
- 返信案のメール/Slack 送信。
- 履歴の永続保存。
- Google Calendar 以外の MCP サーバー対応（本タスクでは Google Calendar に限定）。

## 受け入れ条件

- **Given** ユーザーが「手動入力」を選択している **When** 残り時間・優先度・制約を入力して生成する **Then** 従来どおり POST で送信され、返信案が1件返る。
- **Given** ユーザーが「Google Calendar から取得」を選択している **When** 対象日を指定（または省略で今日）して「予定を取得」する **Then** BE が MCP（MCPServerStdio）経由で予定を取得し、残り時間・制約が導出されて画面に反映される（または生成リクエストに含まれる）。
- **Given** 上記で導出された自分の状況 **When** 返信案生成を実行する **Then** 既存の生成→チェック→作り直しフローで返信案1件が返る。
- **Given** BE が MCP を利用する **When** 接続する **Then** Pydantic AI の **MCPServerStdio** を使用し、.env の `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` を MCP サブプロセスに渡す。

## 影響範囲

| 領域 | 内容 |
|------|------|
| BE Infrastructure | MCP（MCPServerStdio）接続、Google Calendar 予定取得、残り時間・制約の導出 |
| BE Application | 予定取得ユースケースまたは既存ユースケースからの呼び出し |
| BE Interface | 入力ソース・日付パラメータの追加、DTO/ルートの拡張 |
| FE | 入力ソース選択 UI、カレンダー取得呼び出し、表示の切り替え |
| Docs | functional-design, architecture, glossary, implementation-tasklist |
| 環境変数 | 既存に加え GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET（.env に追加済み） |

## 決定事項（ユーザー回答・2026-02-22）

以下、実装前の質問への回答を記録する。

1. **認証情報の形式**: **B-3**。.env には `GOOGLE_CLIENT_ID` と `GOOGLE_CLIENT_SECRET` のみがあり、JSON ファイルは使わない。そのため、環境変数で Client ID/Secret を直接受け取る MCP を採用する。採用パッケージは **mcp-google**（`npx -y mcp-google`）。@nspady/google-calendar-mcp は `GOOGLE_OAUTH_CREDENTIALS`（JSON ファイルパス）必須のため不採用。
2. **業務時間**: **A**。残り時間の導出で業務時間は **固定 9:00–18:00**（9時間）とする。環境変数やリクエストでは変更しない。
3. **npx パッケージ名**: 上記のとおり **mcp-google** を採用（`npx -y mcp-google`）。ユーザー指定の @nspady/google-calendar-mcp は認証仕様の都合で不採用とし、代替として mcp-google を使用。

## 未決事項・リスク・仮定

- **制約の導出ルール**: 取得した予定を「HH:MM–HH:MM 予定名」形式で連結した文字列を `constraints` に設定する。設計で確定済み。
- **OAuth**: mcp-google も初回はブラウザで認証が必要。未認証時はエラーとして扱い、手動入力にフォールバック可能とする。
- **優先度**: カレンダー取得時は「優先度」は未設定（None）。必要なら FE で取得後に手動で上書き可能とする。
