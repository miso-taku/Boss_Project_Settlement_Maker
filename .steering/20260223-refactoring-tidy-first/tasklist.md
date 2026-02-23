# tasklist.md — バックエンド Tidy-First リファクタリング

## 調査・現状把握

- [x] リファクタリングスキル（.cursor/refactoring-tidy-first/SKILL.md）の確認
- [x] backend 配下のソース一覧と主要ファイルの読み込み
- [x] 既存テストの実行（`uv run pytest -q` → 31 passed）

## 整頓フェーズ（挙動不変）

### 1. 読む順番・凝集の順番

- [ ] interface/routes/reply_drafts.py: 定数 JST をファイル上部にまとめる
- [ ] interface/routes/reply_drafts.py: インポートと定数の並びを整理
- [ ] infrastructure/pydantic_ai_adapters.py: 前提（モデル名・フォーマット）を冒頭に
- [ ] infrastructure/calendar_mcp_adapter.py: 定数・ヘルパーの並びを確認

### 2. デッドコード削除・シンメトリー統一

- [ ] infrastructure/pydantic_ai_adapters.py: デバッグ用 print を削除
- [ ] infrastructure/calendar_mcp_adapter.py: デバッグ用 print を削除（またはロガー化は別タスク）
- [ ] interface/routes/reply_drafts.py: 手動/カレンダー分岐のシンメトリーを揃える

### 3. ガード節・説明変数・説明定数

- [ ] interface/routes/reply_drafts.py: バリデーション失敗をガード節で早期 return
- [ ] 必要に応じてマジックナンバー/文字列を説明定数に（既存 CHECK_PASS_THRESHOLD 等は維持）

### 4. ステートメント分割・ヘルパー・コメント

- [ ] 長いブロックに空行または見出しコメントを入れる（必要箇所のみ）
- [ ] 冗長なコメントを削除、Why が必要な箇所にのみコメントを残す

### 5. テスト・品質

- [ ] `uv run pytest -q` で全テストパス確認
- [ ] `uv run ruff check .` / `uv run ruff format .` / `uv run mypy .` で静的解析

## ドキュメント・振り返り

- [x] ./docs/implementation-tasklist.md に本作業の完了を反映
- [x] 本ステアリングの tasklist.md を完了で更新
- [x] design.md に結果と学びを追記（モード3）
