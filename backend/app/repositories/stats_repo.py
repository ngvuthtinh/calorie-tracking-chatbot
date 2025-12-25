from typing import List, Dict
from datetime import date, timedelta
from backend.app.db.connection import fetch_all

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

def get_week_logs(user_id: int, reference_date: str):
    """
    Return list of day summaries for the week containing reference_date.
    reference_date: YYYY-MM-DD
    """
    import datetime
    ref = datetime.date.fromisoformat(reference_date)
    start_date = ref - timedelta(days=ref.weekday())  # Monday
    end_date = start_date + timedelta(days=6)         # Sunday

    query = """
        SELECT ds.entry_date,
               COALESCE(SUM(
                   CASE
                       WHEN xi.reps > 0 THEN xi.reps * x.kcal_per_rep
                       ELSE xi.duration_min * x.met_light * up.weight_kg / 60
                   END
               ), 0) AS burned_kcal,
               COALESCE(SUM(fi.qty * fc.kcal_per_unit / 100), 0) AS intake_kcal,
               COALESCE(ug.daily_target_kcal, 0) AS target_kcal
        FROM day_session ds
        LEFT JOIN food_entry fe ON fe.day_session_id = ds.id
        LEFT JOIN food_item fi ON fi.food_entry_id = fe.id
        LEFT JOIN food_catalog fc ON fc.name_normalized = LOWER(fi.item_name)
        LEFT JOIN exercise_entry xe ON xe.day_session_id = ds.id
        LEFT JOIN exercise_item xi ON xi.exercise_entry_id = xe.id
        LEFT JOIN exercise_catalog x ON x.id = xi.catalog_exercise_id
        LEFT JOIN user_profile up ON up.user_id = %s
        LEFT JOIN user_goal ug ON ug.user_id = %s
        WHERE ds.entry_date BETWEEN %s AND %s
        GROUP BY ds.entry_date, ug.daily_target_kcal, up.weight_kg
        ORDER BY ds.entry_date
    """
    return fetch_all(query, (user_id, user_id, start_date, end_date))


def get_month_logs(user_id: int, month: str):
    """
    Return list of day summaries for a given month.
    month: YYYY-MM
    """
    import datetime
    from calendar import monthrange

    year, mon = map(int, month.split("-"))
    start_date = datetime.date(year, mon, 1)
    end_date = datetime.date(year, mon, monthrange(year, mon)[1])

    query = """
        SELECT ds.entry_date,
               COALESCE(SUM(
                   CASE
                       WHEN xi.reps > 0 THEN xi.reps * x.kcal_per_rep
                       ELSE xi.duration_min * x.met_light * up.weight_kg / 60
                   END
               ), 0) AS burned_kcal,
               COALESCE(SUM(fi.qty * fc.kcal_per_unit / 100), 0) AS intake_kcal,
               COALESCE(ug.daily_target_kcal, 0) AS target_kcal
        FROM day_session ds
        LEFT JOIN food_entry fe ON fe.day_session_id = ds.id
        LEFT JOIN food_item fi ON fi.food_entry_id = fe.id
        LEFT JOIN food_catalog fc ON fc.name_normalized = LOWER(fi.item_name)
        LEFT JOIN exercise_entry xe ON xe.day_session_id = ds.id
        LEFT JOIN exercise_item xi ON xi.exercise_entry_id = xe.id
        LEFT JOIN exercise_catalog x ON x.id = xi.catalog_exercise_id
        LEFT JOIN user_profile up ON up.user_id = %s
        LEFT JOIN user_goal ug ON ug.user_id = %s
        WHERE ds.entry_date BETWEEN %s AND %s
        GROUP BY ds.entry_date, ug.daily_target_kcal, up.weight_kg
        ORDER BY ds.entry_date
    """

    return fetch_all(query, (user_id, user_id, start_date, end_date))