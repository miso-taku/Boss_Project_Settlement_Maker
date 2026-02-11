"""返信案生成 API ルータ。

POST /api/v1/reply-drafts: 依頼文＋自分の状況を受け取り、返信案リストを返す。
Port は Depends で注入し、テスト時は dependency_overrides でモックに差し替え可能。
"""

from fastapi import APIRouter, Depends, HTTPException

from settlement_maker.application.generate_reply_drafts import generate_reply_drafts
from settlement_maker.application.ports import (
    CheckReplyDraftsPort,
    GenerateReplyDraftsPort,
    ReviseReplyDraftsPort,
)
from settlement_maker.domain.models import MySituation, Priority, RequestText
from settlement_maker.infrastructure.pydantic_ai_adapters import (
    PydanticAICheckAdapter,
    PydanticAIGenerateAdapter,
    PydanticAIReviseAdapter,
)
from settlement_maker.interface.dto.reply_drafts import (
    GenerateReplyDraftsRequest,
    GenerateReplyDraftsResponse,
    ReplyDraftItem,
)

router = APIRouter(prefix="/reply-drafts", tags=["reply-drafts"])


def get_generate_port() -> GenerateReplyDraftsPort:
    """返信案生成 Port のデフォルト実装（テスト時は dependency_overrides で差し替え可能）。"""
    return PydanticAIGenerateAdapter()


def get_check_port() -> CheckReplyDraftsPort:
    """返信案チェック Port のデフォルト実装。"""
    return PydanticAICheckAdapter()


def get_revise_port() -> ReviseReplyDraftsPort:
    """返信案作り直し Port のデフォルト実装。"""
    return PydanticAIReviseAdapter()


def _request_to_domain(body: GenerateReplyDraftsRequest) -> tuple[RequestText, MySituation]:
    """Request DTO を Domain の RequestText と MySituation に変換する。"""
    request_text = RequestText(value=body.request_text)
    priority = Priority(body.priority) if body.priority is not None else None
    my_situation = MySituation(
        remaining_hours=body.remaining_hours,
        priority=priority,
        constraints=body.constraints or "",
    )
    return request_text, my_situation


@router.post("", response_model=GenerateReplyDraftsResponse)
def post_reply_drafts(
    body: GenerateReplyDraftsRequest,
    generate_port: GenerateReplyDraftsPort = Depends(get_generate_port),
    check_port: CheckReplyDraftsPort = Depends(get_check_port),
    revise_port: ReviseReplyDraftsPort = Depends(get_revise_port),
) -> GenerateReplyDraftsResponse:
    """依頼文と自分の状況から返信案リストを生成する。"""
    try:
        request_text, my_situation = _request_to_domain(body)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    drafts = generate_reply_drafts(
        request_text,
        my_situation,
        generate_port=generate_port,
        check_port=check_port,
        revise_port=revise_port,
    )
    first = drafts[0] if drafts else None
    return GenerateReplyDraftsResponse(
        draft=ReplyDraftItem(text=first.text if first else "")
    )
