from typing import Any, Dict
from datetime import date
from app.services.stats_handlers import build_daily_stats, build_weekly_stats


def handle_stats_profile(intent: str, data: Dict[str, Any], repo, context: Dict[str, Any]):
    selected_date = context["date"]

    if intent == "show_summary_today":
        stats = build_daily_stats(context, selected_date)
        return {
            "message": _format_daily_message(stats),
            "result": stats
        }

    if intent == "show_summary_date":
        target = date.fromisoformat(data["date"])
        stats = build_daily_stats(context, target)
        return {
            "message": _format_daily_message(stats),
            "result": stats
        }

    if intent in ("show_weekly_stats", "show_stats_this_week"):
        stats = build_weekly_stats(context, selected_date)
        return {
            "message": _format_weekly_message(stats),
            "result": stats
        }

    return {"message": "Unknown stats command", "result": None}


def _format_daily_message(stats: Dict[str, Any]) -> str:
    return (
        f"Summary for {stats['date']}:\n"
        f"- Intake: {stats['intake_kcal']} kcal\n"
        f"- Burned: {stats['burned_kcal']} kcal\n"
        f"- Net: {stats['net_kcal']} kcal\n"
        f"- {stats['message']}"
    )

def _format_weekly_message(stats: Dict[str, Any]) -> str:
    return (
        f"Weekly summary ({stats['start_date']} → {stats['end_date']}):\n"
        f"- Total intake: {stats['total_intake_kcal']} kcal\n"
        f"- Total burned: {stats['total_burned_kcal']} kcal"
    )
