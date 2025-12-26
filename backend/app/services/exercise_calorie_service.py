"""
Exercise Calorie Estimation Service

Estimates burned calories for exercises using:
- MET (Metabolic Equivalent of Task) values for duration-based exercises
- Intensity levels (light, moderate, heavy) for more accurate estimates
- Simple approximations for reps-based exercises
- User weight when available for better accuracy

Data is loaded from the exercise_catalog database table with in-memory caching.
"""

from typing import Any, Dict, List, Optional
from backend.app.repositories.exercise_catalog_repo import ExerciseRepo


# In-memory cache for exercise data (lazy loaded from database)
_exercise_cache: Optional[Dict[str, Any]] = None


def _load_exercise_cache() -> Dict[str, Any]:
    """
    Load exercise data from database into memory cache.
    
    This is called lazily on first use to avoid database queries at import time.
    Cache structure:
    {
        "met_values": {exercise_name: {intensity: met_value}},
        "calories_per_rep": {exercise_name: kcal_per_rep}
    }
    
    Returns:
        Dictionary containing MET values and calories per rep
    """
    global _exercise_cache
    
    if _exercise_cache is not None:
        return _exercise_cache
    
    # Initialize cache structure
    cache = {
        "met_values": {},
        "calories_per_rep": {}
    }
    
    try:
        # Load all exercises from database
        repo = ExerciseRepo()
        exercises = repo.get_all_exercises()
        
        for exercise in exercises:
            name = exercise["name_normalized"]
            
            # Cache MET values if available
            if any([exercise.get("met_light"), exercise.get("met_moderate"), exercise.get("met_heavy")]):
                cache["met_values"][name] = {}
                if exercise.get("met_light"):
                    cache["met_values"][name]["light"] = float(exercise["met_light"])
                if exercise.get("met_moderate"):
                    cache["met_values"][name]["moderate"] = float(exercise["met_moderate"])
                if exercise.get("met_heavy"):
                    cache["met_values"][name]["heavy"] = float(exercise["met_heavy"])
            
            # Cache calories per rep if available
            if exercise.get("kcal_per_rep"):
                cache["calories_per_rep"][name] = float(exercise["kcal_per_rep"])
    
    except Exception as e:
        # If database is unavailable, use fallback values
        print(f"Warning: Could not load exercise data from database: {e}")
        print("Using fallback values.")
        cache = _get_fallback_cache()
    
    _exercise_cache = cache
    return _exercise_cache


def _get_fallback_cache() -> Dict[str, Any]:
    """
    Get fallback exercise data if database is unavailable.
    
    Returns:
        Dictionary with minimal exercise data for basic functionality
    """
    return {
        "met_values": {
            "run": {"light": 6.0, "moderate": 9.0, "heavy": 12.5},
            "walk": {"light": 2.5, "moderate": 3.5, "heavy": 5.0},
            "cycling": {"light": 5.5, "moderate": 7.5, "heavy": 10.0},
            "swim": {"light": 6.0, "moderate": 8.0, "heavy": 11.0},
            "plank": {"light": 3.0, "moderate": 4.0, "heavy": 5.0},
        },
        "calories_per_rep": {
            "pushups": 0.5,
            "squats": 0.6,
            "lunges": 0.6,
        }
    }



from backend.app.services.calorie_strategies import DurationStrategy, DistanceStrategy, RepsStrategy

# Strategies (Stateless, so we can reuse instances)
_duration_strategy = DurationStrategy()
_distance_strategy = DistanceStrategy()
_reps_strategy = RepsStrategy()
DEFAULT_WEIGHT_KG = 70.0

import re

# ... existing code ...

def estimate_burn(items: List[Dict[str, Any]], profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Estimate total calories burned for a list of exercise items using Strategy Pattern.
    """
    if not items:
        return {"burned_kcal": 0.0, "breakdown": []}
    
    weight_kg = _get_user_weight(profile)
    
    breakdown = []
    total_kcal = 0.0
    
    for item in items:
        exercise_type = item.get("type", "unknown")
        intensity = item.get("intensity", "moderate")
        kcal = 0.0
        measurement = ""
        
        # Check if calorie is explicitly provided in note or 'kcal' field
        # "kcal in note" logic as requested
        note = item.get("note", "")
        extracted_kcal = _extract_kcal_from_note(str(note)) if note else None
        
        if item.get("kcal"):
             # Trust explicit kcal field if present
             kcal = float(item["kcal"])
             measurement = "manual"
        elif extracted_kcal is not None:
             # Trust kcal found in note
             kcal = extracted_kcal
             measurement = "from note"
        
        # Default strategy calculation if no manual override
        elif "duration_min" in item and item["duration_min"] is not None:
             met = _get_met_value(exercise_type, intensity)
             kcal = _duration_strategy.calculate(item, weight_kg, met)
             measurement = f"{item['duration_min']}min"
             
        elif "distance_km" in item and item["distance_km"] is not None:
             met = _get_met_value(exercise_type, intensity)
             kcal = _distance_strategy.calculate(item, weight_kg, met)
             measurement = f"{item['distance_km']}km"
             
        elif "reps" in item and item["reps"] is not None:
             kcal_per_rep = _get_reps_calorie(exercise_type)
             kcal = _reps_strategy.calculate(item, weight_kg, kcal_per_rep)
             measurement = f"{item['reps']} reps"
             
        total_kcal += kcal
        
        breakdown.append({
            "type": exercise_type,
            "measurement": measurement,
            "kcal": round(kcal, 1)
        })
    
    return {
        "burned_kcal": round(total_kcal, 1),
        "breakdown": breakdown
    }

def _extract_kcal_from_note(note_text: str) -> Optional[float]:
    """
    Extract calorie value from note text.
    Patterns: "300kcal", "300 kcal", "300 cal", "300 calories"
    Returns first match or None.
    """
    # Regex for number followed by optional space and kcal/cal/calories
    pattern = r"(\d+(?:\.\d+)?)\s*(?:kcal|cal|calories)\b"
    match = re.search(pattern, note_text, re.IGNORECASE)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None


def _get_user_weight(profile: Optional[Dict[str, Any]]) -> float:
    if not profile:
        return DEFAULT_WEIGHT_KG
    weight = profile.get("weight")
    # Handle potentially string values or missing stats
    try:
        if weight:
             w_val = float(weight)
             if w_val > 0:
                 return w_val
    except ValueError:
        pass
    return DEFAULT_WEIGHT_KG


def _get_met_value(exercise_type: str, intensity: str = "moderate") -> float:
    """
    Get MET value for exercise type and intensity level from database.
    
    Args:
        exercise_type: Type of exercise
        intensity: Intensity level ("light", "moderate", "heavy")
        
    Returns:
        MET value (defaults to 3.5 for unknown exercises)
    """
    exercise_type_lower = exercise_type.lower()
    intensity_lower = intensity.lower()
    
    # Load cache from database if needed
    cache = _load_exercise_cache()
    met_values = cache.get("met_values", {})
    
    # Try to get intensity-specific MET value
    if exercise_type_lower in met_values:
        intensities = met_values[exercise_type_lower]
        if intensity_lower in intensities:
            return intensities[intensity_lower]
        # Default to moderate if intensity not found
        return intensities.get("moderate", 3.5)
    
    # Fallback for unknown exercises
    return 3.5



def _get_reps_calorie(exercise_type: str) -> float:
    """
    Get calorie burn per rep for exercise type from database.
    
    Args:
        exercise_type: Type of exercise
        
    Returns:
        Calories per rep (defaults to 0.3 for unknown exercises)
    """
    exercise_type_lower = exercise_type.lower()
    
    # Load cache from database if needed
    cache = _load_exercise_cache()
    calories_per_rep = cache.get("calories_per_rep", {})
    
    return calories_per_rep.get(exercise_type_lower, 0.3)

