# Constants for goal types
LOSE_WEIGHT = "lose_weight"
MAINTAIN_WEIGHT = "maintain_weight"
GAIN_WEIGHT = "gain_weight"

# Constants for calorie adjustments (approx 0.5kg per week)
DEFICIT_CALORIES = 500
SURPLUS_CALORIES = 500

def calculate_daily_target(
    tdee: float, 
    goal_type: str, 
    current_weight: float = None,
    target_weight: float = None,
    target_date = None
) -> int:
    """
    Calculate daily calorie target based on TDEE, goal, and optional timeline.
    
    Args:
        tdee: Total Daily Energy Expenditure
        goal_type: "lose_weight", "maintain_weight", "gain_weight"
        current_weight: Current weight in kg (optional, for dynamic calculation)
        target_weight: Target weight in kg (optional, for dynamic calculation)
        target_date: Target date to achieve goal (optional, for dynamic calculation)
        
    Returns:
        Daily calorie target (integer)
    """
    from datetime import date, datetime
    from decimal import Decimal
    
    if tdee <= 0:
        return 0
        
    goal = goal_type.lower().strip()
    
    # Maintain weight: return TDEE
    if goal == MAINTAIN_WEIGHT:
        return int(round(tdee))
    
    # Try dynamic calculation if we have all required data
    if current_weight and target_weight and target_date:
        # Convert Decimal to float if needed
        if isinstance(current_weight, Decimal):
            current_weight = float(current_weight)
        if isinstance(target_weight, Decimal):
            target_weight = float(target_weight)
        
        # Parse target_date if it's a string
        if isinstance(target_date, str):
            try:
                target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
            except ValueError:
                target_date = None
        
        if target_date and isinstance(target_date, date):
            today = date.today()
            days_remaining = (target_date - today).days
            
            # Only use dynamic calculation if target date is in the future
            if days_remaining > 0:
                weight_diff = target_weight - current_weight
                
                # Calculate total calorie difference needed
                # 1 kg ≈ 7700 kcal
                total_kcal_diff = weight_diff * 7700
                
                # Calculate daily adjustment
                daily_adjustment = total_kcal_diff / days_remaining
                
                # Apply safety limits
                # Max deficit: 1000 kcal/day (~1kg/week loss)
                # Max surplus: 500 kcal/day (healthy gain)
                if daily_adjustment < -1000:
                    daily_adjustment = -1000
                elif daily_adjustment > 500:
                    daily_adjustment = 500
                
                target = tdee + daily_adjustment
                
                # Safety floor: minimum 1200 kcal/day
                if target < 1200:
                    return 1200
                    
                return int(round(target))
    
    # Fallback to fixed ±500 kcal
    target = tdee
    if goal == LOSE_WEIGHT:
        target = tdee - DEFICIT_CALORIES
    elif goal == GAIN_WEIGHT:
        target = tdee + SURPLUS_CALORIES

    # Safety floor
    if target < 1200:
        return 1200
        
    return int(round(target))

def infer_goal_from_target(current_weight: float, target_weight: float) -> tuple[str, int]:
    from decimal import Decimal

    # Convert Decimal to float
    if isinstance(current_weight, Decimal):
        current_weight = float(current_weight)
    if isinstance(target_weight, Decimal):
        target_weight = float(target_weight)

    if current_weight <= 0:
        return LOSE_WEIGHT, 0

    if target_weight < current_weight:
        return LOSE_WEIGHT, int(round(current_weight - target_weight))
    elif target_weight > current_weight:
        return GAIN_WEIGHT, int(round(target_weight - current_weight))
    else:
        return MAINTAIN_WEIGHT, 0

