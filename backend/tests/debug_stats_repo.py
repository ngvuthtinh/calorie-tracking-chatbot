
import sys
import os

# Add root to sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(root_path)

print(f"Root path added: {root_path}")
print("Contents of root path:")
try:
    print(os.listdir(root_path))
except Exception as e:
    print(e)

from backend.app.repositories.stats_repo import get_period_stats
from datetime import date, timedelta

def test_repo():
    print("Testing get_period_stats...")
    today = date(2025, 12, 26) # Use specific date for consistent testing
    start = date(today.year, today.month, 1)
    end = today 
    
    print(f"Range: {start} to {end}")
    try:
        results = get_period_stats(1, start, end)
        print("Success!")
        print(f"Got {len(results)} results")
        if results:
            print("First day sample:", results[0])
    except Exception as e:
        print("Caught exception:")
        print(e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_repo()
