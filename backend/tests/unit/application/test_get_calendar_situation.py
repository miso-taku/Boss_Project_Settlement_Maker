"""get_my_situation_from_calendar ユースケースのユニットテスト。"""

import asyncio
from datetime import date

from settlement_maker.application.get_calendar_situation import get_my_situation_from_calendar
from settlement_maker.domain.models import MySituation


class MockCalendarPort:
    """固定の MySituation を返すモック。"""

    def __init__(self, situation: MySituation) -> None:
        self.situation = situation

    async def get_my_situation_for_date(self, target_date: date) -> MySituation:
        return self.situation


def test_get_my_situation_from_calendar_returns_port_result():
    """カレンダー Port が返した MySituation がそのまま返る。"""
    expected = MySituation(
        remaining_hours=6.0,
        priority=None,
        constraints="10:00–11:00 定例",
    )
    port = MockCalendarPort(expected)

    async def run() -> MySituation:
        return await get_my_situation_from_calendar(date(2026, 2, 22), calendar_port=port)

    result = asyncio.run(run())
    assert result.remaining_hours == 6.0
    assert result.priority is None
    assert result.constraints == "10:00–11:00 定例"
