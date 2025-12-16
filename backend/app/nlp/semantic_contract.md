# Semantic Contract – CalorieAssistant

## 1. Output Format (Global)

All semantic outputs MUST follow this structure:

```python
{
  "intent": "<string>",
  "data": { ... }
}

* intent: determines what action the system will perform
* data: structured information extracted from the command

## 2. Intent Names

### Food
- log_food
- edit_food_entry
- add_food_items
- move_food_entry
- delete_food_entry

### Exercise
- log_exercise
- edit_exercise_entry
- add_exercise_items
- delete_exercise_entry

### Stats
- show_summary_today
- show_summary_date
- show_weekly_stats
- show_stats_this_week

### Profile
- update_profile

### Undo
- undo

## 3. Food – Data Schema

```python
{
  "intent": "log_food",
  "data": {
    "meal": "breakfast | lunch | dinner | snack",   # optional
    "action": "eat | drink",                         # optional
    "items": [
      {
        "name": "<string>",
        "qty": <int>,                                # optional
        "unit": "<string>",                          # optional
        "note": "<string>"                           # optional
      }
    ]
  }
}

## 4. Exercise – Data Schema

```python
{
  "intent": "log_exercise",
  "data": {
    "items": [
      {
        "type": "run | walk | cycling | swim | plank | pushups | squats | lunges",
        "duration_min": <int> | null,
        "distance_km": <int> | null,
        "reps": <int> | null
      }
    ]
  }
}


## 5. Stats – Data Schema

### Summary Today
```python
{"intent": "show_summary_today", "data": {}}

### Summary by Date
```python
{"intent": "show_summary_date", "data": {"date": "YYYY-MM-DD"}}

### Weekly Stats
```python
{"intent": "show_weekly_stats", "data": {}}


## 6. Profile – Data Schema

```python
{
  "intent": "update_profile",
  "data": {
    "field": "weight | height | goal | activity_level",
    "value": "<int or string>",
    "unit": "kg | cm"        # optional
  }
}


## 7. Undo – Data Schema

```python
{"intent": "undo", "data": {}}
or 
{"intent": "undo", "data": {"scope": "food | exercise"}}
