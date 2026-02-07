"""返信案生成ユースケース（生成→チェック→作り直しのオーケストレーション）。

architecture 3.5 に従い、Port 経由で AI エージェントを呼び出す。
最大作り直し回数 N で無限ループを防ぐ。
"""

from settlement_maker.application.ports import (
    CheckReplyDraftsPort,
    GenerateReplyDraftsPort,
    ReviseReplyDraftsPort,
)
from settlement_maker.domain.models import (
    MySituation,
    ReplyDraft,
    RequestText,
)

# 最大作り直し回数（チェック NG 時の revise 呼び出し上限）
MAX_REVISE_ROUNDS = 2


def generate_reply_drafts(
    request_text: RequestText,
    my_situation: MySituation,
    *,
    generate_port: GenerateReplyDraftsPort,
    check_port: CheckReplyDraftsPort,
    revise_port: ReviseReplyDraftsPort,
    max_revise_rounds: int = MAX_REVISE_ROUNDS,
) -> list[ReplyDraft]:
    """依頼文と自分の状況から返信案リストを生成する。

    フロー:
    1. 生成: 依頼文＋自分の状況 → 返信案リスト（初稿）
    2. チェック: 返信案リストをチェック → OK/NG＋指摘
    3. OK ならそのまま返却。NG なら作り直し（最大 max_revise_rounds 回）
    4. 最大回数に達した場合も、その時点の返信案リストを返却する。

    Args:
        request_text: 依頼文
        my_situation: 自分の状況（残り時間・優先度・制約）
        generate_port: 返信案生成 Port（依頼文＋状況 → 返信案リスト）
        check_port: 返信案チェック Port（返信案リスト＋依頼文・状況 → チェック結果）
        revise_port: 返信案作り直し Port（返信案＋指摘＋依頼文・状況 → 修正版リスト）
        max_revise_rounds: チェック NG 時の最大作り直し回数（デフォルト 2）

    Returns:
        返信案のリスト（最終版）
    """
    drafts = generate_port.generate(request_text, my_situation)

    for _ in range(max_revise_rounds):
        check_result = check_port.check(drafts, request_text, my_situation)
        if check_result.ok:
            return drafts
        drafts = revise_port.revise(
            drafts, check_result, request_text, my_situation
        )

    return drafts
