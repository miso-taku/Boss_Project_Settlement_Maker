"""POST /api/v1/reply-drafts の統合テスト。

TDD: テストで期待を固定し、Port は Depends で注入（テスト時はモックに差し替え）。
"""

import pytest
from fastapi.testclient import TestClient

from settlement_maker.domain.models import CheckResult, MySituation, ReplyDraft, RequestText
from settlement_maker.interface.app import app
from settlement_maker.interface.routes.reply_drafts import (
    get_check_port,
    get_generate_port,
    get_revise_port,
)


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
        return CheckResult(score_1=9, score_2=9, score_3=9, feedback="")


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
    assert "drafts" in data
    assert len(data["drafts"]) == 1
    assert data["drafts"][0]["text"] == "返信案です。"


def test_post_reply_drafts_minimal_body_returns_200(client_with_mock_ports):
    """依頼文のみで自分の状況は省略しても 200 で返信案1件が返る。"""
    response = client_with_mock_ports.post(
        "/api/v1/reply-drafts",
        json={"request_text": "お願いします"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "drafts" in data
    assert len(data["drafts"]) == 1


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
