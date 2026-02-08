# B6: FastAPI ルータ・DTO・入力検証 — 要求

## 背景 / 目的

- B4 で返信案生成ユースケース、B5 で PydanticAI アダプターを実装済み。これらを HTTP API として公開する。
- 本タスクでは **Interface 層** で POST 返信案生成 API を実装し、依頼文＋自分の状況を受け取り、返信案リストを返す契約を確定する。

## スコープ

### やること

- **DTO**: リクエスト（依頼文・残り時間・優先度・制約）とレスポンス（返信案リスト）の Pydantic モデルを定義する。
- **入力検証**: 依頼文は必須・非空。残り時間は 0 以上（任意）。優先度は high/medium/low のいずれか（任意）。制約は任意（空文字可）。
- **FastAPI ルータ**: `POST /api/v1/reply-drafts` を定義し、入力検証 → DTO→Domain 変換 → Usecase 呼び出し → レスポンス DTO 返却を行う。
- **アプリケーションのエントリ**: FastAPI アプリ（`app`）を作成し、上記ルータをマウントする。uvicorn で `settlement_maker.interface.app:app` として起動可能にする。

### やらないこと

- 認証・認可（本プロダクトではなし）。
- 履歴保存・DB（初版ではなし）。
- B7 で実施するドメイン/アプリケーション/API のテスト（本タスクでは API の手動確認まで）。

## 受け入れ条件

- **Given** 依頼文（非空）・自分の状況（残り時間・優先度・制約は任意）を JSON で POST する  
  **When** `POST /api/v1/reply-drafts` を呼ぶ  
  **Then** 200 で返信案のリスト（各要素に `text`）が返る。

- **Given** 依頼文が空または未指定  
  **When** `POST /api/v1/reply-drafts` を呼ぶ  
  **Then** 422 Unprocessable Entity でバリデーションエラーが返る。

- **Given** 残り時間が負の数  
  **When** `POST /api/v1/reply-drafts` を呼ぶ  
  **Then** 422 でバリデーションエラーが返る。

- `uv run uvicorn settlement_maker.interface.app:app --reload` でアプリが起動し、OpenAPI ドキュメント（/docs）で上記エンドポイントが確認できる。

## 影響範囲

- **BE**: interface/dto（新規）、interface/routes（新規 reply_drafts ルータ）、interface/app.py（新規）。Domain/Application/Infrastructure は変更しない。
- **FE**: なし（契約のみ確定）。
- **API**: 新規エンドポイント `POST /api/v1/reply-drafts`。
- **Docs**: architecture.md の API 契約（エンドポイント名）が確定済みのため、必要なら「確定した契約」として追記。implementation-tasklist.md を B6 完了で更新。

## 受け入れ条件チェック結果（モード3）

- 依頼文＋自分の状況を POST して 200 で返信案リストが返る: 実装済み（ルータ＋Usecase＋Adapter 連携）。
- 依頼文が空または未指定で 422: DTO の min_length=1 と model_validator（strip 後空で ValueError）で担保。
- 残り時間が負で 422: DTO の Field(ge=0) で担保。
- uvicorn で app 起動・/docs でエンドポイント確認: interface/app.py で `app` を定義し、`uv run uvicorn settlement_maker.interface.app:app --reload` で起動可能。

## 未決事項 / リスク / 仮定

- タイムアウト・レート制限は本タスクでは設けない（I1 や今後の非機能で検討可能）。
- Port の注入は「ルータ内で Adapter をインスタンス化して Usecase に渡す」でよい（テスト時は B7 でモックや overrides を検討）。
