import sys
import os
from datetime import date

# Add project root to path
sys.path.append(os.getcwd())

from backend.app.repositories.food_repo import get_day_food_entries
from backend.app.services.stats_service import StatsService

def test_repo():
    print("Testing get_day_food_entries...")
    try:
        entries = get_day_food_entries(1, date.today())
        print(f"Entries: {len(entries)}")
        print(entries)
    except Exception as e:
        print("CRASH in get_day_food_entries:", e)
        import traceback
        traceback.print_exc()

def test_stats_service():
    print("\nTesting StatsService.get_overview_stats...")
    try:
        stats = StatsService.get_overview_stats(1)
        print("Overview Stats:", stats)
    except Exception as e:
        print("CRASH in get_overview_stats:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_repo()
    test_stats_service()
