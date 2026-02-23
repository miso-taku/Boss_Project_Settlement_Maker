"""PydanticAI Adapter の AI/MCP ログ出力のユニットテスト。"""

from unittest.mock import Mock, patch

from settlement_maker.domain.models import MySituation, RequestText
from settlement_maker.infrastructure.ai_schemas import (
    ReplyDraftSchema,
    ReplyDraftsOutput,
)
from settlement_maker.infrastructure.pydantic_ai_adapters import (
    PydanticAIGenerateAdapter,
)


def test_generate_adapter_logs_prompt_and_output() -> None:
    """Generate 実行時に get_ai_mcp_logger().info が adapter 名・プロンプト・出力で呼ばれる。"""
    adapter = PydanticAIGenerateAdapter()
    adapter._agent = Mock()
    adapter._agent.run_sync.return_value = Mock(
        output=ReplyDraftsOutput(drafts=[ReplyDraftSchema(text="返信案テキスト")])
    )

    with patch(
        "settlement_maker.infrastructure.pydantic_ai_adapters.get_ai_mcp_logger"
    ) as mock_logger_fn:
        mock_log = Mock()
        mock_logger_fn.return_value = mock_log

        result = adapter.generate(
            RequestText("お願いします"),
            MySituation(remaining_hours=None, priority=None, constraints=""),
        )

    assert len(result) == 1
    assert result[0].text == "返信案テキスト"
    mock_log.info.assert_called()
    call_args = mock_log.info.call_args[0]
    assert "ai_adapter=generate" in call_args[0]
    assert "お願いします" in call_args[1]
    assert "返信案テキスト" in call_args[2]
