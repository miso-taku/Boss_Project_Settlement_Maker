"""Google Calendar MCP を用いた GetCalendarSituationPort の実装。

Pydantic AI の MCPServerStdio で mcp-google に接続し、list-calendars でタスク用カレンダーを特定し、
list-events でそのカレンダーからのみ予定（タスク）を取得する。
予定から残り時間（業務時間 9–18 の空き）と制約（HH:MM–HH:MM 予定名）を導出する。
日付・時刻は日本時間（JST, UTC+9）で扱う。
"""

import json
import os
import re
from datetime import date, datetime, timedelta, timezone
from typing import Any

# 日本時間（JST = UTC+9）
JST = timezone(timedelta(hours=9))

from dotenv import load_dotenv
from pydantic_ai.mcp import MCPServerStdio

from settlement_maker.application.ports import GetCalendarSituationPort
from settlement_maker.domain.models import MySituation
from settlement_maker.infrastructure.ai_mcp_logging import get_ai_mcp_logger

load_dotenv()

# 業務時間（固定 9:00–18:00 JST、9時間）
WORKDAY_START_HOUR = 9
WORKDAY_END_HOUR = 18
WORKDAY_HOURS = float(WORKDAY_END_HOUR - WORKDAY_START_HOUR)


def _mcp_result_to_log_string(result: Any) -> str:
    """MCP の direct_call_tool 戻り値をログ用に文字列化する。"""
    raw: Any = result
    if hasattr(raw, "content"):
        raw = raw.content
    try:
        if isinstance(raw, (list, dict)):
            return json.dumps(raw, ensure_ascii=False, default=str)
        return str(raw)
    except (TypeError, ValueError):
        return repr(raw)


def _env_for_mcp() -> dict[str, str]:
    """MCP サブプロセスに渡す環境変数（GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET）。"""
    env = os.environ.copy()
    # 既に .env から load_dotenv() で読み込まれている前提
    return env


def _to_iso_utc_z(dt: datetime) -> str:
    """datetime を API が要求する形式（YYYY-MM-DDTHH:MM:SSZ、マイクロ秒なし）に変換。"""
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso_to_local_hours(iso_str: str, target_date: date) -> tuple[int, int] | None:
    """ISO8601 文字列から JST の (時, 分) を返す。対象日でない場合は None。"""
    if not iso_str:
        return None
    try:
        if "T" in iso_str:
            dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            dt_jst = dt.astimezone(JST)
            if dt_jst.date() != target_date:
                return None
            return (dt_jst.hour, dt_jst.minute)
        return None
    except (ValueError, TypeError):
        return None


def _event_duration_hours(start_iso: str, end_iso: str, target_date: date) -> float:
    """予定の開始・終了から時間数を返す（対象日の業務時間内にクロップ）。"""
    start_hm = _parse_iso_to_local_hours(start_iso, target_date)
    end_hm = _parse_iso_to_local_hours(end_iso, target_date)
    if not start_hm or not end_hm:
        return 0.0
    start_m = start_hm[0] * 60 + start_hm[1]
    end_m = end_hm[0] * 60 + end_hm[1]
    # 業務時間内にクロップ
    work_start_m = WORKDAY_START_HOUR * 60
    work_end_m = WORKDAY_END_HOUR * 60
    start_m = max(start_m, work_start_m)
    end_m = min(end_m, work_end_m)
    if end_m <= start_m:
        return 0.0
    return (end_m - start_m) / 60.0


def _event_to_constraint_line(start_iso: str, end_iso: str, summary: str, target_date: date) -> str:
    """1 件の予定を 'HH:MM–HH:MM 予定名' 形式にする。"""
    start_hm = _parse_iso_to_local_hours(start_iso, target_date)
    end_hm = _parse_iso_to_local_hours(end_iso, target_date)
    if not start_hm or not end_hm:
        return summary or "(予定)"
    sh, sm = start_hm
    eh, em = end_hm
    title = (summary or "").strip() or "(予定)"
    return f"{sh:02d}:{sm:02d}–{eh:02d}:{em:02d} {title}"


# タスク用カレンダーとして扱う名前（いずれかに一致すれば採用）
TASK_CALENDAR_NAMES = ("ToDoリスト", "ToDo", "Tasks", "タスク", "TODO")


def _extract_calendars_from_tool_result(result: Any) -> list[dict[str, Any]]:
    """list-calendars の戻り値からカレンダーリストを抽出する。"""
    raw: Any = result
    if hasattr(raw, "content"):
        raw = raw.content
    calendars: list[dict[str, Any]] = []
    if isinstance(raw, list):
        for item in raw:
            text: str | None = None
            if isinstance(item, dict) and "text" in item:
                text = item["text"]
            elif hasattr(item, "text"):
                text = getattr(item, "text", None)
            elif isinstance(item, str):
                text = item
            if isinstance(text, str):
                calendars.extend(_parse_calendars_from_text(text))
    elif isinstance(raw, dict):
        if "items" in raw:
            calendars = raw["items"]
        elif "calendars" in raw:
            calendars = raw["calendars"]
        else:
            calendars = _parse_calendars_from_text(json.dumps(raw))
    elif isinstance(raw, str):
        calendars = _parse_calendars_from_text(raw)
    return calendars if isinstance(calendars, list) else []


def _parse_calendars_from_text(text: str) -> list[dict[str, Any]]:
    """文字列からカレンダーリストをパースする。JSON または mcp-google のテキスト形式「名前 (calendarId)」に対応。"""
    out: list[dict[str, Any]] = []
    text = (text or "").strip()
    # 1) JSON 形式を試す
    try:
        data = json.loads(text)
        if isinstance(data, list):
            for c in data:
                if isinstance(c, dict) and c.get("id"):
                    out.append(c)
            return out
        if isinstance(data, dict):
            if "items" in data and isinstance(data["items"], list):
                for c in data["items"]:
                    if isinstance(c, dict) and c.get("id"):
                        out.append(c)
                return out
    except json.JSONDecodeError:
        pass
    json_match = re.search(r"\[[\s\S]*?\]", text)
    if json_match:
        try:
            arr = json.loads(json_match.group())
            if isinstance(arr, list):
                for c in arr:
                    if isinstance(c, dict) and c.get("id"):
                        out.append(c)
                return out
        except json.JSONDecodeError:
            pass
    # 2) mcp-google のテキスト形式: 1行ごとに "名前 (calendarId)" または "calendarId (calendarId)"
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # "日本の祝日 (ja.japanese#holiday@...)" や "wk.ta93mis@gmail.com (wk.ta93mis@gmail.com)" 形式
        m = re.match(r"^(.+?)\s*\(([^)]+)\)\s*$", line)
        if m:
            summary_part = m.group(1).strip()
            cal_id = m.group(2).strip()
            out.append({"id": cal_id, "summary": summary_part})
    return out


def _find_task_calendar_id(calendars: list[dict[str, Any]]) -> str | None:
    """カレンダー一覧からタスク用（ToDoリスト等）の calendarId を返す。見つからなければ None。"""
    for cal in calendars:
        summary = (cal.get("summary") or cal.get("summaryOverride") or "").strip()
        if not summary:
            continue
        if any(name in summary for name in TASK_CALENDAR_NAMES):
            cid = cal.get("id")
            if cid:
                return cid
    return None


def _extract_events_from_tool_result(result: Any) -> list[dict[str, Any]]:
    """direct_call_tool の戻り値からイベントのリストを抽出する。"""
    events: list[dict[str, Any]] = []
    raw: Any = result
    # Pydantic AI MCP が content を持つオブジェクトを返す場合は中身を使う
    if hasattr(raw, "content"):
        raw = raw.content

    # MCP の ToolResult は content の並びのことが多い
    if isinstance(raw, list):
        for item in raw:
            text: str | None = None
            if isinstance(item, dict) and "text" in item:
                text = item["text"]
            elif hasattr(item, "text"):
                text = getattr(item, "text", None)
            elif isinstance(item, str):
                text = item
            if text:
                events.extend(_parse_events_from_text(text))
    elif isinstance(raw, dict):
        if "items" in raw:
            events = raw["items"]
        elif "events" in raw:
            events = raw["events"]
        else:
            events.extend(_parse_events_from_text(json.dumps(raw)))
    elif isinstance(raw, str):
        events.extend(_parse_events_from_text(raw))

    return events


def _parse_events_from_mcp_text(text: str) -> list[dict[str, Any]]:
    """mcp-google の list-events テキスト形式をパースする。

    形式例:
      資料作成 (3vkodjrsqu7bs5ucaifdposgfo)
      Description: 資料作成
      Start: 2026-02-23T13:30:00+09:00
      End: 2026-02-23T18:00:00+09:00
      Reminders: Using default
    """
    events: list[dict[str, Any]] = []
    text = (text or "").strip()
    # 1ブロック = 1行目がタイトル、続いて Description / Start / End
    pattern = re.compile(
        r"^(.+?)(?:\s*\([^)]+\))?\s*\n"  # 1行目: タイトル (id) は省略可
        r"Description:[^\n]*\n"
        r"Start:\s*([^\n]+)\n"
        r"End:\s*([^\n]+)",
        re.MULTILINE,
    )
    for m in pattern.finditer(text):
        summary = m.group(1).strip()
        start_iso = m.group(2).strip()
        end_iso = m.group(3).strip()
        events.append({
            "summary": summary,
            "start": {"dateTime": start_iso},
            "end": {"dateTime": end_iso},
        })
    return events


def _parse_events_from_text(text: str) -> list[dict[str, Any]]:
    """文字列（JSON または mcp-google テキスト形式）からイベントリストをパースする。"""
    events: list[dict[str, Any]] = []
    text = (text or "").strip()
    # 1) JSON 配列を探す
    json_match = re.search(r"\[[\s\S]*?\]", text)
    if json_match:
        try:
            arr = json.loads(json_match.group())
            if isinstance(arr, list):
                for e in arr:
                    if isinstance(e, dict):
                        events.append(e)
                return events
        except json.JSONDecodeError:
            pass
    try:
        data = json.loads(text)
        if isinstance(data, list):
            for e in data:
                if isinstance(e, dict):
                    events.append(e)
            return events
        if isinstance(data, dict) and "items" in data:
            events = data["items"]
            return events
    except json.JSONDecodeError:
        pass
    # 2) mcp-google のテキスト形式（Description / Start / End）
    events = _parse_events_from_mcp_text(text)
    return events


def _get_event_time_range(ev: dict[str, Any]) -> tuple[str, str]:
    """Google Calendar 形式の start/end から ISO 文字列を取得。"""
    start = ev.get("start") or {}
    end = ev.get("end") or {}
    start_iso = start.get("dateTime") or start.get("date") or ""
    end_iso = end.get("dateTime") or end.get("date") or ""
    if isinstance(start_iso, str) and isinstance(end_iso, str):
        return (start_iso, end_iso)
    return ("", "")


def _derive_situation_from_events(
    events: list[dict[str, Any]],
    target_date: date,
    reference_dt: datetime | None = None,
) -> MySituation:
    """予定リストから残り時間と制約を導出して MySituation を返す。

    reference_dt が指定された場合（現在時刻）は「reference_dt から業務終了までの残り」から
    予定時間を差し引く。未指定の場合は従来どおり「業務時間全体 - 予定時間」。
    """
    total_event_hours = 0.0
    constraint_parts: list[str] = []

    for ev in events:
        start_iso, end_iso = _get_event_time_range(ev)
        summary = ev.get("summary") or ev.get("title") or ""
        total_event_hours += _event_duration_hours(start_iso, end_iso, target_date)
        line = _event_to_constraint_line(start_iso, end_iso, summary, target_date)
        if line:
            constraint_parts.append(line)

    if reference_dt is not None:
        # 現在時刻ベース: 業務終了（18:00 JST）までの残り時間 - 予定時間
        end_workday_jst = datetime(
            target_date.year, target_date.month, target_date.day,
            WORKDAY_END_HOUR, 0, 0, tzinfo=JST,
        )
        if reference_dt.tzinfo is None:
            reference_dt = reference_dt.replace(tzinfo=JST)
        else:
            reference_dt = reference_dt.astimezone(JST)
        delta_seconds = (end_workday_jst - reference_dt).total_seconds()
        cap_hours = max(0.0, min(float(WORKDAY_HOURS), delta_seconds / 3600.0))
        remaining = max(0.0, cap_hours - total_event_hours)
    else:
        remaining = max(0.0, WORKDAY_HOURS - total_event_hours)

    constraints_str = "\n".join(constraint_parts) if constraint_parts else ""

    return MySituation(
        remaining_hours=round(remaining, 1),
        priority=None,
        constraints=constraints_str,
    )


class CalendarMCPAdapter(GetCalendarSituationPort):
    """mcp-google を MCPServerStdio で呼び出す GetCalendarSituationPort の実装。"""

    def __init__(
        self,
        *,
        command: str = "npx",
        args: list[str] | None = None,
        env: dict[str, str] | None = None,
        timeout: float = 30.0,
    ) -> None:
        self._command = command
        self._args = args if args is not None else ["-y", "mcp-google"]
        self._env = env if env is not None else _env_for_mcp()
        self._timeout = timeout

    def _make_server(self) -> MCPServerStdio:
        return MCPServerStdio(
            self._command,
            args=self._args,
            env=self._env,
            timeout=self._timeout,
        )

    async def get_my_situation_for_date(self, target_date: date) -> MySituation:
        """指定日の予定をタスク用カレンダー（ToDoリスト等）からのみ list-events で取得し、残り時間・制約を導出する。

        日付・時刻は日本時間（JST）で扱う。対象日が今日（JST）の場合は現在時刻を
        time_min に使い、残り時間は「現在〜業務終了 18:00 JST」ベースで計算する。
        タスク用カレンダーが見つからない場合は予定なしとして扱う。
        """
        now_jst = datetime.now(JST)
        today_jst = now_jst.date()

        if target_date == today_jst:
            time_min_dt = now_jst.astimezone(timezone.utc)
            time_min = _to_iso_utc_z(time_min_dt)
            reference_dt = now_jst
        else:
            start_of_day_jst = datetime(
                target_date.year, target_date.month, target_date.day,
                0, 0, 0, tzinfo=JST,
            )
            time_min = _to_iso_utc_z(start_of_day_jst.astimezone(timezone.utc))
            reference_dt = None

        end_of_day_jst = datetime(
            target_date.year, target_date.month, target_date.day,
            23, 59, 59, tzinfo=JST,
        )
        time_max = _to_iso_utc_z(end_of_day_jst.astimezone(timezone.utc))

        server = self._make_server()
        async with server:
            calendars_result = await server.direct_call_tool("list-calendars", {})
            get_ai_mcp_logger().info(
                "mcp_tool=list-calendars args=%s result=%s",
                json.dumps({}),
                _mcp_result_to_log_string(calendars_result),
            )
            calendars = _extract_calendars_from_tool_result(calendars_result)
            task_calendar_id = _find_task_calendar_id(calendars)
            if not task_calendar_id:
                task_calendar_id = "primary"

            tool_args = {
                "calendarId": task_calendar_id,
                "timeMin": time_min,
                "timeMax": time_max,
                "maxResults": 50,
            }
            result = await server.direct_call_tool("list-events", tool_args)
            get_ai_mcp_logger().info(
                "mcp_tool=list-events args=%s result=%s",
                json.dumps(tool_args, ensure_ascii=False),
                _mcp_result_to_log_string(result),
            )
        events = _extract_events_from_tool_result(result)
        return _derive_situation_from_events(events, target_date, reference_dt=reference_dt)
