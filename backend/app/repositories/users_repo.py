from typing import Optional
from backend.app.db.connection import fetch_one, execute

def get_or_create_user(email: str) -> int:
    """
    Get user ID by email. If user does not exist, create a new one.
    """
    query_check = "SELECT id FROM users WHERE email = %s"
    row = fetch_one(query_check, (email,))
    
    if row:
        return row['id']
    
    query_insert = "INSERT INTO users (email) VALUES (%s)"
    new_id = execute(query_insert, (email,))
    return new_id

def update_user_profile(user_id: int, profile_data: dict):
    """
    Update or create user profile.
    profile_data keys: height_cm, weight_kg, age, gender, activity_level
    """
    # Prepare values, defaulting to None if key missing
    height = profile_data.get("height_cm")
    weight = profile_data.get("weight_kg")
    age = profile_data.get("age")
    gender = profile_data.get("gender")
    activity = profile_data.get("activity_level")

    query = """
        INSERT INTO user_profile (user_id, height_cm, weight_kg, age, gender, activity_level)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            height_cm = VALUES(height_cm),
            weight_kg = VALUES(weight_kg),
            age = VALUES(age),
            gender = VALUES(gender),
            activity_level = VALUES(activity_level)
    """
    execute(query, (user_id, height, weight, age, gender, activity))

def update_user_goal(user_id: int, goal_data: dict):
    """
    Update or create user goal.
    goal_data keys: goal_type, target_weight_kg, target_delta_kg, daily_target_kcal
    """
    g_type = goal_data.get("goal_type")
    t_weight = goal_data.get("target_weight_kg")
    t_delta = goal_data.get("target_delta_kg")
    # unit removed, default to kg
    daily = goal_data.get("daily_target_kcal")

    query = """
        INSERT INTO user_goal (user_id, goal_type, target_weight_kg, target_delta_kg, daily_target_kcal)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            goal_type = VALUES(goal_type),
            target_weight_kg = VALUES(target_weight_kg),
            target_delta_kg = VALUES(target_delta_kg),
            daily_target_kcal = VALUES(daily_target_kcal)
    """
    execute(query, (user_id, g_type, t_weight, t_delta, daily))
