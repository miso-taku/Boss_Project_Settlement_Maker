"""FastAPI ルータ。"""

from settlement_maker.interface.routes.reply_drafts import router as reply_drafts_router

__all__ = ["reply_drafts_router"]
