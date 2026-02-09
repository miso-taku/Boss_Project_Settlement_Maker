"""FastAPI アプリケーションのエントリ。

uvicorn settlement_maker.interface.app:app --reload で起動する。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settlement_maker.interface.routes.reply_drafts import router as reply_drafts_router

app = FastAPI(
    title="上司案件・落とし所AIエージェント",
    description="返信案生成 API（依頼文＋自分の状況 → 返信案リスト）",
    version="0.1.0",
)

# CORS 設定（開発環境: Next.js のデフォルトポート 3000 を許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js 開発サーバーのデフォルトポート
        "http://127.0.0.1:3000",  # localhost の別表記
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(reply_drafts_router, prefix="/api/v1")
