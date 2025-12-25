from typing import Any, Dict, List, Optional
from datetime import date, timedelta
from decimal import Decimal

from backend.app.repositories.stats_repo import get_day_logs, get_week_logs
from backend.app.repositories.profile_repo import get_profile, upsert_profile
from backend.app.repositories.goal_repo import get_goal, upsert_goal
from backend.app.services.health_service import calculate_health_stats
from backend.app.services.goal_service import infer_goal_from_target, calculate_daily_target

class UserService:
    """
    Service layer for User, Profile, and Stats operations.
    """

    @staticmethod
    def _format_summary(entries: List[Dict[str, Any]]) -> str:
        if not entries:
            return "No entries for this day."
        lines = []
        for i, e in enumerate(entries, 1):
            if "type" in e:
                desc = e["type"]
                if "calories" in e:
                    desc += f" ({e['calories']} kcal)"
                lines.append(f"{i}. {desc}")
            elif "items" in e:  # Entry with sub-items
                items_desc = []
                for item in e["items"]:
                    # Item structure differs for food vs exercise
                    # Food item: name, qty, unit, kcal
                    # Exercise item: type, duration/dist/reps
                    
                    # Handler logic for exercise:
                    t = item.get("type", item.get("name", "unknown")) # Fallback for food item name?
                    
                    # Exercise specific checks
                    if "duration_min" in item:
                        items_desc.append(f"{t} {item['duration_min']}min")
                    elif "distance_km" in item:
                        items_desc.append(f"{t} {item['distance_km']}km")
                    elif "reps" in item:
                        items_desc.append(f"{item['reps']} {t}")
                    elif "kcal" in item: # Food item likely
                        items_desc.append(f"{t} ({item.get('kcal')} kcal)")
                    else:
                         items_desc.append(f"{t}")
                         
                lines.append(f"{i}. {', '.join(items_desc)}")
                
        return "\n".join(lines)


    @staticmethod
    def get_user_profile(user_id: int) -> Dict[str, Any]:
        return get_profile(user_id) or {}

    @classmethod
    def get_summary_today(cls, user_id: int, day: date) -> Dict[str, Any]:
        logs = get_day_logs(user_id, day)
        profile = get_profile(user_id)
        goal = get_goal(user_id)

        stats_msg = ""
        if profile:
            # Prepare stats dict (handle missing keys gracefully)
            stats = calculate_health_stats({
                "weight": profile.get("weight_kg", 0),
                "height": profile.get("height_cm", 0),
                "age": profile.get("age", 0),
                "gender": profile.get("gender", "male"),
                "activity_level": profile.get("activity_level", "sedentary"),
            })

            stats_msg += (
                f"\n\nHealth:\n"
                f"BMI: {stats['bmi']}\n"
                f"BMR: {stats['bmr']} kcal\n"
                f"TDEE: {stats['tdee']} kcal"
            )

            if goal and goal.get("daily_target_kcal") is not None:
                stats_msg += (
                    f", Daily target: {goal['daily_target_kcal']} kcal "
                    f"({goal.get('goal_type', 'unknown')})"
                )
            elif goal:
                stats_msg += f"\nGoal: {goal.get('goal_type')} (target not calculated yet)"

        message = (
            f"Summary for {day}:\n\n"
            f"Food:\n{cls._format_summary(logs['food_entries'])}\n\n"
            f"Exercise:\n{cls._format_summary(logs['exercise_entries'])}"
            f"{stats_msg}"
        )

        return {
            "success": True,
            "message": message,
            "result": logs
        }

    @classmethod
    def get_summary_date(cls, user_id: int, day: date) -> Dict[str, Any]:
        logs = get_day_logs(user_id, day)
        
        food_summary = cls._format_summary(logs["food_entries"])
        exercise_summary = cls._format_summary(logs["exercise_entries"])

        message = (
            f"Summary for {day.isoformat()}:\n\n"
            f"Food:\n{food_summary}\n\n"
            f"Exercise:\n{exercise_summary}"
        )

        return {
            "success": True,
            "message": message,
            "result": logs
        }

    @staticmethod
    def get_weekly_stats(user_id: int, end_date: date) -> Dict[str, Any]:
        start_date = end_date - timedelta(days=6)
        week_logs = get_week_logs(user_id, start_date, end_date)

        total_food = []
        total_exercise = []

        for day_log in week_logs:
            total_food.extend(day_log.get("food_entries", []))
            total_exercise.extend(day_log.get("exercise_entries", []))

        message = (
            f"Weekly summary ({start_date.isoformat()} → {end_date.isoformat()}):\n"
            f"Food entries: {len(total_food)}\n"
            f"Exercise entries: {len(total_exercise)}"
        )

        return {
            "success": True,
            "message": message,
            "result": {
                "days": week_logs,
                "food_entries": total_food,
                "exercise_entries": total_exercise,
            }
        }

    @staticmethod
    def update_profile(user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        field = data.get("field")
        value = data.get("value")
        
        # Helper to extract numeric value
        def extract_val(val):
            if isinstance(val, (int, float, Decimal)):
                return float(val)
            try:
                return float(str(val).split()[0])
            except Exception:
                return 0.0

        updated_profile_state = {} # To return

        # --- GOAL AUTO UPDATE ---
        if field == "goal" and value == "auto":
            target_weight = extract_val(data.get("target_weight", 0))
            profile_db = get_profile(user_id)
            if not profile_db or not profile_db.get("weight_kg"):
                return {"success": False, "message": "Please set your weight before setting a goal."}

            # Infer goal type and delta
            goal_type, delta = infer_goal_from_target(float(profile_db["weight_kg"]), target_weight)

            # Calculate daily target using target weight
            profile_for_stats = {**profile_db, "weight_kg": target_weight}
            stats = calculate_health_stats({
                "weight": profile_for_stats["weight_kg"],
                "height": profile_for_stats.get("height_cm", 0),
                "age": profile_for_stats.get("age", 25),
                "gender": profile_for_stats.get("gender", "male"),
                "activity_level": profile_for_stats.get("activity_level", "sedentary"),
            })
            daily_target = calculate_daily_target(stats["tdee"], goal_type)

            # Upsert goal
            upsert_goal(
                user_id=user_id,
                goal_type=goal_type,
                target_weight_kg=target_weight,
                target_delta_kg=delta,
                daily_target_kcal=daily_target,
            )

            msg = f"Updated goal: {goal_type}, Daily target: {daily_target} kcal"
            
            # Construct return result with inferred details
            updated_profile_state = {
                "goal": goal_type,
                "target_weight": target_weight,
                "target_delta": delta,
                "daily_target_kcal": daily_target
            }
            return {"success": True, "message": msg, "result": updated_profile_state}

        # --- PROFILE UPDATE ---
        kwargs = {}
        if field == "weight":
            val = extract_val(value)
            kwargs["weight_kg"] = val
            updated_profile_state[field] = val
        elif field == "height":
            val = extract_val(value)
            kwargs["height_cm"] = val
            updated_profile_state[field] = val
        elif field == "age":
            val = int(extract_val(value))
            kwargs["age"] = val
            updated_profile_state[field] = val
        elif field == "gender":
            kwargs["gender"] = value
            updated_profile_state[field] = value
        elif field == "activity_level":
            kwargs["activity_level"] = value
            updated_profile_state[field] = value

        if kwargs:
            upsert_profile(user_id, **kwargs)

        # Recalculate daily target using **current weight** and existing goal
        profile_db = get_profile(user_id)
        goal_db = get_goal(user_id)
        daily_target = None
        
        if profile_db and goal_db and goal_db.get("goal_type"):
            # Recalculate daily target using updated profile

            stats = calculate_health_stats({
                "weight": profile_db.get("weight_kg", 0),
                "height": profile_db.get("height_cm", 0),
                "age": profile_db.get("age", 25),
                "gender": profile_db.get("gender", "male"),
                "activity_level": profile_db.get("activity_level", "sedentary"),
            })
            daily_target = calculate_daily_target(stats["tdee"], goal_db["goal_type"])
            upsert_goal(user_id=user_id, goal_type=goal_db["goal_type"], daily_target_kcal=daily_target)
            updated_profile_state["daily_target_kcal"] = daily_target

        return {
            "success": True,
            "message": f"Updated profile: {field} = {value}, Daily target: {daily_target if daily_target else 0} kcal",
            "result": updated_profile_state,
        }
