"""PydanticAI の構造化出力用 Pydantic モデル。

Domain の ReplyDraft / CheckResult は dataclass のため、
LLM の出力検証用に Infrastructure 層で Pydantic モデルを定義する。
"""

from pydantic import BaseModel, Field


class ReplyDraftSchema(BaseModel):
    """返信案 1 件（LLM 出力用）。"""

    text: str


class ReplyDraftsOutput(BaseModel):
    """返信案リスト（LLM 出力用）。ルートを 1 オブジェクトにしてリストを返させる。"""

    drafts: list[ReplyDraftSchema]


class CheckResultSchema(BaseModel):
    """チェック結果（LLM 出力用）。3項目を10点満点で評価、must_fix / nice_to_have で指摘。"""

    score_1: int = Field(..., ge=0, le=10, description="角の立たなさ 0-10")
    score_2: int = Field(..., ge=0, le=10, description="代替案・確認質問の適切さ 0-10")
    score_3: int = Field(..., ge=0, le=10, description="依頼文・制約準拠 0-10")
    must_fix: list[str] = Field(default_factory=list, description="必須修正（箇条書き）")
    nice_to_have: list[str] = Field(default_factory=list, description="任意改善（箇条書き）")
