
import requests
import datetime
from pprint import pprint

BASE_URL = "http://localhost:8000/api"

def test_day_view():
    today = datetime.date.today().isoformat()
    print(f"\n--- Testing Day View for {today} ---")
    resp = requests.get(f"{BASE_URL}/day/{today}")
    
    if resp.status_code == 200:
        print("Success!")
        pprint(resp.json())
    else:
        print(f"Failed: {resp.status_code}")
        print(resp.text)

def test_month_view():
    today = datetime.date.today()
    month_str = f"{today.year}-{today.month:02d}"
    print(f"\n--- Testing Month View for {month_str} ---")
    # Pass month as query parameter
    resp = requests.get(f"{BASE_URL}/calendar/month?month={month_str}")
    
    if resp.status_code == 200:
        print("Success!")
        data = resp.json()
        print(f"Month: {data['month']}")
        print(f"Days found: {len(data['days'])}")
        if data['days']:
            print("First day sample:", data['days'][0])
    else:
        print(f"Failed: {resp.status_code}")
        print(resp.text)

def test_week_view():
    today = datetime.date.today().isoformat()
    print(f"\n--- Testing Week View for {today} ---")
    # Note: parameter name is 'date', not 'week'
    resp = requests.get(f"{BASE_URL}/calendar/week?date={today}")
    
    if resp.status_code == 200:
        print("Success!")
        data = resp.json()
        print(f"Week Start: {data['week_start']}")
        print(f"Week End: {data['week_end']}")
        print(f"Days found: {len(data['days'])}")
    else:
        print(f"Failed: {resp.status_code}")
        print(resp.text)

if __name__ == "__main__":
    try:
        test_day_view()
        test_month_view()
        test_week_view()
    except Exception as e:
        print(f"An error occurred: {e}")
