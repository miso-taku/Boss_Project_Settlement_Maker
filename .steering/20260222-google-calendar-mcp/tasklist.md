# タスクリスト（tasklist）

## ステアリング（モード1）

- [x] requirements.md 作成
- [x] design.md 作成
- [x] tasklist.md 作成

## 調査・現状把握

- [x] 採用する Google Calendar MCP パッケージの選定（mcp-google、GOOGLE_CLIENT_ID/SECRET 対応）
- [x] Pydantic AI で MCP ツールを直接呼ぶ（MCPServerStdio.direct_call_tool）で予定取得

## バックエンド

### Domain

- [x] 変更なし（MySituation は既存のまま）

### Application

- [x] 予定取得 Port（GetCalendarSituationPort）の定義
- [x] get_my_situation_from_calendar ユースケース追加
- [x] ドメインテスト: get_calendar_situation のユニットテスト（Port モック）

### Infrastructure

- [x] CalendarMCPAdapter（MCPServerStdio + mcp-google、env に GOOGLE_CLIENT_ID/SECRET）
- [x] 予定取得結果 → remaining_hours / constraints 導出（業務時間 9–18 固定、HH:MM–HH:MM 予定名）
- [ ] 結合テストまたは手動確認（MCP ツール呼び出し・要 npx mcp-google と OAuth）

### Interface

- [x] DTO 拡張: situation_source, calendar_date
- [x] ルート: situation_source=calendar 時に予定取得→MySituation 導出→既存生成フロー
- [x] 統合テスト: situation_source=calendar をモックで検証

### その他 BE

- [x] ruff check（変更ファイルのみ通過）。環境変数は .env から load_dotenv で読み込み

## フロントエンド

- [x] 入力ソース選択 UI（手動 / Google Calendar）
- [x] Google Calendar 選択時の日付入力（初期値は今日）
- [x] API クライアント: request に situation_source, calendar_date を追加
- [x] 型定義の更新（SituationSource, GenerateReplyDraftsRequest）
- [ ] コンポーネントテスト（環境により Jest が EPERM で未実行）

## 結合・統合

- [ ] FE–BE 結合動作確認（手動・カレンダー両方・要 MCP 認証）
- [ ] 受け入れ条件の確認（requirements の Given-When-Then）

## ドキュメント・振り返り

- [x] docs/functional-design.md 更新（入力方法・データフロー）
- [x] docs/architecture.md 更新（3.4.1 MCP・導出ルール・API）
- [x] docs/glossary.md 更新（用語）
- [x] docs/implementation-tasklist.md に S4 追加・完了反映
- [x] ステアリング（モード3）振り返り（design.md に追記）
