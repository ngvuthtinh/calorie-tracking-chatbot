from typing import Any, Dict, List, Optional
from datetime import date
from decimal import Decimal

from backend.app.repositories.users_repo import (
    get_user_profile_db, upsert_user_profile, 
    upsert_goal, get_user_goal
)
from backend.app.services.health_service import calculate_health_stats
from backend.app.services.goal_service import infer_goal_from_target, calculate_daily_target

class UserService:
    """
    Service layer for User Profile and Goal operations.
    (Stats logic has been moved to StatsService)
    (Action logic has been moved to ActionService)
    """

    @staticmethod
    def get_user_profile(user_id: int) -> Dict[str, Any]:
        return get_user_profile_db(user_id)

    @staticmethod
    def update_profile(user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update profile and goal, recalculate stats.
        data keys: height_cm, weight_kg, age, gender, activity_level, goal_type, target_weight_kg
        """
        # 1. Update Profile fields
        profile_fields = ["height_cm", "weight_kg", "age", "gender", "activity_level", "target_weight_kg"]
        profile_update = {k: data[k] for k in profile_fields if k in data}
        
        if profile_update:
            upsert_user_profile(user_id, **profile_update)
            
        # 2. Recalculate Health Stats (BMR, TDEE)
        # Fetch fresh data to ensure we have all fields
        profile_db = get_user_profile_db(user_id)
        
        health_metrics = calculate_health_stats(profile_db)
        tdee = health_metrics.get("tdee", 0)
        
        # 3. Update Goal / Daily Target
        goal_db = get_user_goal(user_id) or {}
        
        # If user explicitly sets goal_type or we infer it
        if "goal_type" in data:
            goal_db["goal_type"] = data["goal_type"]
            
        # Update daily target if we have goal + tdee
        if goal_db.get("goal_type") and tdee > 0:
            daily_target = calculate_daily_target(tdee, goal_db["goal_type"])
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
