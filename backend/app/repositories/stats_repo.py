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


def get_month_logs(user_id: int, year: int, month: int) -> List[Dict]:
    """
    Fetch per-day net calories for a given month.
    Repo only reads DB. No business logic.
    """

    rows = fetch_all(
        """
        SELECT
            ds.entry_date AS date,
            COALESCE(SUM(fc.kcal_per_unit * IFNULL(fi.qty, 1)), 0) AS intake_kcal,
            COALESCE(SUM(
                CASE
                    WHEN ei.duration_min IS NOT NULL
                    THEN ec.met_moderate * up.weight_kg * (ei.duration_min / 60)
                    ELSE 0
                END
            ), 0) AS burned_kcal
        FROM day_session ds
        LEFT JOIN food_entry fe 
            ON fe.day_session_id = ds.id AND fe.is_deleted = 0
        LEFT JOIN food_item fi 
            ON fi.food_entry_id = fe.id
        LEFT JOIN food_catalog fc 
            ON fc.id = fi.catalog_food_id
        LEFT JOIN exercise_entry ee 
            ON ee.day_session_id = ds.id AND ee.is_deleted = 0
        LEFT JOIN exercise_item ei 
            ON ei.exercise_entry_id = ee.id
        LEFT JOIN exercise_catalog ec 
            ON ec.id = ei.catalog_exercise_id
        LEFT JOIN user_profile up 
            ON up.user_id = ds.user_id
        WHERE ds.user_id = %s
          AND YEAR(ds.entry_date) = %s
          AND MONTH(ds.entry_date) = %s
        GROUP BY ds.entry_date
        ORDER BY ds.entry_date
        """,
        (user_id, year, month),
    )

    result = []
    for r in rows:
        net = (r["intake_kcal"] or 0) - (r["burned_kcal"] or 0)
        result.append({
            "date": r["date"].isoformat(),
            "net_kcal": round(net),
        })

    return result
