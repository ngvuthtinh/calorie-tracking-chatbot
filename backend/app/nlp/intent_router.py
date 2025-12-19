from handlers.food_handlers import handle_food
from handlers.exercise_handlers import handle_exercise
from handlers.stats_profile_handlers import handle_stats_profile

def route_frame(frame, repo, context):
    intent = frame["intent"]
    data = frame.get("data", {})

    if intent.startswith("log_food") or intent in {
        "log_food", "edit_food_entry", "add_food_items", "move_food_entry", "delete_food_entry"
    }:
        return handle_food(intent, data, repo, context)

    if intent in {
        "log_exercise", "edit_exercise_entry", "add_exercise_items", "delete_exercise_entry"
    }:
        return handle_exercise(intent, data, repo, context)

    if intent in {
        "show_summary_today", "show_summary_date", "show_weekly_stats", "show_stats_this_week",
        "update_profile", "undo"
    }:
        return handle_stats_profile(intent, data, repo, context)

    return {"message": f"Unknown intent: {intent}", "result": None}
