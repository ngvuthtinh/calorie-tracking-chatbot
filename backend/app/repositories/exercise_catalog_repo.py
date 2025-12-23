"""
Repository for exercise catalog database operations using MySQLdb.
"""

from typing import Dict, List, Optional
from app.db.connection import fetch_all, fetch_one


class ExerciseRepo:
    """
    Repository for accessing exercise catalog data using raw MySQL queries.
    
    Provides methods to query exercise information including MET values
    and calories per repetition.
    """
    
    def get_all_exercises(self) -> List[Dict]:
        """
        Fetch all exercises from the catalog.
        
        Returns:
            List of exercise dictionaries
        """
        query = """
            SELECT id, name_normalized, met_light, met_moderate, met_heavy, kcal_per_rep
            FROM exercise_catalog
            ORDER BY name_normalized
        """
        return fetch_all(query)
    
    def get_exercise_by_name(self, name: str) -> Optional[Dict]:
        """
        Fetch exercise by normalized name.
        
        Args:
            name: Normalized exercise name (e.g., "run", "pushups")
            
        Returns:
            Exercise dictionary or None if not found
        """
        query = """
            SELECT id, name_normalized, met_light, met_moderate, met_heavy, kcal_per_rep
            FROM exercise_catalog
            WHERE name_normalized = %s
        """
        return fetch_one(query, (name.lower(),))
    
    def get_met_value(self, exercise_name: str, intensity: str = "moderate") -> Optional[float]:
        """
        Get MET value for a specific exercise and intensity.
        
        Args:
            exercise_name: Normalized exercise name
            intensity: Intensity level ("light", "moderate", "heavy")
            
        Returns:
            MET value as float, or None if not found
        """
        exercise = self.get_exercise_by_name(exercise_name)
        if not exercise:
            return None
        
        intensity_lower = intensity.lower()
        
        # Get the appropriate MET value based on intensity
        if intensity_lower == "light" and exercise.get("met_light"):
            return float(exercise["met_light"])
        elif intensity_lower == "moderate" and exercise.get("met_moderate"):
            return float(exercise["met_moderate"])
        elif intensity_lower == "heavy" and exercise.get("met_heavy"):
            return float(exercise["met_heavy"])
        
        # Default to moderate if available
        if exercise.get("met_moderate"):
            return float(exercise["met_moderate"])
        
        return None
    
    def get_calories_per_rep(self, exercise_name: str) -> Optional[float]:
        """
        Get calories per repetition for a strength exercise.
        
        Args:
            exercise_name: Normalized exercise name
            
        Returns:
            Calories per rep as float, or None if not found
        """
        exercise = self.get_exercise_by_name(exercise_name)
        if exercise and exercise.get("kcal_per_rep"):
            return float(exercise["kcal_per_rep"])
        return None
    
    def get_all_as_dict(self) -> Dict[str, Dict]:
        """
        Get all exercises as a dictionary keyed by name.
        
        Returns:
            Dictionary mapping exercise names to exercise dictionaries
        """
        exercises = self.get_all_exercises()
        return {ex["name_normalized"]: ex for ex in exercises}
