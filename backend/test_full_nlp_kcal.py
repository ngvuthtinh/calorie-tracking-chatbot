import sys
import os
# Add the project root to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.nlp.nlp_facade import NlpFacade
from backend.app.services.nutrition_service import estimate_intake

def test_full_nlp_kcal(text):
    print(f"\nTesting Text: '{text}'")
    try:
        frames = NlpFacade.parse(text)
        print(f"Frames: {frames}")
        for frame in frames:
            if frame['intent'] == 'log_food':
                items = frame['data'].get('items', [])
                result = estimate_intake(items)
                print(f"Estimation Result: {result}")
                for b in result['breakdown']:
                    print(f"  - Item: {b['name']}, Kcal: {b['kcal']}, Status: {b['status']}")
    except Exception as e:
        import traceback
        print(f"ERROR: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_full_nlp_kcal("Lunch: banana (200kcal)")
    test_full_nlp_kcal("Breakfast: 2 eggs (150 kcal)")
    test_full_nlp_kcal("Drink: 50ml coffe (200kcal)")
    test_full_nlp_kcal("Eat: 1 apple (100 kcal)")
