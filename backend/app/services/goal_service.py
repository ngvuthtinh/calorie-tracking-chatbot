# Constants for goal types
LOSE_WEIGHT = "lose_weight"
MAINTAIN_WEIGHT = "maintain_weight"
GAIN_WEIGHT = "gain_weight"

# Constants for calorie adjustments (approx 0.5kg per week)
DEFICIT_CALORIES = 500
SURPLUS_CALORIES = 500

def calculate_daily_target(tdee: float, goal_type: str) -> int:
    """
    Calculate daily calorie target based on TDEE and goal.
    
    Args:
        tdee: Total Daily Energy Expenditure
        goal_type: "lose_weight", "maintain_weight", "gain_weight"
        
    Returns:
        Daily calorie target (integer)
    """
    if tdee <= 0:
        return 0
        
    goal = goal_type.lower().strip()
    target = tdee

    if goal == LOSE_WEIGHT:
        target = tdee - DEFICIT_CALORIES
    elif goal == GAIN_WEIGHT:
        target = tdee + SURPLUS_CALORIES
    # else MAINTAIN_WEIGHT: target = tdee

    # Safety floor: Don't recommend starving (e.g. < 1000 kcal) 
    # unless medically supervised. For this bot, let's clamp at 1000.
    if target < 1200:
        return 1200
        
    return int(round(target))

def infer_goal_from_target(current_weight: float, target_weight: float) -> tuple[str, int]:
    """
    Infer goal type and calorie delta based on current vs target weight.
    Returns: (goal_type, target_delta)
    """
    if current_weight <= 0:
        # Default fallback if current weight is unknown
        return LOSE_WEIGHT, 0

    if target_weight < current_weight:
        # Lose weight
        return LOSE_WEIGHT, int(current_weight - target_weight)
    elif target_weight > current_weight:
        # Gain weight
        return GAIN_WEIGHT, int(target_weight - current_weight)
    else:
        # Maintain
        return MAINTAIN_WEIGHT, 0
