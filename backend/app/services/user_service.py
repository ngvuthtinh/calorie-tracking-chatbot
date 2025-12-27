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
        profile_fields = ["height_cm", "weight_kg", "age", "gender", "activity_level"]
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
        
        # New: Update target weight and target date if provided
        new_target_weight = data.get("target_weight_kg")
        new_target_date = data.get("target_date")
        
        # Determine goal_type:
        # 1. Use explicit input if provided
        # 2. Else infer from weights if available
        new_goal_type = data.get("goal_type")
        
        if not new_goal_type:
             current_weight = profile_db.get("weight_kg")
             # Use new target weight if provided, else fallback to DB
             target_weight = new_target_weight if new_target_weight is not None else goal_db.get("target_weight_kg")
             
             if current_weight is not None and target_weight is not None:
                 inferred_goal, _ = infer_goal_from_target(current_weight, target_weight)
                 new_goal_type = inferred_goal

        goal_updates = {}
        if new_goal_type:
            goal_updates["goal_type"] = new_goal_type
        if new_target_weight is not None:
            goal_updates["target_weight_kg"] = new_target_weight
        if new_target_date is not None:
            goal_updates["target_date"] = new_target_date

        # Update goal_db local dict tentatively
        goal_db.update(goal_updates)

        # Update daily target if we have goal + tdee
        current_goal_type = goal_db.get("goal_type")
        if current_goal_type and tdee > 0:
            # Get current and target weights for dynamic calculation
            current_weight = profile_db.get("weight_kg")
            target_weight = goal_db.get("target_weight_kg")
            target_date = goal_db.get("target_date")
            
            daily_target = calculate_daily_target(
                tdee, 
                current_goal_type,
                current_weight=current_weight,
                target_weight=target_weight,
                target_date=target_date
            )
            goal_updates["daily_target_kcal"] = daily_target
        
        if goal_updates:
            upsert_goal(
                user_id=user_id, 
                goal_type=goal_updates.get("goal_type"),
                target_weight_kg=goal_updates.get("target_weight_kg"),
                target_date=goal_updates.get("target_date"),
                daily_target_kcal=goal_updates.get("daily_target_kcal")
            )
            # Update local for return
            goal_db.update(goal_updates)

        return {
            "success": True,
            "message": "Profile updated successfully.",
            "profile": profile_db,
            "goal": goal_db,
            "health_metrics": health_metrics
        }
