from app.db.connection import fetch_all
from datetime import date
import sys
import os

# Add backend to path to allow imports
sys.path.append(os.getcwd())

def verify_data():
    user_id = 1
    print(f"--- Checking Data for User {user_id} ---")
    
    # 1. Check Sessions
    sessions = fetch_all("SELECT * FROM day_session WHERE user_id = %s", (user_id,))
    print(f"\n[Day Sessions] Count: {len(sessions)}")
    for s in sessions:
        print(f" - ID: {s['id']}, Date: {s['entry_date']} (Type: {type(s['entry_date'])})")

    # 2. Check Food Entries
    if sessions:
        session_ids = [s['id'] for s in sessions]
        placeholders = ', '.join(['%s'] * len(session_ids))
        food_entries = fetch_all(f"SELECT * FROM food_entry WHERE day_session_id IN ({placeholders})", tuple(session_ids))
        print(f"\n[Food Entries] Count: {len(food_entries)}")
        for f in food_entries:
            print(f" - ID: {f['id']}, SessionID: {f['day_session_id']}, Kcal: {f['intake_kcal']}, Created: {f['created_at']}")
    else:
        print("\n[Food Entries] No sessions found.")

    # 3. Check Today
    today = date.today()
    print(f"\n[System Date] Today is: {today}")
    
    # Check if today exists in sessions
    today_session = next((s for s in sessions if str(s['entry_date']) == str(today)), None)
    if today_session:
        print(f" -> Found session for today (ID: {today_session['id']})")
    else:
        print(f" -> NO session found for today ({today})")

if __name__ == "__main__":
    verify_data()
