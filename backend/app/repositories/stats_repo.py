from typing import List, Dict, Optional
from datetime import date, timedelta
from backend.app.db.connection import fetch_all, fetch_one

def get_day_logs(user_id: int, entry_date: date) -> Dict[str, List[Dict]]:
    """
    Fetch all food_entries and exercise_entries for ONE day, grouped by entry with their items.
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

    # ---- FOOD ENTRIES (with items) ----
    food_entries_raw = fetch_all(
        """
        SELECT
            fe.id,
            fe.entry_code,
            fe.meal,
            fe.action,
            fe.intake_kcal
        FROM food_entry fe
        WHERE fe.day_session_id = %s
          AND fe.is_deleted = 0
        ORDER BY fe.id
        """,
        (session_id,),
    )
    
    # Get all food items for this session
    food_items_raw = fetch_all(
        """
        SELECT
            fi.id,
            fi.food_entry_id,
            fi.item_name,
            fi.qty,
            fi.unit,
            fi.kcal
        FROM food_item fi
        JOIN food_entry fe ON fi.food_entry_id = fe.id
        WHERE fe.day_session_id = %s
          AND fe.is_deleted = 0
        ORDER BY fi.id
        """,
        (session_id,),
    )
    
    # Group items by entry
    food_items_by_entry = {}
    for item in food_items_raw:
        entry_id = item["food_entry_id"]
        if entry_id not in food_items_by_entry:
            food_items_by_entry[entry_id] = []
        food_items_by_entry[entry_id].append({
            "name": item["item_name"],
            "qty": float(item["qty"]) if item["qty"] else None,
            "unit": item["unit"],
            "kcal": float(item["kcal"]) if item["kcal"] else 0
        })
    
    # Build food entries with items
    food_entries = []
    for entry in food_entries_raw:
        food_entries.append({
            "id": entry["id"],
            "entry_code": entry["entry_code"],
            "meal": entry["meal"],
            "action": entry["action"],
            "intake_kcal": float(entry["intake_kcal"]) if entry["intake_kcal"] else 0,
            "items": food_items_by_entry.get(entry["id"], [])
        })

    # ---- EXERCISE ENTRIES (with items) ----
    exercise_entries_raw = fetch_all(
        """
        SELECT
            ee.id,
            ee.entry_code,
            ee.burned_kcal
        FROM exercise_entry ee
        WHERE ee.day_session_id = %s
          AND ee.is_deleted = 0
        ORDER BY ee.id
        """,
        (session_id,),
    )
    
    # Get all exercise items for this session
    exercise_items_raw = fetch_all(
        """
        SELECT
            ei.id,
            ei.exercise_entry_id,
            ei.ex_type,
            ei.duration_min,
            ei.distance_km,
            ei.reps
        FROM exercise_item ei
        JOIN exercise_entry ee ON ei.exercise_entry_id = ee.id
        WHERE ee.day_session_id = %s
          AND ee.is_deleted = 0
        ORDER BY ei.id
        """,
        (session_id,),
    )
    
    # Group items by entry
    exercise_items_by_entry = {}
    for item in exercise_items_raw:
        entry_id = item["exercise_entry_id"]
        if entry_id not in exercise_items_by_entry:
            exercise_items_by_entry[entry_id] = []
        exercise_items_by_entry[entry_id].append({
            "type": item["ex_type"],
            "duration_min": float(item["duration_min"]) if item["duration_min"] else None,
            "distance_km": float(item["distance_km"]) if item["distance_km"] else None,
            "reps": int(item["reps"]) if item["reps"] else None
        })
    
    # Build exercise entries with items
    exercise_entries = []
    for entry in exercise_entries_raw:
        exercise_entries.append({
            "id": entry["id"],
            "entry_code": entry["entry_code"],
            "burned_kcal": float(entry["burned_kcal"]) if entry["burned_kcal"] else 0,
            "items": exercise_items_by_entry.get(entry["id"], [])
        })

    return {
        "food_entries": food_entries,
        "exercise_entries": exercise_entries,
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
        SELECT SUM(f.intake_kcal) as total_intake
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

def get_period_stats(user_id: int, start_date: date, end_date: date) -> List[Dict]:
    """
    Fetch aggregated stats (intake, burned, target) for each day in a date range.
    Efficiently uses SQL grouping.
    """
    days = (end_date - start_date).days + 1
    
    # 1. Get all sessions in range
    sessions = fetch_all(
        """
        SELECT id, entry_date
        FROM day_session
        WHERE user_id = %s
          AND entry_date BETWEEN %s AND %s
        """,
        (user_id, start_date, end_date),
    )
    session_map = {s["entry_date"]: s for s in sessions}

    # 2. Pre-fetch all food totals per session
    food_totals = fetch_all(
        """
        SELECT day_session_id, SUM(intake_kcal) as intake
        FROM food_entry
        WHERE day_session_id IN (
            SELECT id FROM day_session 
            WHERE user_id = %s AND entry_date BETWEEN %s AND %s
        ) AND is_deleted = 0
        GROUP BY day_session_id
        """,
        (user_id, start_date, end_date)
    )
    food_map = {f["day_session_id"]: float(f["intake"] or 0) for f in food_totals}

    # 3. Pre-fetch all exercise totals per session
    ex_totals = fetch_all(
        """
        SELECT day_session_id, SUM(burned_kcal) as burned
        FROM exercise_entry
        WHERE day_session_id IN (
            SELECT id FROM day_session 
            WHERE user_id = %s AND entry_date BETWEEN %s AND %s
        ) AND is_deleted = 0
        GROUP BY day_session_id
        """,
        (user_id, start_date, end_date)
    )
    ex_map = {e["day_session_id"]: float(e["burned"] or 0) for e in ex_totals}

    # 4. Build result list filling in gaps
    result = []
    from backend.app.repositories.goal_repo import get_goal
    
    # Fallback target if no session exists
    current_goal = get_goal(user_id)
    default_target = current_goal["daily_target_kcal"] if current_goal else 2000

    for i in range(days):
        d = start_date + timedelta(days=i)
        
        sess = session_map.get(d)
        if sess:
            sid = sess["id"]
            intake = food_map.get(sid, 0.0)
            burned = ex_map.get(sid, 0.0)
            target = float(default_target)
        else:
            intake = 0.0
            burned = 0.0
            target = float(default_target)
            
        result.append({
            "entry_date": d,
            "intake_kcal": intake,
            "burned_kcal": burned,
            "target_kcal": target
        })
        
    return result
