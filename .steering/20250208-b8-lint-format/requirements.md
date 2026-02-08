# B8: lint/format（ruff, mypy 等）— 要求

## 背景 / 目的

- バックエンド（FastAPI）の静的解析・フォーマットを整備し、コード品質と一貫性を担保する。
- implementation-tasklist.md の B8「lint/format（ruff, mypy 等）」を完了する。

## スコープ

### やること

- **ruff**: `uv run ruff check .` でリントを実行し、指摘があれば修正する（または設定で許容する理由を残す）。
- **ruff format**: `uv run ruff format .` でフォーマットを適用する。
- **mypy**: `uv run mypy .` で型チェックを実行し、指摘があれば修正する（または設定で許容する理由を残す）。
- 上記を `backend/` で実行し、全通過する状態にする。必要なら pyproject.toml の [tool.ruff] / [tool.mypy] を微調整する。

### やらないこと

- 新機能追加・仕様変更。振る舞い変更は行わない。
- フロントエンドの lint/format（F7 で実施）。

## 受け入れ条件

- **Given** バックエンドのソースが存在する  
  **When** `uv run ruff check .` を backend で実行する  
  **Then** エラー・警告が解消され、終了コード 0 で完了する。

- **Given** 上記と同様  
  **When** `uv run ruff format .` を backend で実行する  
  **Then** フォーマットが適用され、変更が必要な場合は適用済みで終了コード 0 となる。

- **Given** 上記と同様  
  **When** `uv run mypy .` を backend で実行する（対象は src 等、設定に従う）  
  **Then** 型エラーが解消され、終了コード 0 で完了する（ignore_missing_imports 等の既存設定は維持可）。

- 上記実施後も `uv run pytest -q` が全テスト通過することを確認する。

## 影響範囲

- **BE**: backend/ のソース・pyproject.toml（tool.ruff / tool.mypy）。振る舞い変更は最小限（import 順序・空白・型注釈の追加等）。
- **FE**: なし。
- **Docs**: implementation-tasklist.md の B8 を完了に更新。

## 受け入れ条件チェック結果（モード3）

- ruff check: backend で `uv run ruff check .` 実行 → All checks passed（終了コード 0）。
- ruff format: `uv run ruff format .` 実行 → 23 files already formatted / 23 files left unchanged。適用済みで終了コード 0。
- mypy: `uv run mypy .` 実行 → Success: no issues found in 23 source files（終了コード 0）。
- pytest: `uv run pytest -q` で 23 passed。回帰なし。

## 未決事項 / リスク / 仮定

- mypy の対象パスは pyproject.toml またはコマンドで `src` に限定する想定（tests は optional でよい場合あり）。→ 現状 `mypy .` で src + tests を含めても 23 files で Success。
- 既存の ignore_missing_imports = true は維持し、外部ライブラリの型スタブがなくても通過する形でよい。
