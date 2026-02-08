"""依頼文・自分の状況・返信案のドメインモデルのユニットテスト。"""

import pytest

from settlement_maker.domain.models import (
    CheckResult,
    MySituation,
    Priority,
    ReplyDraft,
    RequestText,
)


class TestPriority:
    """Priority 列挙のテスト。"""

    def test_has_three_levels(self) -> None:
        assert Priority.HIGH.value == "high"
        assert Priority.MEDIUM.value == "medium"
        assert Priority.LOW.value == "low"


class TestRequestText:
    """RequestText 値オブジェクトのテスト。"""

    def test_creates_with_non_empty_text(self) -> None:
        r = RequestText("今日中に仕上げて")
        assert r.value == "今日中に仕上げて"
        assert str(r) == "今日中に仕上げて"

    def test_rejects_empty_string(self) -> None:
        with pytest.raises(ValueError, match="依頼文は空にできません"):
            RequestText("")

    def test_rejects_whitespace_only(self) -> None:
        with pytest.raises(ValueError, match="依頼文は空にできません"):
            RequestText("   \n\t  ")

    def test_accepts_text_with_leading_trailing_spaces(self) -> None:
        r = RequestText("  依頼内容  ")
        assert r.value == "  依頼内容  "


class TestMySituation:
    """MySituation 値オブジェクトのテスト。"""

    def test_creates_with_all_fields(self) -> None:
        s = MySituation(
            remaining_hours=1.5,
            priority=Priority.HIGH,
            constraints="NGワードなし",
        )
        assert s.remaining_hours == 1.5
        assert s.priority == Priority.HIGH
        assert s.constraints == "NGワードなし"
        assert "残り時間" in str(s)
        assert "優先度" in str(s)
        assert "制約" in str(s)

    def test_creates_with_optional_none(self) -> None:
        s = MySituation(
            remaining_hours=None,
            priority=None,
            constraints="",
        )
        assert s.remaining_hours is None
        assert s.priority is None
        assert s.constraints == ""
        assert str(s) == "(未入力)"

    def test_rejects_negative_remaining_hours(self) -> None:
        with pytest.raises(ValueError, match="残り時間は0以上"):
            MySituation(remaining_hours=-1.0, priority=None, constraints="")

    def test_accepts_zero_remaining_hours(self) -> None:
        s = MySituation(remaining_hours=0.0, priority=None, constraints="")
        assert s.remaining_hours == 0.0


class TestReplyDraft:
    """ReplyDraft 値オブジェクトのテスト。"""

    def test_creates_with_text(self) -> None:
        d = ReplyDraft(text="承知しました。明日までに提出します。")
        assert d.text == "承知しました。明日までに提出します。"
        assert str(d) == "承知しました。明日までに提出します。"

    def test_accepts_empty_text(self) -> None:
        d = ReplyDraft(text="")
        assert d.text == ""


class TestCheckResult:
    """CheckResult 値オブジェクトのテスト。"""

    def test_creates_ok_when_all_scores_at_least_8(self) -> None:
        c = CheckResult(score_1=9, score_2=9, score_3=9, feedback="")
        assert c.ok is True
        assert c.feedback == ""

    def test_creates_ok_when_all_scores_exactly_8(self) -> None:
        c = CheckResult(score_1=8, score_2=8, score_3=8, feedback="")
        assert c.ok is True

    def test_creates_ng_when_any_score_below_8(self) -> None:
        c = CheckResult(score_1=7, score_2=8, score_3=8, feedback="表現を柔らかくしてください")
        assert c.ok is False
        assert c.feedback == "表現を柔らかくしてください"

    def test_rejects_score_below_0(self) -> None:
        with pytest.raises(ValueError, match="score_1 は0〜10の範囲で指定してください"):
            CheckResult(score_1=-1, score_2=8, score_3=8, feedback="")

    def test_rejects_score_above_10(self) -> None:
        with pytest.raises(ValueError, match="score_3 は0〜10の範囲で指定してください"):
            CheckResult(score_1=8, score_2=8, score_3=11, feedback="")
