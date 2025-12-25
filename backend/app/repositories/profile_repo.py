from typing import Optional, Dict
from backend.app.db.connection import fetch_one, execute


def get_profile(user_id: int) -> Optional[Dict]:
    return fetch_one(
        """
        SELECT user_id, height_cm, weight_kg, age, gender, activity_level
        FROM user_profile
        WHERE user_id = %s
        """,
        (user_id,)
    )


def upsert_profile(
    user_id: int,
    height_cm: Optional[int] = None,
    weight_kg: Optional[float] = None,
    age: Optional[int] = None,
    gender: Optional[str] = None,
    activity_level: Optional[str] = None,
):
    existing = get_profile(user_id) or {}

    execute(
        """
        INSERT INTO user_profile (
            user_id, height_cm, weight_kg, age, gender, activity_level
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            height_cm = COALESCE(VALUES(height_cm), height_cm),
            weight_kg = COALESCE(VALUES(weight_kg), weight_kg),
            age = COALESCE(VALUES(age), age),
            gender = COALESCE(VALUES(gender), gender),
            activity_level = COALESCE(VALUES(activity_level), activity_level)
        """,
        (
            user_id,
            height_cm,
            weight_kg,
            age,
            gender,
            activity_level,
        ),
    )
