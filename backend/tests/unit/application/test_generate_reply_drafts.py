"""generate_reply_drafts ユースケースのユニットテスト。

Port をモックに差し替え、生成→チェック→作り直しのオーケストレーションを検証する。
"""

from settlement_maker.application.generate_reply_drafts import generate_reply_drafts
from settlement_maker.domain.models import (
    CheckResult,
    MySituation,
    Priority,
    ReplyDraft,
    RequestText,
)


class MockGeneratePort:
    """返信案を固定で1件返すモック。"""

    def __init__(self, drafts: list[ReplyDraft] | None = None) -> None:
        self.drafts = drafts or [ReplyDraft(text="初稿")]

    def generate(
        self,
        request_text: RequestText,
        my_situation: MySituation,
    ) -> list[ReplyDraft]:
        return list(self.drafts)


class MockCheckPort:
    """チェック結果を制御するモック。"""

    def __init__(self, results: list[CheckResult]) -> None:
        self.results = list(results)
        self.call_count = 0

    def check(
        self,
        drafts: list[ReplyDraft],
        request_text: RequestText,
        my_situation: MySituation,
    ) -> CheckResult:
        idx = min(self.call_count, len(self.results) - 1)
        self.call_count += 1
        return self.results[idx]


class MockRevisePort:
    """作り直し結果を制御するモック。"""

    def __init__(self, revised: list[ReplyDraft]) -> None:
        self.revised = list(revised)
        self.call_count = 0

    def revise(
        self,
        drafts: list[ReplyDraft],
        check_result: CheckResult,
        request_text: RequestText,
        my_situation: MySituation,
    ) -> list[ReplyDraft]:
        self.call_count += 1
        return list(self.revised)


def test_generate_reply_drafts_returns_drafts_when_check_ok_first_time() -> None:
    """チェックが初回で OK のとき、generate の結果がそのまま返る。revise は呼ばれない。"""
    request_text = RequestText("お願いします")
    my_situation = MySituation(remaining_hours=None, priority=None, constraints="")
    generate_port = MockGeneratePort()
    check_port = MockCheckPort(
        [CheckResult(score_1=9, score_2=9, score_3=9, must_fix=(), nice_to_have=())]
    )
    revise_port = MockRevisePort([ReplyDraft(text="revised")])

    result = generate_reply_drafts(
        request_text,
        my_situation,
        generate_port=generate_port,
        check_port=check_port,
        revise_port=revise_port,
        max_revise_rounds=2,
    )

    assert len(result) == 1
    assert result[0].text == "初稿"
    assert check_port.call_count == 1
    assert revise_port.call_count == 0


def test_generate_reply_drafts_calls_revise_when_check_ng_then_ok() -> None:
    """チェックが 1 回 NG のあと OK のとき、revise が 1 回呼ばれ、その結果が返る。"""
    request_text = RequestText("お願いします")
    my_situation = MySituation(remaining_hours=1.0, priority=Priority.HIGH, constraints="")
    generate_port = MockGeneratePort()
    check_port = MockCheckPort(
        [
            CheckResult(
                score_1=7,
                score_2=8,
                score_3=8,
                must_fix=("修正して",),
                nice_to_have=(),
            ),
            CheckResult(score_1=9, score_2=9, score_3=9, must_fix=(), nice_to_have=()),
        ]
    )
    revised = [ReplyDraft(text="修正版")]
    revise_port = MockRevisePort(revised)

    result = generate_reply_drafts(
        request_text,
        my_situation,
        generate_port=generate_port,
        check_port=check_port,
        revise_port=revise_port,
        max_revise_rounds=2,
    )

    assert len(result) == 1
    assert result[0].text == "修正版"
    assert check_port.call_count == 2
    assert revise_port.call_count == 1


def test_generate_reply_drafts_stops_after_max_revise_rounds() -> None:
    """チェックがずっと NG でもスコアが改善するとき、max_revise_rounds 回 revise が呼ばれ、最後の結果が返る。"""
    request_text = RequestText("お願い")
    my_situation = MySituation(remaining_hours=None, priority=None, constraints="")
    generate_port = MockGeneratePort()
    # スコア合計が毎回改善するようにする（22 → 23）。改善なしで終了しない
    check_port = MockCheckPort(
        [
            CheckResult(score_1=6, score_2=8, score_3=8, must_fix=("1",), nice_to_have=()),
            CheckResult(score_1=7, score_2=8, score_3=8, must_fix=("2",), nice_to_have=()),
            CheckResult(score_1=8, score_2=8, score_3=8, must_fix=(), nice_to_have=()),
        ]
    )
    revised = [ReplyDraft(text="最終版")]
    revise_port = MockRevisePort(revised)

    result = generate_reply_drafts(
        request_text,
        my_situation,
        generate_port=generate_port,
        check_port=check_port,
        revise_port=revise_port,
        max_revise_rounds=2,
    )

    assert len(result) == 1
    assert result[0].text == "最終版"
    assert check_port.call_count == 2  # max_revise_rounds=2 でループ 2 回（各ループで check 1 回）
    assert revise_port.call_count == 2


def test_generate_reply_drafts_stops_when_score_sum_does_not_improve() -> None:
    """スコア合計が改善しない場合、作り直しを打ち切ってその時点の返信案を返す。"""
    request_text = RequestText("お願い")
    my_situation = MySituation(remaining_hours=None, priority=None, constraints="")
    generate_port = MockGeneratePort()
    # 1回目: 22点 → 2回目: 21点（悪化）→ 改善なしで終了
    check_port = MockCheckPort(
        [
            CheckResult(score_1=8, score_2=7, score_3=7, must_fix=("a",), nice_to_have=()),
            CheckResult(score_1=7, score_2=7, score_3=7, must_fix=("b",), nice_to_have=()),
        ]
    )
    revise_port = MockRevisePort([ReplyDraft(text="修正版")])

    result = generate_reply_drafts(
        request_text,
        my_situation,
        generate_port=generate_port,
        check_port=check_port,
        revise_port=revise_port,
        max_revise_rounds=2,
    )

    # 1回目のチェック後、revise で「修正版」になる。2回目のチェックで 21 点（改善なし）→ 終了
    assert len(result) == 1
    assert result[0].text == "修正版"
    assert check_port.call_count == 2
    assert revise_port.call_count == 1


def test_generate_reply_drafts_zero_max_revise_rounds_returns_initial_drafts() -> None:
    """max_revise_rounds=0 のとき、チェック NG でも revise は呼ばれず初回生成結果が返る。"""
    request_text = RequestText("お願い")
    my_situation = MySituation(remaining_hours=None, priority=None, constraints="")
    generate_port = MockGeneratePort()
    check_port = MockCheckPort(
        [CheckResult(score_1=6, score_2=7, score_3=8, must_fix=("要修正",), nice_to_have=())]
    )
    revise_port = MockRevisePort([ReplyDraft(text="revised")])

    result = generate_reply_drafts(
        request_text,
        my_situation,
        generate_port=generate_port,
        check_port=check_port,
        revise_port=revise_port,
        max_revise_rounds=0,
    )

    assert len(result) == 1
    assert result[0].text == "初稿"
    assert check_port.call_count == 0  # max_revise_rounds=0 なので check は呼ばれない
    assert revise_port.call_count == 0
