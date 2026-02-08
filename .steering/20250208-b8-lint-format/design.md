# B8: lint/format（ruff, mypy 等）— 設計

## 方針

- **既存設定尊重**: pyproject.toml の [tool.ruff] / [tool.mypy] は既に定義済み。変更は「指摘解消に必要な最小限」に留める。
- **振る舞い不変**: リファクタは import 順・空白・型注釈の追加などに限定し、ロジック変更は行わない。
- **実行場所**: コマンドは backend ディレクトリで実行する（`cd backend && uv run ...`）。mypy の対象は `src` を明示するか、ルートで `src` を指定する。

## データフロー

- 開発者 → `uv run ruff check .` / `uv run ruff format .` / `uv run mypy src` → 指摘があればソース修正 → 再実行で 0 終了。

## 設定（現状）

- **ruff**: target-version = "py310", line-length = 100。lint select = E, F, I, N, W。
- **mypy**: python_version = "3.10", warn_return_any, warn_unused_configs, ignore_missing_imports = true。
- 必要なら mypy に `files = ["src"]` またはコマンドで `uv run mypy src` を採用し、tests を除外または別扱いする。

## 代替案と採用理由

- **ruff のみで mypy は後回し**: B8 は「ruff, mypy 等」とあるため、両方実施する。採用: 両方実行・解消。
- **mypy を strict にする**: 既存が ignore_missing_imports 等で緩めのため、今回は現状のまま通過させる。strict は今後のタスクで検討。採用: 現状設定で通過。

## テスト戦略

- lint/format 適用後、`uv run pytest -q` で全テストが通過することを確認する。リグレッションなし。

## ドキュメント更新方針

- implementation-tasklist.md: B8 を完了にし、完了日・備考（ruff/mypy 実行・解消内容）を記録。実装サマリー・セクション別進捗・更新履歴を更新。

## 全体タスク反映方針

- implementation-tasklist.md の B8 を完了。総タスク数 24 のうち完了 10、バックエンド 8 のうち完了 7（B8 完了後）。

---

## 結果と学び（モード3）

- **採用案の妥当性**: 既存の pyproject.toml の [tool.ruff] / [tool.mypy] をそのまま使用。ruff check / ruff format / mypy はいずれも追加修正なしで通過。ソースは既に B7 時点で整っていた。
- **想定外**: mypy を初回 `uv run mypy src` で実行した際にタイムアウトしたが、再実行で Success。`mypy .` でも 23 source files で Success。
- **改善点**: なし。development-guidelines の「uv run ruff check .」「uv run ruff format .」「uv run mypy .」を backend で実行する運用で完了。
