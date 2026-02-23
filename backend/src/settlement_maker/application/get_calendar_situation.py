"""カレンダーから自分の状況を取得するユースケース。

対象日の予定を Port 経由で取得し、残り時間・制約を導出した MySituation を返す。
"""

from datetime import date

from settlement_maker.application.ports import GetCalendarSituationPort
from settlement_maker.domain.models import MySituation


async def get_my_situation_from_calendar(
    target_date: date,
    *,
    calendar_port: GetCalendarSituationPort,
) -> MySituation:
    """指定日のカレンダー予定から自分の状況（残り時間・制約）を導出する。

    Args:
        target_date: 予定を取得する日付。
        calendar_port: カレンダー予定取得 Port。

    Returns:
        導出された MySituation（remaining_hours, constraints は予定から計算。priority は None）。
    """
    return await calendar_port.get_my_situation_for_date(target_date)
