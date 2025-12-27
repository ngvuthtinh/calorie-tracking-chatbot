import sys
import os
# Add the project root to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.nlp.nlp_facade import NlpFacade
from backend.app.services.nutrition_service import estimate_intake

def test_nutrition_note():
    print("\nTesting: 'banana (200kcal)'")
    items = [{"name": "banana", "note": "200kcal"}]
    try:
        result = estimate_intake(items)
        print(f"Result: {result}")
        if result['breakdown'][0]['kcal'] == 200:
            print("SUCCESS: 200 kcal extracted from note.")
        else:
            print(f"FAILURE: Expected 200, got {result['breakdown'][0]['kcal']}.")
    except Exception as e:
        import traceback
        print(f"ERROR: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_nutrition_note()
