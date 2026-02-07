"""依頼文・自分の状況・返信案のドメインモデル（値オブジェクト）。

I/O 禁止。エンティティ・値オブジェクト・ドメインルールのみ。
用語は glossary に合わせる（依頼文・自分の状況・残り時間・優先度・制約・返信案）。
"""

from dataclasses import dataclass
from enum import Enum


class Priority(str, Enum):
    """優先度（3段階）。"""

    HIGH = "high"  # 高
    MEDIUM = "medium"  # 中
    LOW = "low"  # 低


@dataclass(frozen=True)
class RequestText:
    """依頼文（相手から受け取った依頼のテキスト）。"""

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("依頼文は空にできません")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class MySituation:
    """自分の状況（残り時間・優先度・制約）。"""

    remaining_hours: float | None  # 残り時間（時間単位）。任意
    priority: Priority | None  # 優先度（3段階）。任意
    constraints: str  # 制約（自由文）。空文字可

    def __post_init__(self) -> None:
        if self.remaining_hours is not None and self.remaining_hours < 0:
            raise ValueError("残り時間は0以上である必要があります")

    def __str__(self) -> str:
        parts = []
        if self.remaining_hours is not None:
            parts.append(f"残り時間: {self.remaining_hours}h")
        if self.priority is not None:
            parts.append(f"優先度: {self.priority.value}")
        if self.constraints:
            parts.append(f"制約: {self.constraints}")
        return "; ".join(parts) if parts else "(未入力)"


@dataclass(frozen=True)
class ReplyDraft:
    """返信案（AI が生成した1件の文案）。"""

    text: str

    def __str__(self) -> str:
        return self.text


@dataclass(frozen=True)
class CheckResult:
    """返信案チェック結果（OK/NG と指摘・改善点）。"""

    ok: bool  # True: 合格, False: 要修正
    feedback: str  # 指摘・改善点（NG 時）。OK の場合は空文字可
