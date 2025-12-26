from typing import Any, Dict, List, Optional
from datetime import date, timedelta
from decimal import Decimal

from backend.app.repositories.stats_repo import get_day_logs, get_week_logs, get_log_dates, get_total_days_logged, get_lifetime_stats, get_period_stats
from backend.app.repositories.profile_repo import get_profile, upsert_profile
from backend.app.repositories.goal_repo import get_goal, upsert_goal
from backend.app.services.health_service import calculate_health_stats
from backend.app.services.goal_service import infer_goal_from_target, calculate_daily_target
from calendar import monthrange

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

        # Calculate totals from individual items (food_item.kcal, exercise_entry.burned_kcal)
        total_intake = sum(float(e.get("kcal", 0)) for e in logs["food_entries"])
        total_burned = sum(float(e.get("burned_kcal", 0)) for e in logs["exercise_entries"])

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
                f"\n\nTotals Today:\n"
                f"Intake: {total_intake} kcal\n"
                f"Burned: {total_burned} kcal\n"
            )

            stats_msg += (
                f"\nHealth:\n"
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
    def get_overview_stats(user_id: int) -> Dict[str, Any]:
        """
        Get overview for homepage: streak, total days, weight progress.
        """
        profile = get_profile(user_id) or {}
        
        # --- Streak Calculation (Business Logic) ---
        log_dates = get_log_dates(user_id)
        streak = 0
        if log_dates:
            dates = log_dates # Already sorted DESC
            today = date.today()
            yesterday = today - timedelta(days=1)
            
            # Check if streak is active
            if dates[0] == today or dates[0] == yesterday:
                current_date = dates[0]
                for d in dates:
                    expected = current_date - timedelta(days=streak)
                    if d == expected:
                        streak += 1
                    else:
                        break
        
        total_days = get_total_days_logged(user_id)
        lifetime_stats = get_lifetime_stats(user_id)
        
        # Determine weight start vs current
        current_weight = profile.get("weight_kg", 0.0)
        start_weight = current_weight # Placeholder until weight history is implemented
        
        return {
            "total_days_logged": total_days,
            "current_streak": streak,
            "weight_start": start_weight,
            "weight_current": current_weight,
            "start_date": "2023-01-01",
            "total_calories_intake": lifetime_stats["total_intake"],
            "total_calories_burned": lifetime_stats["total_burned"]
        }

    @staticmethod
    def update_profile(user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update profile and goal, recalculate stats.
        Expected data keys matching ProfileUpdateRequest:
        height_cm, weight_kg, age, gender, activity_level, goal_type, target_weight_kg
        """
        
        # 1. Update Profile Fields
        profile_fields = ["height_cm", "weight_kg", "age", "gender", "activity_level"]
        profile_update = {k: data[k] for k in profile_fields if k in data and data[k] is not None}
        
        if profile_update:
            upsert_profile(user_id, **profile_update)

        # 2. Update Goal Fields (if provided)
        goal_type = data.get("goal_type")
        target_weight = data.get("target_weight_kg")
        
        if goal_type or target_weight is not None:
            # We need current goal state if partial update
            current_goal = get_goal(user_id) or {}
            
            new_goal_type = goal_type if goal_type else current_goal.get("goal_type")
            new_target_weight = target_weight if target_weight is not None else current_goal.get("target_weight_kg")
            
            # Infer delta if we have both weights
            current_profile = get_profile(user_id)
            current_weight = current_profile.get("weight_kg") if current_profile else 0
            
            delta = 0
            if new_target_weight and current_weight:
                _, delta = infer_goal_from_target(current_weight, new_target_weight)
                
            upsert_goal(
                user_id=user_id, 
                goal_type=new_goal_type, 
                target_weight_kg=new_target_weight,
                target_delta_kg=delta
            )

        # 3. Recalculate TDEE & Daily Target (Always needed if profile or goal changed)
        profile_db = get_profile(user_id)
        goal_db = get_goal(user_id)
        
        health_metrics = {"bmi": 0, "bmr": 0, "tdee": 0}
        
        if profile_db:
             health_metrics = calculate_health_stats({
                "weight": profile_db.get("weight_kg", 0),
                "height": profile_db.get("height_cm", 0),
                "age": profile_db.get("age", 25),
                "gender": profile_db.get("gender", "male"),
                "activity_level": profile_db.get("activity_level", "sedentary"),
            })
             
        # Update daily target if we have goal + tdee
        if goal_db and goal_db.get("goal_type") and health_metrics["tdee"] > 0:
            daily_target = calculate_daily_target(health_metrics["tdee"], goal_db["goal_type"])
            upsert_goal(
                user_id=user_id, 
                goal_type=goal_db["goal_type"], 
                daily_target_kcal=daily_target
            )
            goal_db["daily_target_kcal"] = daily_target # Update local dict for return

        return {
            "success": True,
            "message": "Profile updated successfully.",
            "profile": profile_db,
            "goal": goal_db,
            "health_metrics": health_metrics
        }

    @staticmethod
    def get_day_view_api(user_id: int, entry_date: date) -> Dict[str, Any]:
        """
        Get day view for API - reuses existing data from DB (intake_kcal, burned_kcal).
        """
        logs = get_day_logs(user_id, entry_date)
        goal = get_goal(user_id)
        
        # Calculate totals from individual food items (each has kcal field)
        # Note: food_items come from food_item table which has kcal per item
        intake = sum(float(f.get("kcal", 0)) for f in logs.get("food_entries", []))
        burned = sum(float(e.get("burned_kcal", 0)) for e in logs.get("exercise_entries", []))
        net = intake - burned
        target = goal["daily_target_kcal"] if goal else 0
        remaining = target - net if target else 0
        
        # Format entries for API
        food_entries = [{
            "id": f["id"],
            "type": "food",
            "name": f["item_name"],
            "calories": float(f.get("kcal", 0)),  # calories for this specific item
            "time": f.get("time"),
            "quantity": float(f.get("quantity", 1)),
            "unit": f.get("unit"),
        } for f in logs.get("food_entries", [])]
        
        exercise_entries = [{
            "id": x["id"],
            "type": "exercise",
            "name": x["name"],
            "calories": float(x.get("burned_kcal", 0)),
            "time": x.get("time"),
        } for x in logs.get("exercise_entries", [])]
        
        return {
            "date": entry_date.isoformat(),
            "summary": {
                "intake_kcal": round(intake),
                "burned_kcal": round(burned),
                "net_kcal": round(net),
                "target_kcal": target,
                "remaining_kcal": round(remaining),
            },
            "food_entries": food_entries,
            "exercise_entries": exercise_entries,
        }

    @staticmethod
    def get_month_view_api(user_id: int, month: str) -> Dict[str, Any]:
        """
        Get month view for API - uses get_period_stats which already aggregates data.
        """
        try:
            y_str, m_str = month.split("-")
            year = int(y_str)
            month_int = int(m_str)
        except ValueError:
            today = date.today()
            year, month_int = today.year, today.month
        
        start_date = date(year, month_int, 1)
        _, last_day = monthrange(year, month_int)
        end_date = date(year, month_int, last_day)
        
        # get_period_stats already calculates intake/burned/target per day
        logs = get_period_stats(user_id, start_date, end_date)
        
        days = []
        for d in logs:
            net = float(d["intake_kcal"]) - float(d["burned_kcal"])
            target = float(d["target_kcal"])
            status = "under_budget" if net <= target else "over_budget"
            
            days.append({
                "date": d["entry_date"].isoformat(),
                "status": status,
                "net_kcal": round(net),
            })
        
        return {
            "month": month,
            "days": days
        }
