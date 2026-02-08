# B5: PydanticAI エージェント実装 — 設計

## 方針

- **DDD 境界**: Infrastructure 層が Application の Port（Protocol）を実装する。Domain の型（RequestText, MySituation, ReplyDraft, CheckResult）をそのまま Port の入出力に使い、Infrastructure 内では PydanticAI の構造化出力用に Pydantic モデルのみを追加する（LLM 出力 → Domain 変換）。
- **責務分割**: 各 Adapter は 1 つの Port を実装し、内部で 1 つの PydanticAI Agent を保持。プロンプト・モデルは Adapter 内に閉じる。

## データフロー

- **生成**: RequestText + MySituation → プロンプト文字列組み立て → Agent.run_sync → 構造化出力（例: list[ReplyDraftSchema]）→ list[ReplyDraft] に変換して返す
- **チェック**: drafts + RequestText + MySituation → プロンプト組み立て → Agent.run_sync → CheckResultSchema → CheckResult に変換して返す
- **作り直し**: drafts + CheckResult + RequestText + MySituation → プロンプト組み立て → Agent.run_sync → list[ReplyDraftSchema] → list[ReplyDraft] に変換して返す

## モデル名・環境変数

- **OPENAI_API_KEY**: 必須。PydanticAI（OpenAI プロバイダ）が参照する。
- **OPENAI_MODEL**（任意）: デフォルトは `gpt-4o-mini`。architecture の「gpt-5-mini」は現状 API で一般的でないため、実装時に利用可能なモデル名に合わせる。

## PydanticAI 出力型（Infrastructure 内の Pydantic モデル）

- **返信案リスト用**: `ReplyDraftSchema`（text: str）のリスト。Agent の output_type には `list[ReplyDraftSchema]` または 1 つの「drafts: list[ReplyDraftSchema]」を持つ Pydantic モデルを使う（LLM がリストを返しやすいよう、ルートを 1 オブジェクトにする場合は `ReplyDraftsOutput(drafts: list[ReplyDraftSchema])` とする）。
- **チェック結果用**: `CheckResultSchema(ok: bool, feedback: str)`。Domain の CheckResult と同形なので、Agent 出力をそのまま CheckResult(ok=..., feedback=...) で包む。

## プロンプト方針

- **生成**: 依頼文・自分の状況（残り時間・優先度・制約）を埋め込み、「角の立たない断り・代替案・確認質問・次の一手」を複数パターン（2〜3 件）で返すよう指示。出力は構造化（返信案のリスト）。
- **チェック**: 返信案リスト・依頼文・状況を渡し、「角が立っていないか・代替案が適切か・制約に反していないか」をチェックし、OK なら ok=True / feedback=""、NG なら ok=False / feedback=指摘文 を返すよう指示。
- **作り直し**: 現在の返信案リスト・チェック指摘・依頼文・状況を渡し、指摘を反映して修正した返信案リストを返すよう指示。

## 実装構成

- `infrastructure/ai_schemas.py`: Pydantic モデル（ReplyDraftSchema, ReplyDraftsOutput, CheckResultSchema）。Domain には依存しない（Infrastructure は Domain を import して Port の型で使うが、スキーマは Pydantic のみ）。
- `infrastructure/pydantic_ai_adapters.py`: 3 クラス
  - `PydanticAIGenerateAdapter`: GenerateReplyDraftsPort を実装。生成用 Agent を保持し、generate() で run_sync して list[ReplyDraft] を返す。
  - `PydanticAICheckAdapter`: CheckReplyDraftsPort を実装。チェック用 Agent を保持し、check() で run_sync して CheckResult を返す。
  - `PydanticAIReviseAdapter`: ReviseReplyDraftsPort を実装。作り直し用 Agent を保持し、revise() で run_sync して list[ReplyDraft] を返す。
- モデル名は `os.environ.get("OPENAI_MODEL", "gpt-4o-mini")` で取得。Agent には `f"openai:{model}"` のように渡す。

## 代替案と採用理由

- **1 ファイルに 3 Adapter をまとめる**: プロンプト・エージェント定義が一箇所で見やすく、B5 のスコープで十分。採用。
- **モデルを 3 エージェントで別々に指定する**: 現状は同一モデルでよい。必要になったら環境変数で個別化できる。今回は共通 OPENAI_MODEL で十分。

## テスト戦略

- B5 では結合テストは行わない（B7 で実施）。手動で Adapter をユースケースに注入して動作確認可能であることを確認する程度。
- 必要なら tests/unit/infrastructure でモックなしの軽いインテグレーション（API キーが無い場合はスキップ）を追加可能。今回はスコープ外とする。

## ドキュメント更新方針

- `./docs/implementation-tasklist.md`: B5 を「完了」にし、完了日・備考を記録。実装サマリー・セクション別進捗・更新履歴を更新。
- architecture.md のモデル名記載は既に「gpt-4o-mini 等の可能性あり」となっているため、変更不要。

## 全体タスク反映方針

- implementation-tasklist.md の B5 を完了。総タスク数 24 のうち完了 7、バックエンド 8 のうち完了 5。

---

## 結果と学び（モード3）

- **採用案の妥当性**: 3 Adapter + Pydantic スキーマで、Port の契約を満たしつつ PydanticAI の output_type で構造化出力を得る形にできた。プロンプトは各 Adapter の system_prompt に閉じ、モデル名は環境変数で切り替え可能にした。
- **想定外**: pydantic-ai 1.56.0 には `[openai]` extra がなく、openai を別依存として pyproject.toml に追加した。
- **改善点**: B7 でユースケース＋Adapter の結合テスト（モックまたは API キーありでスキップ可能）を追加するとよい。
