from app.nlp.handlers.food_handlers import handle_food
from app.nlp.handlers.exercise_handlers import handle_exercise
from app.nlp.handlers.stats_profile_handlers import handle_stats_profile

FOOD_INTENTS = {
    "log_food", "edit_food_entry", "add_food_items", "move_food_entry", "delete_food_entry"
}

EXERCISE_INTENTS = {
    "log_exercise", "edit_exercise_entry", "edit_exercise_item", "add_exercise_items", "delete_exercise_entry"
}

STATS_PROFILE_INTENTS = {
    "show_summary_today", "show_summary_date", "show_weekly_stats", "show_stats_this_week",
    "update_profile", "undo"
}

def route_frame(frame, context):
    intent = frame.get("intent")
    data = frame.get("data", {})

    if not intent:
        return {"message": "Missing intent in frame", "result": None}

    if intent in FOOD_INTENTS:
        return handle_food(intent, data, context)

    if intent in EXERCISE_INTENTS:
        # Note: handle_exercise might still expect repo, checking next
        return handle_exercise(intent, data, context)

    if intent in STATS_PROFILE_INTENTS:
        # Note: handle_stats_profile might still expect repo, checking next
        return handle_stats_profile(intent, data, context)

    return {"message": f"Unknown intent: {intent}", "result": None}
