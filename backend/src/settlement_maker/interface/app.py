"""FastAPI アプリケーションのエントリ。

uvicorn settlement_maker.interface.app:app --reload で起動する。
"""

from fastapi import FastAPI

from settlement_maker.interface.routes.reply_drafts import router as reply_drafts_router

app = FastAPI(
    title="上司案件・落とし所AIエージェント",
    description="返信案生成 API（依頼文＋自分の状況 → 返信案リスト）",
    version="0.1.0",
)

app.include_router(reply_drafts_router, prefix="/api/v1")
