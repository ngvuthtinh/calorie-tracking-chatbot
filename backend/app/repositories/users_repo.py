from typing import Optional, Dict, Any, List
from backend.app.db.connection import fetch_one, execute, fetch_all

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

def get_all_users() -> List[Dict[str, Any]]:
    query = "SELECT * FROM users"
    return fetch_all(query)

# --- Profile ---
def get_user_profile_db(user_id: int) -> Dict[str, Any]:
    query = "SELECT * FROM user_profile WHERE user_id = %s"
    row = fetch_one(query, (user_id,))
    return dict(row) if row else {}

def upsert_user_profile(user_id: int, **kwargs) -> None:
    """
    Upsert user profile fields.
    kwargs matches column names: height_cm, weight_kg, age, gender, activity_level, target_weight_kg
    """
    if not kwargs:
        return

    # Check existence
    check_query = "SELECT user_id FROM user_profile WHERE user_id = %s"
    exists = fetch_one(check_query, (user_id,))
    
    if exists:
        # Update
        set_clauses = [f"{k} = %s" for k in kwargs.keys()]
        values = list(kwargs.values()) + [user_id]
        sql = f"UPDATE user_profile SET {', '.join(set_clauses)} WHERE user_id = %s"
        execute(sql, tuple(values))
    else:
        # Insert
        columns = ["user_id"] + list(kwargs.keys())
        placeholders = ["%s"] * len(columns)
        values = [user_id] + list(kwargs.values())
        sql = f"INSERT INTO user_profile ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        execute(sql, tuple(values))

# --- Goal ---
def get_user_goal(user_id: int) -> Dict[str, Any]:
    query = "SELECT * FROM user_goal WHERE user_id = %s"
    row = fetch_one(query, (user_id,))
    return dict(row) if row else {}

def upsert_goal(user_id: int, goal_type: str = None, daily_target_kcal: float = None, target_weight_kg: float = None, target_date = None) -> None:
    check_query = "SELECT user_id FROM user_goal WHERE user_id = %s"
    exists = fetch_one(check_query, (user_id,))
    
    updates = {}
    if goal_type: updates["goal_type"] = goal_type
    if daily_target_kcal is not None: updates["daily_target_kcal"] = daily_target_kcal
    if target_weight_kg is not None: updates["target_weight_kg"] = target_weight_kg
    if target_date is not None: updates["target_date"] = target_date
    
    if not updates:
        return

    if exists:
        set_clauses = [f"{k} = %s" for k in updates.keys()]
        values = list(updates.values()) + [user_id]
        sql = f"UPDATE user_goal SET {', '.join(set_clauses)} WHERE user_id = %s"
        execute(sql, tuple(values))
    else:
        # Insert needs both ideally, but handle partial
        columns = ["user_id"] + list(updates.keys())
        placeholders = ["%s"] * len(columns)
        values = [user_id] + list(updates.values())
        sql = f"INSERT INTO user_goal ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        execute(sql, tuple(values))
