"""返信案生成 API のリクエスト/レスポンス DTO。

architecture 3.3 に従う。依頼文・自分の状況（残り時間・優先度・制約）を入力、
返信案 1 件（draft）を出力する。
"""

from typing import Literal

from pydantic import BaseModel, Field, model_validator

PriorityLiteral = Literal["high", "medium", "low"]
SituationSourceLiteral = Literal["manual", "calendar"]


class GenerateReplyDraftsRequest(BaseModel):
    """POST /api/v1/reply-drafts のリクエスト body。"""

    request_text: str = Field(..., min_length=1, description="依頼文（必須・非空）")
    remaining_hours: float | None = Field(
        default=None,
        ge=0,
        description="残り時間（時間単位）。任意。0以上。situation_source=manual 時のみ使用。",
    )
    priority: PriorityLiteral | None = Field(
        default=None,
        description="優先度（high/medium/low）。任意。",
    )
    constraints: str = Field(
        default="",
        description="制約（自由文）。任意。situation_source=manual 時のみ使用。",
    )
    situation_source: SituationSourceLiteral = Field(
        default="manual",
        description="自分の状況の入力元。manual=手動入力、calendar=Google Calendar から取得。",
    )
    calendar_date: str | None = Field(
        default=None,
        description="対象日（YYYY-MM-DD）。situation_source=calendar 時のみ。省略時は今日。",
    )

    @model_validator(mode="after")
    def strip_request_text(self) -> "GenerateReplyDraftsRequest":
        """依頼文の前後空白を除去し、空の場合はバリデーションエラーとする。"""
        t = self.request_text.strip()
        if not t:
            raise ValueError("依頼文は空にできません")
        return self.model_copy(update={"request_text": t})


class ReplyDraftItem(BaseModel):
    """返信案 1 件（API レスポンス用）。"""

    text: str = Field(..., description="返信案の本文")


class GenerateReplyDraftsResponse(BaseModel):
    """POST /api/v1/reply-drafts のレスポンス body。"""

    draft: ReplyDraftItem = Field(..., description="返信案 1 件")
