from typing import Dict, Optional

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """
    Calculate Body Mass Index (BMI).
    Formula: weight (kg) / [height (m)]^2
    """
    if height_cm <= 0:
        return 0.0
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)

def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation.
    Men: 10 * weight(kg) + 6.25 * height(cm) - 5 * age(y) + 5
    Women: 10 * weight(kg) + 6.25 * height(cm) - 5 * age(y) - 161
    """
    base_bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
    
    # Normalize gender
    g = gender.lower().strip()
    if g in ["male", "m", "nam"]:
        return round(base_bmr + 5, 2)
    elif g in ["female", "f", "nu", "nữ"]:
        return round(base_bmr - 161, 2)
    
    # Default to male formula if unknown, or average? Sticking to male as base or explicit check.
    # For safety/precision, if unknown, maybe return 0 or an error? 
    # Let's fallback to male formula - 80 (avg between +5 and -161 is -78) approximately.
    return round(base_bmr + 5, 2) 

def get_activity_multiplier(activity_level: str) -> float:
    """
    Map activity level string to multiplier.
    References: Harris-Benedict revised.
    """
    levels = {
        "sedentary": 1.2,      # Little or no exercise
        "light": 1.375,        # Light exercise 1-3 days/week
        "moderate": 1.55,      # Moderate exercise 3-5 days/week
        "active": 1.725,       # Hard exercise 6-7 days/week
        "very_active": 1.9     # Very hard exercise & physical job
    }
    key = activity_level.lower().strip()
    return levels.get(key, 1.2) # Default to sedentary

def calculate_tdee(bmr: float, activity_level: str) -> float:
    """
    Calculate Total Daily Energy Expenditure (TDEE).
    Formula: BMR * Activity Multiplier
    """
    multiplier = get_activity_multiplier(activity_level)
    return round(bmr * multiplier, 2)

def calculate_health_stats(profile: Dict) -> Dict:
    def _extract_number(val):
        if isinstance(val, (int, float)):
            return float(val)
        if isinstance(val, str):
            try:
                return float(val.split()[0])
            except (ValueError, IndexError):
                return 0.0
        return 0.0

    weight = _extract_number(profile.get("weight_kg") or profile.get("weight"))
    height = _extract_number(profile.get("height_cm") or profile.get("height"))
    age = int(_extract_number(profile.get("age")))
    
    gender = str(profile.get("gender", "male"))
    activity = str(profile.get("activity_level", "sedentary"))

    if weight <= 0 or height <= 0:
        return {"bmi": 0, "bmr": 0, "tdee": 0}

    bmi = calculate_bmi(weight, height)
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity)

    return {
        "bmi": bmi,
        "bmr": bmr,
        "tdee": tdee
    }
