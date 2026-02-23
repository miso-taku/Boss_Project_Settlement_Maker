"""AI/MCP 専用ロガーのユニットテスト。"""

import logging

from settlement_maker.infrastructure.ai_mcp_logging import (
    LOGGER_NAME,
    get_ai_mcp_logger,
)


def test_get_ai_mcp_logger_returns_logger_with_correct_name() -> None:
    """get_ai_mcp_logger が専用ロガー名 settlement_maker.ai_mcp のロガーを返す。"""
    logger = get_ai_mcp_logger()
    assert logger.name == LOGGER_NAME


def test_get_ai_mcp_logger_info_does_not_raise() -> None:
    """get_ai_mcp_logger().info() が例外を出さずに完了する。"""
    logger = get_ai_mcp_logger()
    logger.info("test message %s", "payload")


def test_get_ai_mcp_logger_writes_to_file_when_path_set(tmp_path, monkeypatch) -> None:
    """AI_MCP_LOG_PATH を設定したとき、ログがそのファイルに書き込まれる。"""
    log_file = tmp_path / "ai_mcp.log"
    monkeypatch.setenv("AI_MCP_LOG_PATH", str(log_file))

    # モジュールの _handler_configured をリセットし、既存ハンドラを外してから再取得する
    import settlement_maker.infrastructure.ai_mcp_logging as mod

    mod._handler_configured = False
    existing = logging.getLogger(LOGGER_NAME)
    existing.handlers.clear()

    logger = get_ai_mcp_logger()
    logger.info("mcp_tool=list-calendars args=%s result=%s", "{}", "[]")

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "list-calendars" in content
    assert "{}" in content
