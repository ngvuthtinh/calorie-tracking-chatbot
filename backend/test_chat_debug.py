import sys
import os
from datetime import date

# Add project root to path
sys.path.append(os.getcwd())

from backend.app.command_service import CommandService
from backend.app.services.nutrition_service import estimate_intake

def test_chat():
    print("Testing Chat logic...")
    service = CommandService()
    
    text = "Breakfast: 2 eggs"
    print(f"Processing: '{text}'")
    
    import time
    start = time.time()
    
    try:
        result = service.handle_command("1", date.today(), text)
        duration = time.time() - start
        
        print(f"Completed in {duration:.4f} seconds")
        print("Result:", result)
        
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

def test_nutrition():
    print("\nTesting Nutrition Service...")
    items = [{"name": "egg", "qty": 2}]
    
    import time
    start = time.time()
    res = estimate_intake(items)
    duration = time.time() - start
    print(f"Nutrition completed in {duration:.4f} s")
    print(res)

if __name__ == "__main__":
    test_nutrition()
    test_chat()
