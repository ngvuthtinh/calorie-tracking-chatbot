from enum import Enum
from typing import NewType

# Constants
class ActivityLevel(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"

class MealType(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"

class GoalType(str, Enum):
    lose = "lose"
    maintain = "maintain"
    gain = "gain"

class ActionType(str, Enum):
    eat = "eat"
    drink = "drink"

# Shared Types
# EntryDate is a string in YYYY-MM-DD format
EntryDate = NewType('EntryDate', str)
UserId = NewType('UserId', int)
