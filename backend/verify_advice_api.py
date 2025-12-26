
import sys
import os
from datetime import date
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.services.user_service import UserService

def verify():
    user_id = 1
    today = date.today()
    
    print("-" * 20)
    print(f"Testing get_day_view_api for user {user_id} on {today}")
    res_day_view = UserService.get_day_view_api(user_id, today)
    if "coach_advice" in res_day_view:
        print("SUCCESS: 'coach_advice' found in get_day_view_api")
        print(res_day_view["coach_advice"])
    else:
        print("FAILURE: 'coach_advice' NOT found in get_day_view_api")
        
    print("-" * 20)
    print(f"Testing get_summary_today for user {user_id} on {today}")
    res_summary = UserService.get_summary_today(user_id, today)
    # result is nested in res_summary["result"]
    result_data = res_summary.get("result", {})
    if "coach_advice" in result_data:
        print("SUCCESS: 'coach_advice' found in get_summary_today result")
        print(result_data["coach_advice"])
    else:
        print("FAILURE: 'coach_advice' NOT found in get_summary_today result")
        print("Result keys:", result_data.keys())

if __name__ == "__main__":
    verify()
