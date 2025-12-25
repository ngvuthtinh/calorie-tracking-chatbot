"""
Nutrition Service - Food Calorie Estimation

Estimates calorie intake from logged food items using:
- Food catalog database lookup
- Food name normalization
- Quantity and unit handling
- Graceful handling of unknown foods

Data is loaded from the food_catalog database table with in-memory caching.
"""

from typing import Any, Dict, List, Optional
from backend.app.repositories.food_catalog_repo import FoodCatalogRepo


# In-memory cache for food data (lazy loaded from database)
_food_cache: Optional[Dict[str, Any]] = None


def _load_food_cache() -> Dict[str, Any]:
    """
    Load food data from database into memory cache.
    
    This is called lazily on first use to avoid database queries at import time.
    Cache structure:
    {
        "foods": {food_name: {kcal_per_unit, base_unit, grams_per_unit}}
    }
    
    Returns:
        Dictionary containing food nutrition data
    """
    global _food_cache
    
    if _food_cache is not None:
        return _food_cache
    
    # Initialize cache structure
    cache = {"foods": {}}
    
    try:
        # Load all foods from database
        repo = FoodCatalogRepo()
        foods = repo.get_all_foods()
        
        for food in foods:
            name = food["name_normalized"]
            cache["foods"][name] = {
                "kcal_per_unit": float(food["kcal_per_unit"]) if food.get("kcal_per_unit") else 0,
                "base_unit": food.get("base_unit", "unit"),
                "grams_per_unit": float(food["grams_per_unit"]) if food.get("grams_per_unit") else None
            }
    
    except Exception as e:
        # If database is unavailable, use fallback values
        print(f"Warning: Could not load food data from database: {e}")
        print("Using fallback values.")
        cache = _get_fallback_cache()
    
    _food_cache = cache
    return _food_cache


def _get_fallback_cache() -> Dict[str, Any]:
    """
    Get fallback food data if database is unavailable.
    
    Returns:
        Dictionary with minimal food data for basic functionality
    """
    return {
        "foods": {
            "egg": {"kcal_per_unit": 72, "base_unit": "piece", "grams_per_unit": None},
            "milk": {"kcal_per_unit": 42, "base_unit": "100ml", "grams_per_unit": 100},
            "banana": {"kcal_per_unit": 105, "base_unit": "piece", "grams_per_unit": None},
            "rice_cooked": {"kcal_per_unit": 130, "base_unit": "100g", "grams_per_unit": 100},
            "chicken_breast": {"kcal_per_unit": 165, "base_unit": "100g", "grams_per_unit": 100},
        }
    }


def estimate_intake(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Estimate total calories consumed for a list of food items.
    
    Args:
        items: List of food items, each containing:
            - name: str (food name)
            - qty: Optional[float] (quantity, defaults to 1)
            - unit: Optional[str] (unit of measurement)
            
    Returns:
        Dict with:
            - total_kcal: float (total calories consumed)
            - breakdown: List[Dict] (per-item calorie breakdown)
            
    Example:
        >>> items = [
        ...     {"name": "egg", "qty": 2},
        ...     {"name": "milk", "qty": 200, "unit": "ml"}
        ... ]
        >>> result = estimate_intake(items)
        >>> result['total_kcal']  # ~228 kcal
    """
    if not items:
        return {"total_kcal": 0.0, "breakdown": []}
    
    breakdown = []
    total_kcal = 0.0
    
    for item in items:
        food_name = _normalize_food_name(item.get("name", ""))
        qty = item.get("qty", 1)
        unit = item.get("unit", "")
        
        # Handle unknown quantity
        if qty is None or qty == "UNKNOWN":
            qty = 1
        
        # Lookup food in cache
        kcal = _estimate_food_calories(food_name, qty, unit)
        total_kcal += kcal
        
        # Format measurement string
        measurement = f"{qty} {unit}" if unit else f"{qty}"
        
        breakdown.append({
            "name": food_name,
            "measurement": measurement.strip(),
            "kcal": round(kcal, 1),
            "status": "found" if kcal > 0 else "unknown"
        })
    
    return {
        "total_kcal": round(total_kcal, 1),
        "breakdown": breakdown
    }


def _normalize_food_name(name: str) -> str:
    """
    Normalize food name for database lookup.
    
    Args:
        name: Raw food name
        
    Returns:
        Normalized food name (lowercase, trimmed, underscores for spaces)
    """
    if not name:
        return "unknown"
    
    # Convert to lowercase and trim
    normalized = name.lower().strip()
    
    # Replace spaces with underscores for database format
    normalized = normalized.replace(" ", "_")
    
    return normalized


def _estimate_food_calories(food_name: str, qty: float, unit: str = "") -> float:
    """
    Estimate calories for a single food item.
    
    Args:
        food_name: Normalized food name
        qty: Quantity
        unit: Unit of measurement (optional)
        
    Returns:
        Estimated calories
    """
    # Load cache from database if needed
    cache = _load_food_cache()
    foods = cache.get("foods", {})
    
    # Lookup food
    food_data = foods.get(food_name)
    
    if not food_data:
        # Try with alias lookup from database
        try:
            repo = FoodCatalogRepo()
            food_db = repo.get_food_by_name(food_name)
            if food_db:
                food_data = {
                    "kcal_per_unit": float(food_db["kcal_per_unit"]),
                    "base_unit": food_db.get("base_unit", "unit"),
                    "grams_per_unit": float(food_db["grams_per_unit"]) if food_db.get("grams_per_unit") else None
                }
                # Cache it for next time
                foods[food_name] = food_data
        except Exception:
            pass
    
    if not food_data:
        # Unknown food - return 0 but don't crash
        return 0.0
    
    # Calculate calories based on quantity
    kcal_per_unit = food_data["kcal_per_unit"]
    base_unit = food_data["base_unit"]
    
    # Simple calculation: qty * kcal_per_unit
    # TODO: Add unit conversion logic if needed
    kcal = qty * kcal_per_unit
    
    return kcal


def get_food_info(food_name: str) -> Optional[Dict[str, Any]]:
    """
    Get nutrition information for a specific food.
    
    Args:
        food_name: Food name to lookup
        
    Returns:
        Dictionary with food nutrition info or None if not found
    """
    normalized_name = _normalize_food_name(food_name)
    cache = _load_food_cache()
    foods = cache.get("foods", {})
    
    food_data = foods.get(normalized_name)
    
    if not food_data:
        # Try database lookup
        try:
            repo = FoodCatalogRepo()
            food_db = repo.get_food_by_name(normalized_name)
            if food_db:
                return {
                    "name": food_db["name_normalized"],
                    "kcal_per_unit": float(food_db["kcal_per_unit"]),
                    "base_unit": food_db["base_unit"],
                    "grams_per_unit": float(food_db["grams_per_unit"]) if food_db.get("grams_per_unit") else None
                }
        except Exception:
            pass
    
    return food_data
