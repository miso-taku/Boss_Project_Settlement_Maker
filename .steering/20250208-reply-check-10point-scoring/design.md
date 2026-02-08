# 仕様変更: 返信案チェックを10点満点×3項目・全て8以上でOK — 設計

## 方針

- **契約は維持**: `POST /api/v1/reply-drafts` のリクエスト/レスポンスは変更しない。チェックはバックエンド内部の判定ロジックのみ変更する。
- **Domain**: CheckResult を「ok + feedback」から「score_1, score_2, score_3, feedback」にし、ok は「全スコア >= 8」の派生プロパティとする。スコアは 0〜10 の整数で検証する。
- **Infrastructure**: CheckResultSchema を score_1, score_2, score_3, feedback の出力にし、チェックエージェントのプロンプトで「3項目を10点満点で付け、全て8以上で合格」と指示する。

## データフロー

- 変更なし。生成 → チェック（**3項目を0〜10でスコア付け、全て8以上ならOK**）→ NG なら作り直し（feedback を参照）→ 最大 N 回繰り返し。

## API 変更

- **なし**。エンドポイント・リクエスト・レスポンスは変更しない。

## 変更内容（箇条書き）

### Domain (domain/models.py)

- **CheckResult**
  - 削除: `ok: bool`（コンストラクタ引数から削除）
  - 追加: `score_1: int`（角の立たなさ 0-10）, `score_2: int`（代替案・確認質問 0-10）, `score_3: int`（依頼文・制約準拠 0-10）
  - 維持: `feedback: str`
  - 追加: `@property def ok(self) -> bool`: `score_1 >= 8 and score_2 >= 8 and score_3 >= 8`
  - `__post_init__`: 各 score が 0〜10 の範囲であることを検証。範囲外なら ValueError。

### Infrastructure (ai_schemas.py)

- **CheckResultSchema**
  - 削除: `ok: bool`
  - 追加: `score_1: int`, `score_2: int`, `score_3: int`（0-10。Pydantic で Field(ge=0, le=10) を付与）
  - 維持: `feedback: str = ""`

### Infrastructure (pydantic_ai_adapters.py)

- **PydanticAICheckAdapter**
  - システムプロンプト: 「3項目をそれぞれ10点満点で評価する。1) 角が立っていないか、2) 代替案・確認質問が適切か、3) 依頼文・制約に反していないか。各スコアは0〜10の整数で返す。3項目すべてが8以上なら合格、1つでも8未満なら feedback に改善点を具体的に書く。」
  - 出力: CheckResultSchema（score_1, score_2, score_3, feedback）
  - マッピング: `CheckResult(score_1=output.score_1, score_2=output.score_2, score_3=output.score_3, feedback=output.feedback or "")`。ok は Domain のプロパティで算出。

### Application

- **generate_reply_drafts.py**: 変更なし。`check_result.ok` と `check_result.feedback` の参照はそのまま。
- **ports.py**: 変更なし。CheckResult の型は Domain に従う。

### テスト

- **tests/unit/domain/test_models.py**
  - CheckResult: `ok=True` の例を `score_1=9, score_2=9, score_3=9, feedback=""` に変更。`ok=False` の例を `score_1=7, score_2=8, score_3=8, feedback="..."` 等に変更。スコア範囲外で ValueError のテストを追加。
- **tests/unit/application/test_generate_reply_drafts.py**
  - MockCheckPort に渡す CheckResult: OK は `CheckResult(score_1=9, score_2=9, score_3=9, feedback="")`、NG は `CheckResult(score_1=7, score_2=8, score_3=8, feedback="修正して")` 等に変更。
- **tests/integration/test_reply_drafts_api.py**
  - MockCheckPort の戻り値: `CheckResult(score_1=9, score_2=9, score_3=9, feedback="")` に変更。

### 永続ドキュメント

- **architecture.md**: 3.5 の「返信案チェックエージェント」の説明に「3項目を10点満点で評価し、全て8以上で合格。1つでも8未満ならNGとし、feedback で改善点を返す」を追記。
- **functional-design.md**: データフローまたはチェックの説明に「チェックは3項目を10点満点で評価し、全て8以上でOK」を追記。
- **glossary.md**: 「チェック結果」の定義に「3項目のスコア（各0〜10）と feedback。合格は全スコア8以上」を追記。
- **implementation-tasklist.md**: 仕様変更セクションに本タスクを追加し、完了時にチェックする。

## 代替案と採用理由

- **ok をコンストラクタ引数に残し、スコアも持つ**: 冗長で不整合の余地がある。ok はスコアから一意に決まるため派生プロパティとする。採用: ok はプロパティ。
- **スコアをリストで持つ**: 可読性とプロンプトの「1〜3」と対応させるため、score_1, score_2, score_3 の明示を採用。

## テスト戦略

- Domain: CheckResult の作成（OK/NG）、スコア範囲外で ValueError。
- Application: 既存のモックを新 CheckResult の形に合わせ、オーケストレーションは変更なしで通過させる。
- Integration: モックの CheckResult を新形式に合わせる。
- 既存の ruff / mypy を維持。

## ドキュメント更新方針

- architecture.md, functional-design.md, glossary.md の該当箇所に「10点満点×3項目・全て8以上で合格」を明記。
- implementation-tasklist.md に本仕様変更タスクを追加。

## 全体タスクリスト反映方針

- implementation-tasklist.md の「6. 仕様変更」に「返信案チェックを10点満点×3項目・全て8以上でOK」を追加し、完了時にチェックする。

---

## 振り返り（モード3）

- **採用案の妥当性**: ok をスコアから派生させることで、不整合がなくなり、テストも「スコアで OK/NG を表現」する形で明確になった。
- **想定外**: なし。既存の application / integration は CheckResult の生成箇所のみ変更で対応できた。
- **改善点**: ruff の E501/E402 は本ファイルで既存のため、本タスクでは追加した行のみ 100 文字以内に収めた。プロジェクト全体の ruff 通過は別タスクで対応可能。
