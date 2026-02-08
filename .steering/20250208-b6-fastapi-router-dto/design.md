# B6: FastAPI ルータ・DTO・入力検証 — 設計

## 方針

- **DDD 境界**: Interface 層のみを追加・変更する。Router は薄く「入力検証 → DTO→Domain 変換 → Usecase 呼び出し → レスポンス DTO」に限定する。
- **契約**: architecture 3.3 に従い、`POST /api/v1/reply-drafts`、リクエストは依頼文＋自分の状況（残り時間・優先度・制約）、レスポンスは返信案リストとする。

## データフロー

1. クライアント → `POST /api/v1/reply-drafts` + JSON body
2. FastAPI: Pydantic でリクエスト検証（422 は自動）
3. ルータ: Request DTO → Domain（RequestText, MySituation）に変換。Domain のバリデーション（依頼文空・残り時間負）は DTO 段階で満たすか、変換時に ValueError を捕捉して 422 にマッピングする。
4. ルータ: Generate/Check/Revise の 3 Adapter をインスタンス化し、`generate_reply_drafts(...)` に渡す。
5. Usecase が list[ReplyDraft] を返す。
6. ルータ: list[ReplyDraft] → Response DTO に変換して 200 で返す。

## API 変更（確定）

- **エンドポイント**: `POST /api/v1/reply-drafts`
- **リクエスト body**（JSON）:
  - `request_text`: string, 必須, 非空
  - `remaining_hours`: number | null, 任意, 0 以上
  - `priority`: "high" | "medium" | "low" | null, 任意
  - `constraints`: string, 任意, デフォルト ""
- **レスポンス**（200）:
  - `drafts`: array of `{ "text": string }`
- **エラー**: 422 バリデーションエラー（FastAPI 標準）。Domain の ValueError（依頼文空・残り時間負）は DTO で弾くか、変換処理で catch して 422 にマッピングする。

## 代替案と採用理由

- **DTO で依頼文を必須・min_length=1**: 依頼文空は FastAPI の 422 で返せる。採用。
- **残り時間を DTO で 0 以上に**: Field(ge=0) で検証。採用。
- **Port を Depends で注入**: 現状はルータ内で Adapter を生成して渡す。B7 でテスト時に overrides を入れる場合は、その時点で Depends に切り替え可能。今回はシンプルにルータ内で生成でよい。

## テスト戦略

- B6 では API の単体テストは行わない（B7 で実施）。手動で `uv run uvicorn ...` 起動と /docs からの実行で受け入れ確認する。
- 必要なら tests/integration に TestClient で POST するテストを B7 で追加する。

## ドキュメント更新方針

- `docs/architecture.md`: 3.3 の「エンドポイント例」を `POST /api/v1/reply-drafts` で確定済みのため、必要に応じてリクエスト/レスポンスの型を一文追記可能。変更最小でよい。
- `docs/implementation-tasklist.md`: B6 を完了にし、完了日・備考を記録。実装サマリー・セクション別進捗・更新履歴を更新。

## 全体タスク反映方針

- implementation-tasklist.md の B6 を完了。総タスク数 24 のうち完了 8、バックエンド 8 のうち完了 6。

---

## 結果と学び（モード3）

- **採用案の妥当性**: DTO で依頼文必須・strip 後空で 422、残り時間 ge=0 で 422 を担保。ルータは薄く DTO→Domain 変換と Usecase 呼び出しのみ。Port はルータ内で Adapter をインスタンス化して渡しており、B7 でテスト時に Depends や overrides を検討可能。
- **想定外**: 特になし。ruff の import 順序修正のみ（--fix で対応済み）。
- **改善点**: なし。契約は architecture 3.3 に反映済み。
