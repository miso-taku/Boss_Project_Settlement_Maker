# design.md — バックエンド Tidy-First リファクタリング設計

## 方針（DDD 境界・責務分割）

- 既存の DDD レイヤ（domain / application / infrastructure / interface）は変更しない。
- 各レイヤ内の「読む順番」「凝集」「命名」「コメント」のみを整頓する。
- 責務の付け替えや新規 Port の追加は行わない（必要なら別タスクで実施）。

## データフロー

- 変更なし。既存の「依頼文＋自分の状況 → 生成→チェック→作り直し → 返信案 1 件」および「カレンダー → 自分の状況」の流れを維持する。

## API 変更

- なし。エンドポイント・リクエスト/レスポンス・ステータスコードは現状のまま。

## 整頓対象ファイルと適用テクニック（案）

| ファイル | 適用する整頓 |
|----------|----------------|
| `application/generate_reply_drafts.py` | 読む順番（定数は既に冒頭）。必要なら説明変数。 |
| `application/get_calendar_situation.py` | 現状で短いため、大きな変更は不要。 |
| `application/ports.py` | 現状で整理されているため、変更は最小限。 |
| `interface/routes/reply_drafts.py` | ガード節（早期 return）、読む順番（定数 JST を上に）、シンメトリー（手動/カレンダー分岐の並び）、変数宣言と初期化の近接。 |
| `interface/dto/reply_drafts.py` | 冗長コメントがなければそのまま。 |
| `infrastructure/pydantic_ai_adapters.py` | デッドコード削除（print 除去）、読む順番（`_model_name` 等の前提を上に）、説明定数（モデル名）。 |
| `infrastructure/calendar_mcp_adapter.py` | デッドコード削除（デバッグ用 print の削除またはロガー化）、ステートメント小分け・説明変数。 |
| `domain/models.py` | 既に説明定数（CHECK_PASS_THRESHOLD）あり。必要なら読む順番のみ。 |

## テスト戦略

- **Unit / Integration**: 既存の pytest をそのまま実行。リファクタ後も全テストパスを確認する。
- **手動確認**: 必要に応じて POST /api/v1/reply-drafts の 1 リクエストでレスポンス形式が変わっていないことを確認する。

## ドキュメント更新方針

- `./docs/implementation-tasklist.md`: 本作業完了時に「バックエンド Tidy-First リファクタリング」の完了を追記する。
- `./docs/architecture.md` 等の仕様は変更しない。

## 全体タスクリスト反映方針

- `./docs/implementation-tasklist.md` の「振り返り・ドキュメント最終更新」または新規行に、本リファクタリング作業の完了を記載する。

## 代替案

- **A) 一括で複数ファイルをまとめて整頓する**  
  → 採用しない。差分が大きくなりレビューしづらくなるため、ファイル単位で進める。
- **B) print を logging に置き換える**  
  → デバッグ用 print は削除を優先。将来ログが必要なら別タスクで logging を導入する。
- **C) calendar_date をルートで使う実装に変更する**  
  → 本リファクタでは挙動不変のため行わない。仕様上は `calendar_date` が API に存在するが、現状ルートでは「今日」固定で取得している実装であれば、その挙動は変えず、必要なら別チケットで対応する。

---

## 結果と学び（モード3・振り返り）

- **実施内容**: 読む順番（routes: JST をルータ直前に配置、インポートを標準→サードパーティ→ローカルに整理）、デッドコード削除（pydantic_ai_adapters と calendar_mcp_adapter のデバッグ用 print 削除）、説明定数（DEFAULT_OPENAI_MODEL）、シンメトリー（routes の calendar 分岐で target_date を先に設定、system_prompt の不要な空文字列削除）、Why コメント維持（asyncio.to_thread の理由）。
- **受け入れ条件**: `uv run pytest -q` で 31 テストすべてパス。API 契約変更なし。
- **想定外**: なし。ruff の E402/E501 は既存のまま（本作業では新規違反を追加していない）。
- **改善点**: 次回の整頓では、calendar_mcp_adapter のインポート順（JST の後に load_dotenv 等が来ている E402）を解消するか、ruff 設定で E402 を noqa するか検討できる。
