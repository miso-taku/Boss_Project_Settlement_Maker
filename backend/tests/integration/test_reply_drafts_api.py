"""POST /api/v1/reply-drafts の統合テスト。

TDD: テストで期待を固定し、Port は Depends で注入（テスト時はモックに差し替え）。
"""

from datetime import date

import pytest
from fastapi.testclient import TestClient

from settlement_maker.domain.models import CheckResult, MySituation, ReplyDraft, RequestText
from settlement_maker.interface.app import app
from settlement_maker.interface.routes.reply_drafts import (
    get_calendar_port,
    get_check_port,
    get_generate_port,
    get_revise_port,
)


class MockCalendarPort:
    """カレンダー予定取得を固定の MySituation で返すモック。"""

    async def get_my_situation_for_date(self, target_date: date) -> MySituation:
        return MySituation(
            remaining_hours=5.0,
            priority=None,
            constraints="10:00–11:00 定例\n14:00–15:00 打ち合わせ",
        )


def _sync_mock_calendar_port():
    """TestClient 用に同期的にモックを返す（get_calendar_port は同じインスタンスを返す）。"""
    return MockCalendarPort()


class MockGeneratePort:
    """返信案を固定で1件返すモック。"""

    def generate(
        self,
        request_text: RequestText,
        my_situation: MySituation,
    ) -> list[ReplyDraft]:
        return [ReplyDraft(text="返信案です。")]


class MockCheckPort:
    """常に OK を返すモック。"""

    def check(
        self,
        drafts: list[ReplyDraft],
        request_text: RequestText,
        my_situation: MySituation,
    ) -> CheckResult:
        return CheckResult(score_1=9, score_2=9, score_3=9, must_fix=(), nice_to_have=())


class MockRevisePort:
    """渡された草案をそのまま返すモック。"""

    def revise(
        self,
        drafts: list[ReplyDraft],
        check_result: CheckResult,
        request_text: RequestText,
        my_situation: MySituation,
    ) -> list[ReplyDraft]:
        return drafts


@pytest.fixture
def client_with_mock_ports():
    """Port をモックに差し替えた TestClient。"""
    app.dependency_overrides[get_generate_port] = lambda: MockGeneratePort()
    app.dependency_overrides[get_check_port] = lambda: MockCheckPort()
    app.dependency_overrides[get_revise_port] = lambda: MockRevisePort()
    app.dependency_overrides[get_calendar_port] = _sync_mock_calendar_port
    try:
        with TestClient(app) as c:
            yield c
    finally:
        app.dependency_overrides.clear()


def test_post_reply_drafts_returns_200_and_drafts(client_with_mock_ports):
    """正常系: 依頼文＋自分の状況を送ると 200 で返信案1件が返る。"""
    response = client_with_mock_ports.post(
        "/api/v1/reply-drafts",
        json={
            "request_text": "明日までに仕上げてほしい",
            "remaining_hours": 1.5,
            "priority": "high",
            "constraints": "無理なら断りたい",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "draft" in data
    assert "drafts" not in data
    assert data["draft"]["text"] == "返信案です。"


def test_post_reply_drafts_minimal_body_returns_200(client_with_mock_ports):
    """依頼文のみで自分の状況は省略しても 200 で返信案1件が返る。"""
    response = client_with_mock_ports.post(
        "/api/v1/reply-drafts",
        json={"request_text": "お願いします"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "draft" in data
    assert data["draft"]["text"]


def test_post_reply_drafts_empty_request_text_returns_422(client_with_mock_ports):
    """依頼文が空のとき 422 が返る。"""
    response = client_with_mock_ports.post(
        "/api/v1/reply-drafts",
        json={"request_text": ""},
    )
    assert response.status_code == 422


def test_post_reply_drafts_whitespace_only_request_text_returns_422(client_with_mock_ports):
    """依頼文が空白のみのとき 422 が返る。"""
    response = client_with_mock_ports.post(
        "/api/v1/reply-drafts",
        json={"request_text": "   \n  "},
    )
    assert response.status_code == 422


def test_post_reply_drafts_negative_remaining_hours_returns_422(client_with_mock_ports):
    """残り時間が負のとき 422 が返る。"""
    response = client_with_mock_ports.post(
        "/api/v1/reply-drafts",
        json={
            "request_text": "お願いします",
            "remaining_hours": -1.0,
        },
    )
    assert response.status_code == 422


def test_post_reply_drafts_missing_request_text_returns_422(client_with_mock_ports):
    """依頼文が未指定のとき 422 が返る。"""
    response = client_with_mock_ports.post(
        "/api/v1/reply-drafts",
        json={},
    )
    assert response.status_code == 422


def test_options_reply_drafts_returns_200(client_with_mock_ports):
    """CORS プリフライトリクエスト（OPTIONS）が 200 で返る。"""
    response = client_with_mock_ports.options(
        "/api/v1/reply-drafts",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_post_reply_drafts_situation_source_calendar_returns_200(client_with_mock_ports):
    """situation_source=calendar のとき現在日付でカレンダー Port を呼び返信案が返る。"""
    response = client_with_mock_ports.post(
        "/api/v1/reply-drafts",
        json={
            "request_text": "今日中にお願いします",
            "situation_source": "calendar",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "draft" in data
    assert data["draft"]["text"] == "返信案です。"
