"""AI 呼び出し Port（抽象）。

Application 層から AI エージェントを呼び出すための抽象。
Infrastructure が各 PydanticAI エージェントを Adapter として実装する。
architecture 3.5（生成→チェック→作り直し）に従う。
"""

from datetime import date
from typing import Protocol

from settlement_maker.domain.models import (
    CheckResult,
    MySituation,
    ReplyDraft,
    RequestText,
)


class GetCalendarSituationPort(Protocol):
    """カレンダー予定取得 Port。対象日 → 自分の状況（残り時間・制約を導出）。"""

    async def get_my_situation_for_date(self, target_date: date) -> MySituation:
        """指定日の予定を取得し、残り時間・制約を導出して MySituation を返す。"""
        ...


class GenerateReplyDraftsPort(Protocol):
    """返信案生成 Port。依頼文＋自分の状況 → 返信案リスト（初稿）。"""

    def generate(
        self,
        request_text: RequestText,
        my_situation: MySituation,
    ) -> list[ReplyDraft]:
        """返信案リスト（初稿）を生成する。"""
        ...


class CheckReplyDraftsPort(Protocol):
    """返信案チェック Port。返信案リスト＋依頼文・状況 → チェック結果。"""

    def check(
        self,
        drafts: list[ReplyDraft],
        request_text: RequestText,
        my_situation: MySituation,
    ) -> CheckResult:
        """返信案リストをチェックし、OK/NG と指摘を返す。"""
        ...


class ReviseReplyDraftsPort(Protocol):
    """返信案作り直し Port。返信案＋チェック指摘＋依頼文・状況 → 返信案リスト（修正版）。"""

    def revise(
        self,
        drafts: list[ReplyDraft],
        check_result: CheckResult,
        request_text: RequestText,
        my_situation: MySituation,
    ) -> list[ReplyDraft]:
        """チェック指摘を反映して返信案リストを修正する。"""
        ...
