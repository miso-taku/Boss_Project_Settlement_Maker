"""PydanticAI を用いた Port の実装（生成・チェック・作り直しの 3 Adapter）。

Application 層の Port を満たし、各エージェントで run_sync して Domain 型で返す。
モデル名は環境変数 OPENAI_MODEL（デフォルト gpt-5-mini）で指定。OPENAI_API_KEY は .env から読み込む必要あり。
"""

import os

from dotenv import load_dotenv

# .env から環境変数を読み込む
load_dotenv()

from pydantic_ai import Agent

from settlement_maker.application.ports import (
    CheckReplyDraftsPort,
    GenerateReplyDraftsPort,
    ReviseReplyDraftsPort,
)
from settlement_maker.domain.models import (
    CheckResult,
    MySituation,
    ReplyDraft,
    RequestText,
)
from settlement_maker.infrastructure.ai_schemas import (
    CheckResultSchema,
    ReplyDraftsOutput,
)


def _model_name() -> str:
    return os.environ.get("OPENAI_MODEL", "gpt-5-mini")


def _format_situation(my_situation: MySituation) -> str:
    parts = []
    if my_situation.remaining_hours is not None:
        parts.append(f"残り時間: {my_situation.remaining_hours} 時間")
    if my_situation.priority is not None:
        parts.append(f"優先度: {my_situation.priority.value}")
    if my_situation.constraints.strip():
        parts.append(f"制約: {my_situation.constraints}")
    return "\n".join(parts) if parts else "（未入力）"


class PydanticAIGenerateAdapter(GenerateReplyDraftsPort):
    """返信案生成 Port の PydanticAI 実装。依頼文＋自分の状況 → 返信案リスト（初稿）。"""

    def __init__(self) -> None:
        model = f"openai:{_model_name()}"
        self._agent = Agent(
            model,
            output_type=ReplyDraftsOutput,
            system_prompt=(
                "あなたは上司や依頼者への返信案を生成するアシスタントです。"
                "依頼文と自分の状況（残り時間・優先度・制約）に基づき、"
                "角の立たない断り・代替案・確認質問・次の一手を1件の返信案として返してください。"
                "返信案は丁寧で実用的な文にし、制約に反しないようにしてください。"
                "返信案は200文字程度で生成してください。"
                "出力は必ず drafts に返信案1件のリスト（各要素は text）を含む JSON 形式にすること。"
                "",
            ),
        )

    def generate(
        self,
        request_text: RequestText,
        my_situation: MySituation,
    ) -> list[ReplyDraft]:
        user_prompt = (
            "【依頼文】\n"
            f"{request_text.value}\n\n"
            "【自分の状況】\n"
            f"{_format_situation(my_situation)}\n\n"
            "上記に基づき、返信案を1件生成してください。"
        )
        result = self._agent.run_sync(user_prompt)
        output: ReplyDraftsOutput = result.output
        print(f"generate output: {output}")
        print(f"generate output.drafts: {output.drafts}")
        return [ReplyDraft(text=d.text) for d in output.drafts]


class PydanticAICheckAdapter(CheckReplyDraftsPort):
    """返信案チェック Port の PydanticAI 実装。返信案リスト＋依頼文・状況 → チェック結果。"""

    def __init__(self) -> None:
        model = f"openai:{_model_name()}"
        self._agent = Agent(
            model,
            output_type=CheckResultSchema,
            system_prompt=(
                "あなたは返信案の品質をチェックするアシスタントです。"
                "与えられた返信案について、以下の3項目をそれぞれ10点満点（0〜10の整数）で評価してください。"
                "1) 角が立っていないか（丁寧さ・角の立たなさ）"
                "2) 代替案・確認質問が適切か"
                "3) 依頼文・制約に反していないか"
                "3項目すべてが8以上なら合格です。"
                "1つでも8未満の項目があれば、must_fix に必須で直すべき点を箇条書きで、nice_to_have にあればよい改善を箇条書きで書いてください。"
                "出力は score_1, score_2, score_3（各0〜10）と must_fix（文字列のリスト）, nice_to_have（文字列のリスト）の JSON にしてください。"
            ),
        )

    def check(
        self,
        drafts: list[ReplyDraft],
        request_text: RequestText,
        my_situation: MySituation,
    ) -> CheckResult:
        drafts_text = "\n".join(f"- {d.text}" for d in drafts)
        user_prompt = (
            "【依頼文】\n"
            f"{request_text.value}\n\n"
            "【自分の状況】\n"
            f"{_format_situation(my_situation)}\n\n"
            "【返信案リスト】\n"
            f"{drafts_text}\n\n"
            "上記の返信案を、1)角の立たなさ 2)代替案・確認質問の適切さ 3)依頼文・制約準拠 の3項目で"
            "それぞれ0〜10の整数で採点し、8未満の項目があれば feedback に改善点を書いてください。"
        )
        result = self._agent.run_sync(user_prompt)
        output: CheckResultSchema = result.output
        return CheckResult(
            score_1=output.score_1,
            score_2=output.score_2,
            score_3=output.score_3,
            must_fix=tuple(output.must_fix or []),
            nice_to_have=tuple(output.nice_to_have or []),
        )


class PydanticAIReviseAdapter(ReviseReplyDraftsPort):
    """返信案作り直し Port の PydanticAI 実装。
    返信案＋指摘＋依頼文・状況 → 返信案リスト（修正版）。"""

    def __init__(self) -> None:
        model = f"openai:{_model_name()}"
        self._agent = Agent(
            model,
            output_type=ReplyDraftsOutput,
            system_prompt=(
                "あなたは返信案を修正するアシスタントです。"
                "現在の返信案とチェック指摘・依頼文・自分の状況を受け取り、"
                "指摘を反映して修正した返信案を1件返してください。"
                "出力は必ず drafts に返信案1件のリスト（各要素は text）を含む JSON 形式にすること。"
            ),
        )

    def revise(
        self,
        drafts: list[ReplyDraft],
        check_result: CheckResult,
        request_text: RequestText,
        my_situation: MySituation,
    ) -> list[ReplyDraft]:
        drafts_text = "\n".join(f"- {d.text}" for d in drafts)
        must_fix_text = (
            "\n".join(f"- {s}" for s in check_result.must_fix) if check_result.must_fix else "（なし）"
        )
        nice_to_have_text = (
            "\n".join(f"- {s}" for s in check_result.nice_to_have)
            if check_result.nice_to_have
            else "（なし）"
        )
        user_prompt = (
            "【依頼文】\n"
            f"{request_text.value}\n\n"
            "【自分の状況】\n"
            f"{_format_situation(my_situation)}\n\n"
            "【現在の返信案リスト】\n"
            f"{drafts_text}\n\n"
            "【必須修正】\n"
            f"{must_fix_text}\n\n"
            "【任意改善】\n"
            f"{nice_to_have_text}\n\n"
            "上記の必須修正を反映し、可能なら任意改善も反映して、返信案を1件に修正して返してください。"
        )
        result = self._agent.run_sync(user_prompt)
        output: ReplyDraftsOutput = result.output
        print(f"revise output: {output}")
        print(f"revise output.drafts: {output.drafts}")
        return [ReplyDraft(text=d.text) for d in output.drafts]
