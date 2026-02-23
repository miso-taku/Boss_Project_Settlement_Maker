# tasklist.md — バックエンド AI/MCP ログ出力

## 調査・現状把握

- [x] logging の未使用確認、Adapter の呼び出し箇所の確認

## 実装

- [x] ログ設定の追加（logging 設定・FileHandler・専用ロガー名の決定）
- [x] PydanticAI Adapter へのログ出力追加（Generate / Check / Revise の 3 箇所）
- [x] Calendar MCP Adapter へのログ出力追加（list-calendars / list-events の呼び出し前後）

## テスト・品質

- [x] 単体テストの追加・更新（ログが書かれることの検証）
- [x] 既存統合テストの実行確認（`uv run pytest -q`）
- [x] lint/format（`uv run ruff check .` / `uv run ruff format .` / `uv run mypy .`）

## ドキュメント・振り返り

- [x] ./docs 更新（architecture.md 等）
- [x] ./docs/implementation-tasklist.md 更新（B10 追加・完了反映）
- [x] 振り返り（モード3: 受け入れ条件チェック・design.md への結果と学びの追記）
