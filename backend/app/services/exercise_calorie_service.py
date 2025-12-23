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
from app.repositories.exercise_catalog_repo import ExerciseRepo


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



# Average pace estimates for distance-to-duration conversion (km/h)
AVERAGE_PACE = {
    "run": 10.0,      # 10 km/h = 6 min/km
    "walk": 5.0,      # 5 km/h = 12 min/km
    "cycling": 20.0,  # 20 km/h = 3 min/km
    "swim": 3.0,      # 3 km/h (swimming is slower)
}

# Default weight in kg when user profile doesn't have weight
DEFAULT_WEIGHT_KG = 70.0



def estimate_burn(items: List[Dict[str, Any]], profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Estimate total calories burned for a list of exercise items.
    
    Args:
        items: List of exercise items, each containing:
            - type: str (exercise type: run, walk, cycling, swim, plank, pushups, squats, lunges)
            - One of: duration_min, distance_km, or reps
            - intensity: Optional[str] ("light", "moderate", "heavy") - defaults to "moderate"
        profile: Optional user profile dict with 'weight' field (in kg)
        
    Returns:
        Dict with:
            - burned_kcal: float (total calories burned)
            - breakdown: List[Dict] (per-item calorie breakdown)
            
    Example:
        >>> items = [
        ...     {"type": "run", "duration_min": 30, "intensity": "heavy"},
        ...     {"type": "pushups", "reps": 20}
        ... ]
        >>> profile = {"weight": 70}
        >>> result = estimate_burn(items, profile)
        >>> result['burned_kcal']  # ~437.5 kcal (heavy run burns more)
    """
    if not items:
        return {"burned_kcal": 0.0, "breakdown": []}
    
    # Get user weight or use default
    weight_kg = _get_user_weight(profile)
    
    breakdown = []
    total_kcal = 0.0
    
    for item in items:
        exercise_type = item.get("type", "unknown")
        intensity = item.get("intensity", "moderate")  # Default to moderate
        kcal = 0.0
        measurement = ""
        
        # Duration-based exercises
        if "duration_min" in item and item["duration_min"] is not None:
            duration_min = item["duration_min"]
            kcal = _estimate_duration_calories(exercise_type, duration_min, weight_kg, intensity)
            measurement = f"{duration_min}min"
        
        # Distance-based exercises
        elif "distance_km" in item and item["distance_km"] is not None:
            distance_km = item["distance_km"]
            # Convert distance to duration, then calculate calories
            duration_min = _estimate_duration_from_distance(exercise_type, distance_km)
            kcal = _estimate_duration_calories(exercise_type, duration_min, weight_kg, intensity)
            measurement = f"{distance_km}km"
        
        # Reps-based exercises
        elif "reps" in item and item["reps"] is not None:
            reps = item["reps"]
            kcal = _estimate_reps_calories(exercise_type, reps)
            measurement = f"{reps} reps"
        
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


def _get_user_weight(profile: Optional[Dict[str, Any]]) -> float:
    """
    Get user weight from profile or return default.
    
    Args:
        profile: User profile dict
        
    Returns:
        Weight in kg (defaults to 70kg if not available)
    """
    if not profile:
        return DEFAULT_WEIGHT_KG
    
    weight = profile.get("weight")
    if weight is None or weight <= 0:
        return DEFAULT_WEIGHT_KG
    
    return float(weight)


def _estimate_duration_calories(exercise_type: str, duration_min: float, weight_kg: float, intensity: str = "moderate") -> float:
    """
    Estimate calories burned for duration-based exercise using MET formula.
    
    Formula: kcal = MET × weight_kg × (duration_min / 60)
    
    Args:
        exercise_type: Type of exercise
        duration_min: Duration in minutes
        weight_kg: User weight in kg
        intensity: Intensity level ("light", "moderate", "heavy")
        
    Returns:
        Estimated calories burned
    """
    met = _get_met_value(exercise_type, intensity)
    duration_hours = duration_min / 60.0
    kcal = met * weight_kg * duration_hours
    return kcal


def _estimate_reps_calories(exercise_type: str, reps: int) -> float:
    """
    Estimate calories burned for reps-based exercise.
    
    Args:
        exercise_type: Type of exercise
        reps: Number of repetitions
        
    Returns:
        Estimated calories burned
    """
    kcal_per_rep = _get_reps_calorie(exercise_type)
    kcal = kcal_per_rep * reps
    return kcal


def _estimate_duration_from_distance(exercise_type: str, distance_km: float) -> float:
    """
    Convert distance to estimated duration based on average pace.
    
    Args:
        exercise_type: Type of exercise
        distance_km: Distance in kilometers
        
    Returns:
        Estimated duration in minutes
    """
    pace_kmh = AVERAGE_PACE.get(exercise_type, 5.0)  # Default to walking pace
    duration_hours = distance_km / pace_kmh
    duration_min = duration_hours * 60.0
    return duration_min


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

