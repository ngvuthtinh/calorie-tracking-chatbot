from typing import Optional, Dict
from backend.app.db.connection import fetch_one, execute


def get_goal(user_id: int) -> Optional[Dict]:
    return fetch_one(
        "SELECT * FROM user_goal WHERE user_id = %s",
        (user_id,)
    )


def upsert_goal(
    user_id: int,
    goal_type: str,
    target_weight_kg: Optional[float] = None,
    target_delta_kg: Optional[float] = None,
    daily_target_kcal: Optional[int] = None
):
    
    existing = get_goal(user_id)

    fields = {"goal_type": goal_type}

    if target_weight_kg is not None:
        fields["target_weight_kg"] = target_weight_kg
    if target_delta_kg is not None:
        fields["target_delta_kg"] = target_delta_kg
    if daily_target_kcal is not None:
        fields["daily_target_kcal"] = daily_target_kcal

    if existing:
        set_clause = ", ".join(f"{k} = %s" for k in fields)
        values = list(fields.values()) + [user_id]

        execute(
            f"""
            UPDATE user_goal
            SET {set_clause}
            WHERE user_id = %s
            """,
            tuple(values),
        )
    else:
        columns = ", ".join(["user_id"] + list(fields))
        placeholders = ", ".join(["%s"] * (len(fields) + 1))
        values = [user_id] + list(fields.values())

        execute(
            f"""
            INSERT INTO user_goal ({columns})
            VALUES ({placeholders})
            """,
            tuple(values),
        )