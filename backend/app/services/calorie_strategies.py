from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

# Average pace estimates for distance-to-duration conversion (km/h)
AVERAGE_PACE = {
    "run": 10.0,      # 10 km/h = 6 min/km
    "walk": 5.0,      # 5 km/h = 12 min/km
    "cycling": 20.0,  # 20 km/h = 3 min/km
    "swim": 3.0,      # 3 km/h (swimming is slower)
}

class CalorieCalculationStrategy(ABC):
    """
    Abstract base class for calorie calculation strategies.
    """
    @abstractmethod
    def calculate(self, item: Dict[str, Any], weight_kg: float, factor: float) -> float:
        """
        Calculate calories for a specific item.
        
        Args:
            item: The exercise item dict (should contain duration, distance, or reps).
            weight_kg: The user's weight in kg.
            factor: The specific factor for calculation (MET value or kcal/rep).
            
        Returns:
            Calculated calories (float).
        """
        pass


class DurationStrategy(CalorieCalculationStrategy):
    """
    Strategy for duration-based exercises (using METs).
    Formula: kcal = MET * weight * (duration_hours)
    """
    def calculate(self, item: Dict[str, Any], weight_kg: float, met_value: float) -> float:
        duration_min = item.get("duration_min", 0)
        if not duration_min:
            return 0.0
        
        duration_hours = float(duration_min) / 60.0
        return met_value * weight_kg * duration_hours


class DistanceStrategy(CalorieCalculationStrategy):
    """
    Strategy for distance-based exercises.
    Converts distance -> duration (using average pace), then calculates using METs.
    """
    def calculate(self, item: Dict[str, Any], weight_kg: float, met_value: float) -> float:
        distance_km = item.get("distance_km", 0)
        if not distance_km:
            return 0.0
            
        exercise_type = item.get("type", "unknown").lower()
        pace_kmh = AVERAGE_PACE.get(exercise_type, 5.0) # Default to walking pace
        
        duration_hours = float(distance_km) / pace_kmh
        return met_value * weight_kg * duration_hours


class RepsStrategy(CalorieCalculationStrategy):
    """
    Strategy for repetition-based exercises.
    Formula: kcal = reps * kcal_per_rep
    """
    def calculate(self, item: Dict[str, Any], weight_kg: float, kcal_per_rep: float) -> float:
        reps = item.get("reps", 0)
        if not reps:
            return 0.0
            
        return float(reps) * kcal_per_rep
