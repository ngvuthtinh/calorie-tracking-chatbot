from typing import List, Dict
from datetime import date, timedelta
from backend.app.db.connection import fetch_all


def get_day_logs(user_id: int, entry_date: date) -> Dict[str, List[Dict]]:
    """
    Fetch all food & exercise logs for ONE day.
    Repo only reads DB. No calculations.
    """

    rows = fetch_all(
        """
        SELECT id
        FROM day_session
        WHERE user_id = %s AND entry_date = %s
        """,
        (user_id, entry_date),
    )

    if not rows:
        return {"food_entries": [], "exercise_entries": []}

    session_id = rows[0]["id"]

    food_entries = fetch_all(
        """
        SELECT *
        FROM food_entry
        WHERE day_session_id = %s
          AND is_deleted = 0
        ORDER BY id
        """,
        (session_id,),
    )

    exercise_entries = fetch_all(
        """
        SELECT *
        FROM exercise_entry
        WHERE day_session_id = %s
          AND is_deleted = 0
        ORDER BY id
        """,
        (session_id,),
    )

    return {
        "food_entries": food_entries,
        "exercise_entries": exercise_entries,
    }


def get_week_logs(
    user_id: int,
    start_date: date,
    end_date: date,
) -> List[Dict]:
    """
    Fetch logs for multiple days.
    Stable shape even if a day has no data.
    """

    sessions = fetch_all(
        """
        SELECT id, entry_date
        FROM day_session
        WHERE user_id = %s
          AND entry_date BETWEEN %s AND %s
        """,
        (user_id, start_date, end_date),
    )

    session_map = {s["entry_date"]: s["id"] for s in sessions}

    result = []
    days = (end_date - start_date).days + 1

    for i in range(days):
        d = start_date + timedelta(days=i)
        session_id = session_map.get(d)

        if not session_id:
            result.append({
                "date": d.isoformat(),
                "food_entries": [],
                "exercise_entries": [],
            })
            continue

        food = fetch_all(
            """
            SELECT *
            FROM food_entry
            WHERE day_session_id = %s
              AND is_deleted = 0
            ORDER BY id
            """,
            (session_id,),
        )

        exercise = fetch_all(
            """
            SELECT *
            FROM exercise_entry
            WHERE day_session_id = %s
              AND is_deleted = 0
            ORDER BY id
            """,
            (session_id,),
        )

        result.append({
            "date": d.isoformat(),
            "food_entries": food,
            "exercise_entries": exercise,
        })

    return result
