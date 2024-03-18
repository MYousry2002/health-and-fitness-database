# import necessary modules from create.py
from create import Session, User, Workout, FoodItem, Meal, SleepLog, BodyComposition, HealthMetric, MealFoodItem
from sqlalchemy import func, and_
from datetime import datetime, timedelta

# Create a new session
session = Session()

# Scenario 1: Get all workouts for a specific user within a date range
def get_workouts_by_user_and_date(user_id, start_date, end_date):
    workouts = session.query(Workout).filter(
        Workout.user_id == user_id,
        Workout.date.between(start_date, end_date)
    ).all()
    return workouts

# Scenario 2: Calculate the average calories consumed per day by a user in a specific week
def average_daily_calories(user_id, start_date, end_date):
    avg_calories = session.query(
        func.avg(MealFoodItem.servings_consumed * FoodItem.calories)
    ).join(Meal).join(FoodItem).filter(
        Meal.user_id == user_id,
        Meal.date.between(start_date, end_date)
    ).scalar()
    return avg_calories

# Scenario 3: Analyze average sleep duration over the last month
def average_sleep_duration_last_month(user_id):
    one_month_ago = datetime.now() - timedelta(days=30)
    avg_sleep_duration = session.query(
        func.avg(SleepLog.total_sleep_duration)
    ).filter(
        SleepLog.user_id == user_id,
        SleepLog.date >= one_month_ago
    ).scalar()
    return avg_sleep_duration

# Scenario 4: Track weight change over the past year
def weight_change_past_year(user_id):
    one_year_ago = datetime.now() - timedelta(days=365)
    weights = session.query(
        BodyComposition.date,
        BodyComposition.weight
    ).filter(
        BodyComposition.user_id == user_id,
        BodyComposition.date >= one_year_ago
    ).order_by(BodyComposition.date.asc()).all()
    return weights

# Scenario 5: Get the last recorded health metrics for a user
def last_recorded_health_metrics(user_id):
    last_metrics = session.query(HealthMetric).filter(
        HealthMetric.user_id == user_id
    ).order_by(HealthMetric.date.desc(), HealthMetric.time.desc()).first()
    return last_metrics

# Usage example
if __name__ == "__main__":
    # user_id_example = 51  # Example user ID
    print(get_workouts_by_user_and_date(51, '2023-04-01', '2024-01-31'))
    print(average_daily_calories(133, '2023-04-01', '2024-01-31'))
    print(average_sleep_duration_last_month(96))
    print(weight_change_past_year(60))
    print(last_recorded_health_metrics(71))
