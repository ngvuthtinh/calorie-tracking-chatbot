from datetime import date
from backend.app.services.stats_service import StatsService
import json

def test_day_view():
    user_id = 1 # Assuming user 1
    today = date.today()
    
    print(f"Testing Day View for user {user_id} on {today}")
    result = StatsService.get_day_view_api(user_id, today)
    
    print("\nFood Entries:")
    for f in result.get('food_entries', []):
        print(f"  - {f['name']} (Code: {f.get('entry_code')})")
        
    print("\nExercise Entries:")
    for x in result.get('exercise_entries', []):
        print(f"  - {x['name']} (Code: {x.get('entry_code')})")

    # If they are empty, let's try to find a day with entries
    if not result.get('food_entries') and not result.get('exercise_entries'):
        print("\nSearching for a day with entries...")
        from backend.app.repositories.day_session_repo import get_user_session_dates
        dates = get_user_session_dates(user_id)
        if dates:
            for d in dates[:5]:
                print(f"\nChecking date: {d}")
                res = StatsService.get_day_view_api(user_id, d)
                for f in res.get('food_entries', []):
                    print(f"  - {f['name']} (Code: {f.get('entry_code')})")
                for x in res.get('exercise_entries', []):
                    print(f"  - {x['name']} (Code: {x.get('entry_code')})")
        else:
            print("No sessions found for user.")

if __name__ == "__main__":
    test_day_view()
