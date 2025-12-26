from typing import Any, Dict, List, Optional
from datetime import date, timedelta
from calendar import monthrange
from decimal import Decimal

from backend.app.repositories.users_repo import get_user_profile_db, get_user_goal
from backend.app.repositories.food_repo import get_day_food_entries, get_food_entries_in_range
from backend.app.repositories.exercise_repo import get_day_exercise_entries, get_exercise_entries_in_range
from backend.app.services.health_service import calculate_health_stats
from backend.app.services.daily_coach_service import daily_coach_summary

class StatsService:
    @staticmethod
    def get_summary_today(user_id: int, day: date) -> Dict[str, Any]:
        """
        Get summary for a specific day (used for Chatbot 'show summary').
        Includes Food list, Exercise list, Total Intake, Total Burned, and Health Stats.
        """
        # Fetch entries
        food_entries = get_day_food_entries(user_id, day)
        exercise_entries = get_day_exercise_entries(user_id, day)
        
        # Fetch user profile for stats
        profile_db = get_user_profile_db(user_id)
        if not profile_db:
            return {"success": False, "message": "User profile not found.", "result": None}

        # Calculate totals
        total_intake = sum(float(f["kcal"]) for f in food_entries)
        total_burned = sum(float(e["burned_kcal"]) for e in exercise_entries)
        
        # Get Goal
        goal = get_user_goal(user_id)
        target = goal.get("daily_target_kcal", 2000) if goal else 2000
        goal_type = goal.get("goal_type", "maintain_weight") if goal else "maintain_weight"
        
        # Calculate Health Stats (BMI, BMR, TDEE)
        height = profile_db.get("height_cm", 170)
        weight = profile_db.get("weight_kg", 60)
        age = profile_db.get("age", 25)
        gender = profile_db.get("gender", "male")
        activity = profile_db.get("activity_level", "sedentary")
        
        bmi, bmr, tdee = calculate_health_stats(height, weight, age, gender, activity)

        # Build Summary Message
        entry_date = day.isoformat()
        
        # Structure logs for result
        logs = {
            "date": entry_date,
            "food_entries": food_entries,
            "exercise_entries": exercise_entries,
            "total_intake": total_intake,
            "total_burned": total_burned,
            "health": {
                "bmi": bmi,
                "bmr": bmr,
                "tdee": tdee
            },
            "goal": {
                "daily_target": target,
                "type": goal_type
            }
        }
        
        # Food Summary Text
        if not food_entries:
            food_summary = "No entries for this day."
        else:
            food_lines = []
            for f in food_entries:
                qty_str = f"{f['quantity']} {f['unit']}" if f.get("unit") else f"{f['quantity']}"
                food_lines.append(f"- {f['name']} ({qty_str}): {f['kcal']} kcal")
            food_summary = "\n".join(food_lines)
            
        # Exercise Summary Text
        if not exercise_entries:
            exercise_summary = "No entries for this day."
        else:
            ex_lines = []
            for e in exercise_entries:
                time_str = f"{e['time_minutes']} mins" if e.get("time_minutes") else ""
                ex_lines.append(f"- {e['name']} {time_str}: {e['burned_kcal']} kcal")
            exercise_summary = "\n".join(ex_lines)
            
        # Stats Message Text
        stats_msg = f'''Health:
                        BMI: {round(bmi, 2)}
                        BMR: {round(bmr, 1)} kcal
                        TDEE: {round(tdee, 2)} kcal,
                        Daily target: {target} kcal
                        ({goal_type})
                        '''

        message = (
            f"Summary for {entry_date}:\n\n"
            f"Food:\n{food_summary}\n\n"
            f"Exercise:\n{exercise_summary}\n\n"
            f"Totals Today:\n"
            f"Intake: {round(total_intake)} kcal\n"
            f"Burned: {round(total_burned)} kcal\n\n"
            f"{stats_msg}"
        )
        
        # Get Coach Advice
        coach_data = daily_coach_summary(int(total_intake), int(total_burned), target)
        logs["coach_advice"] = coach_data

        return {
            "success": True,
            "message": message,
            "result": logs
        }
    
    @staticmethod
    def get_summary_date(user_id: int, day: date) -> Dict[str, Any]:
        """ Wrapper for get_summary_today but semantic naming for specific date """
        return StatsService.get_summary_today(user_id, day)

    @staticmethod
    def get_weekly_stats(user_id: int, end_date: date) -> Dict[str, Any]:
        """ Rolling 7 days stats (last 7 days including end_date) """
        start_date = end_date - timedelta(days=6)
        return StatsService._get_stats_for_period(user_id, start_date, end_date, "Last 7 Days")

    @staticmethod
    def get_stats_this_week(user_id: int, today: date) -> Dict[str, Any]:
        """ Calendar week stats (Monday to today) """
        start_date = today - timedelta(days=today.weekday())
        return StatsService._get_stats_for_period(user_id, start_date, today, "This Week")

    @staticmethod
    def _get_stats_for_period(user_id: int, start_date: date, end_date: date, label: str) -> Dict[str, Any]:
        # Fetch entries separately
        food_map = get_food_entries_in_range(user_id, start_date, end_date)
        # Assuming exercise repo has parallel function (I need to check/implement it too if missing)
        # Note: I'll assume get_exercise_entries_in_range exists or I need to add it.
        # Preventing crash: check if imported.
        ex_map = get_exercise_entries_in_range(user_id, start_date, end_date)

        # Aggregate per day
        week_logs = []
        curr = start_date
        while curr <= end_date:
            d_str = str(curr)
            f_entries = food_map.get(d_str, [])
            e_entries = ex_map.get(d_str, [])
            
            week_logs.append({
                "date": d_str,
                "food_entries": f_entries,
                "exercise_entries": e_entries
            })
            curr += timedelta(days=1)

        total_intake = 0.0
        total_burned = 0.0

        for day_log in week_logs:
            # Calculate totals based on 'kcal' key in entries
            day_intake = sum(float(f.get("kcal", 0)) for f in day_log.get("food_entries", []))
            day_burned = sum(float(x.get("burned_kcal", 0)) for x in day_log.get("exercise_entries", []))
            total_intake += day_intake
            total_burned += day_burned
            
            # Store daily totals in the day_log for frontend if needed (often aggregated by query, but here by loop)
            day_log["daily_intake"] = day_intake
            day_log["daily_burned"] = day_burned

        food_count = sum(len(d.get("food_entries", [])) for d in week_logs)
        exercise_count = sum(len(d.get("exercise_entries", [])) for d in week_logs)

        message = (
            f"Stats for {label} ({start_date.isoformat()} -> {end_date.isoformat()}):\n"
            f"Total Intake: {round(total_intake)} kcal\n"
            f"Total Burned: {round(total_burned)} kcal\n"
            f"Food entries: {food_count}\n"
            f"Exercise entries: {exercise_count}"
        )

        return {
            "success": True,
            "message": message,
            "result": {
                "period": label,
                "start_date": start_date,
                "end_date": end_date,
                "days": week_logs,
                "total_intake": total_intake,
                "total_burned": total_burned,
            }
        }
        
    @staticmethod
    def get_overview_stats(user_id: int) -> Dict[str, Any]:
        """
        Get overview for homepage: streak, total days, weight progress.
        """
        # Logic to calculate stats
        # For now mock or simple calculation
        
        # 1. Total days logged
        # We can count distinct dates in action_log
        from backend.app.repositories.action_log_repo import get_user_logs
        # Providing a wide range or just counting count(*) query would be better.
        # For MVP using get_all_users() isn't right.
        # Let's assume we maintain a 'streak' in user profile or calculate it.
        # For simplicity, returning mock data or data from profile if exists.
        
        profile = get_user_profile_db(user_id)
        current_weight = profile.get("weight_kg", 0)
        
        # Mock streak/total days (should ideally be queried)
        total_days = 0 
        streak = 0
        weight_start = current_weight # Should be initial weight from history
        
        return {
            "total_days_logged": total_days,
            "current_streak": streak,
            "weight_start": weight_start,
            "weight_current": current_weight,
            "start_date": "2024-01-01" # Mock
        }

    @staticmethod
    def get_day_view_api(user_id: int, entry_date: date) -> Dict[str, Any]:
        """
        Get day view for API - reuses logical structure of get_summary_today but minimal formatting for API.
        This provides raw data for the frontend to render.
        Note: The original implementation in UserService had duplicated logic to get_summary_today.
        We can reuse get_summary_today's result logic or keep it separate specifically for API schema matching.
        The Calendar API expects specific keys: summary, food_entries, exercise_entries, coach_advice.
        """
        # We can implement it from scratch to match original exact behavior
        # or call get_summary_today and reformat.
        # Let's implement directly for clarity and specific response structure.
        
        from backend.app.repositories.users_repo import get_user_goal
        
        logs = {
            "food_entries": get_day_food_entries(user_id, entry_date),
            "exercise_entries": get_day_exercise_entries(user_id, entry_date)
        }
        goal = get_user_goal(user_id)
        
        intake = sum(float(f["kcal"]) for f in logs["food_entries"])
        burned = sum(float(e["burned_kcal"]) for e in logs["exercise_entries"])
        net = intake - burned
        target = goal.get("daily_target_kcal", 2000) if goal else 2000
        remaining = target - net
        
        # Format entries
        food_entries = [{
            "id": f["id"],
            "type": "food",
            "name": f["name"],
            "calories": float(f["kcal"]),
            "time": f.get("time"),
            "quantity": float(f["quantity"]) if f.get("quantity") else None,
            "unit": f.get("unit")
        } for f in logs["food_entries"]]
        
        exercise_entries = [{
            "id": x["id"],
            "type": "exercise",
            "name": x["name"],
            "calories": float(x["burned_kcal"]),
            "time": x.get("time_minutes"),
        } for x in logs["exercise_entries"]]
        
        # Coach Advice
        coach_data = daily_coach_summary(int(intake), int(burned), target)
        
        return {
            "date": entry_date.isoformat(),
            "summary": {
                "intake_kcal": round(intake),
                "burned_kcal": round(burned),
                "net_kcal": round(net),
                "target_kcal": target,
                "remaining_kcal": round(remaining),
            },
            "coach_advice": {
                "status": coach_data["status"],
                "message": coach_data["message"]
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
        
        # Get data for month
        food_map = get_food_entries_in_range(user_id, start_date, end_date)
        ex_map = get_exercise_entries_in_range(user_id, start_date, end_date)
        
        # Get Goal
        goal = get_user_goal(user_id)
        target = float(goal.get("daily_target_kcal", 2000)) if goal else 2000.0
        
        days = []
        curr = start_date
        while curr <= end_date:
            d_str = str(curr)
            f_total = sum(f['kcal'] for f in food_map.get(d_str, []))
            e_total = sum(e['burned_kcal'] for e in ex_map.get(d_str, []))
            
            net = f_total - e_total
            status = "under_budget" if net <= target else "over_budget"
            
            days.append({
                "date": d_str,
                "status": status,
                "net_kcal": round(net),
            })
            curr += timedelta(days=1)
        
        return {
            "month": month,
            "days": days
        }
