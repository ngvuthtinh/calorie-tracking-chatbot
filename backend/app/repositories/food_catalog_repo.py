"""
Repository for food catalog database operations using MySQLdb.
"""

from typing import Dict, List, Optional
from app.db.connection import fetch_all, fetch_one


class FoodCatalogRepo:
    """
    Repository for accessing food catalog data using raw MySQL queries.
    
    Provides methods to query food nutrition information including calories per unit,
    base units, and food aliases.
    """
    
    def get_all_foods(self) -> List[Dict]:
        """
        Fetch all foods from the catalog.
        
        Returns:
            List of food dictionaries
        """
        query = """
            SELECT id, name_normalized, kcal_per_unit, base_unit, 
                   grams_per_unit, source
            FROM food_catalog
            ORDER BY name_normalized
        """
        return fetch_all(query)
    
    def get_food_by_name(self, name: str) -> Optional[Dict]:
        """
        Fetch food by normalized name, checking both main catalog and aliases.
        
        Args:
            name: Food name (will be normalized to lowercase)
            
        Returns:
            Food dictionary or None if not found
        """
        name_lower = name.lower().strip()
        
        # First, try direct lookup in food_catalog
        query = """
            SELECT id, name_normalized, kcal_per_unit, base_unit, 
                   grams_per_unit, source
            FROM food_catalog
            WHERE name_normalized = %s
        """
        food = fetch_one(query, (name_lower,))
        
        if food:
            return food
        
        # If not found, try looking up in aliases
        alias_query = """
            SELECT fc.id, fc.name_normalized, fc.kcal_per_unit, fc.base_unit,
                   fc.grams_per_unit, fc.source
            FROM food_catalog fc
            JOIN food_alias fa ON fc.id = fa.food_id
            WHERE fa.alias_normalized = %s
        """
        return fetch_one(alias_query, (name_lower,))
    
    def get_calories_per_unit(self, food_name: str) -> Optional[float]:
        """
        Get calories per unit for a food item.
        
        Args:
            food_name: Normalized food name
            
        Returns:
            Calories per unit as float, or None if not found
        """
        food = self.get_food_by_name(food_name)
        if food and food.get("kcal_per_unit"):
            return float(food["kcal_per_unit"])
        return None
    
    def get_all_as_dict(self) -> Dict[str, Dict]:
        """
        Get all foods as a dictionary keyed by name.
        
        Returns:
            Dictionary mapping food names to food dictionaries
        """
        foods = self.get_all_foods()
        return {food["name_normalized"]: food for food in foods}
    
    def search_foods(self, search_term: str) -> List[Dict]:
        """
        Search for foods by partial name match.
        
        Args:
            search_term: Term to search for
            
        Returns:
            List of matching food dictionaries
        """
        search_pattern = f"%{search_term.lower()}%"
        query = """
            SELECT DISTINCT fc.id, fc.name_normalized, fc.kcal_per_unit, 
                   fc.base_unit, fc.grams_per_unit, fc.source
            FROM food_catalog fc
            LEFT JOIN food_alias fa ON fc.id = fa.food_id
            WHERE fc.name_normalized LIKE %s 
               OR fa.alias_normalized LIKE %s
            ORDER BY fc.name_normalized
            LIMIT 20
        """
        return fetch_all(query, (search_pattern, search_pattern))
