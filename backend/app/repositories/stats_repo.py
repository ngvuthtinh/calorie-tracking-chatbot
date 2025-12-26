from typing import List, Dict, Optional
from datetime import date, timedelta
from backend.app.db.connection import fetch_all, fetch_one

def get_day_logs(user_id: int, entry_date: date) -> Dict[str, List[Dict]]:
    """
    Fetch all food_items and exercise_items for ONE day.
    """

    session = fetch_all(
        """
        SELECT id
        FROM day_session
        WHERE user_id = %s AND entry_date = %s
        """,
        (user_id, entry_date),
    )

    if not session:
        return {"food_entries": [], "exercise_entries": []}

    session_id = session[0]["id"]

    # ---- FOOD ITEMS (JOIN) ----
    food_items = fetch_all(
        """
        SELECT
            fi.id,
            fi.item_name,
            fi.qty AS quantity,
            fi.unit
        FROM food_entry fe
        JOIN food_item fi ON fi.food_entry_id = fe.id
        WHERE fe.day_session_id = %s
          AND fe.is_deleted = 0
        ORDER BY fi.id
        """,
        (session_id,),
    )

    # ---- EXERCISE ITEMS (JOIN) ----
    exercise_items = fetch_all(
        """
        SELECT
            ei.id,
            ei.ex_type AS name,
            ei.duration_min,
            ei.distance_km,
            ei.reps
        FROM exercise_entry ee
        JOIN exercise_item ei ON ei.exercise_entry_id = ee.id
        WHERE ee.day_session_id = %s
          AND ee.is_deleted = 0
        ORDER BY ei.id
        """,
        (session_id,),
    )

    return {
        "food_entries": food_items,
        "exercise_entries": exercise_items,
    }


def get_week_logs(user_id: int, start_date: date, end_date: date) -> List[Dict]:
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

def get_total_days_logged(user_id: int) -> int:
    """
    Count total number of days the user has logged something.
    """
    row = fetch_one(
        "SELECT COUNT(DISTINCT entry_date) as cnt FROM day_session WHERE user_id = %s",
        (user_id, )
    )
    return row["cnt"] if row else 0

def get_log_dates(user_id: int) -> List[date]:
    """
    Fetch all unique dates where user logged data.
    """
    rows = fetch_all(
        "SELECT DISTINCT entry_date FROM day_session WHERE user_id = %s ORDER BY entry_date DESC",
        (user_id,)
    )
    return [r["entry_date"] for r in rows]

def get_lifetime_stats(user_id: int) -> Dict[str, float]:
    """
    Efficiently calculate lifetime totals using SQL SUM.
    """
    # 1. Sum food calories
    query_food = """
        SELECT SUM(f.total_kcal) as total_intake
        FROM food_entry f
        JOIN day_session s ON f.day_session_id = s.id
        WHERE s.user_id = %s AND f.is_deleted = 0
    """
    row_food = fetch_one(query_food, (user_id,))
    total_intake = float(row_food["total_intake"] or 0)

    # 2. Sum exercise burned calories
    query_ex = """
        SELECT SUM(e.burned_kcal) as total_burned
        FROM exercise_entry e
        JOIN day_session s ON e.day_session_id = s.id
        WHERE s.user_id = %s AND e.is_deleted = 0
    """
    row_ex = fetch_one(query_ex, (user_id,))
    total_burned = float(row_ex["total_burned"] or 0)

    return {
        "total_intake": total_intake,
        "total_burned": total_burned
    }
