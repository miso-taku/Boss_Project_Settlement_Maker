"""AI/MCP 入出力を専用ログファイルに記録するためのロガー。

専用ロガー名 settlement_maker.ai_mcp と FileHandler を用い、
uvicorn 等の既存ログと識別しやすくする。
ログファイルパスは環境変数 AI_MCP_LOG_PATH で指定（未設定時は ai_mcp.log）。
"""

import logging
import os

LOGGER_NAME = "settlement_maker.ai_mcp"
_handler_configured = False


def get_ai_mcp_logger() -> logging.Logger:
    """専用ロガーを返す。初回呼び出し時に FileHandler を追加する。"""
    global _handler_configured
    logger = logging.getLogger(LOGGER_NAME)
    if not _handler_configured:
        path = os.environ.get("AI_MCP_LOG_PATH", "ai_mcp.log")
        dir_path = os.path.dirname(path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        handler = logging.FileHandler(path, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        _handler_configured = True
    return logger
