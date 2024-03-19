# import necessary modules from create.py
from create import (
    Session,
    User, Workout, FoodItem, Vitamin, Mineral,
    FoodItemVitamin, FoodItemMineral, Meal, MealFoodItem,
    WaterIntake, NutritionLog, Medication, SleepLog,
    HealthMetric, BodyComposition, Goal, GoalStatusEnum
)
from sqlalchemy import func, distinct
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

# Scenario 6: Recommend water intake based on recent water intake data
def recommend_water_intake(user_id):
    recent_date = datetime.now() - timedelta(days=7)
    avg_water_intake = session.query(
        func.avg(WaterIntake.amount)
    ).filter(
        WaterIntake.user_id == user_id,
        WaterIntake.date >= recent_date
    ).scalar()
    # Fetch the gender from the User table
    user_gender = session.query(User.gender).filter(User.id == user_id).scalar()
    recommended_intake = 3.7 if user_gender == 'Male' else 2.7  # Liters per day, roughly
    return avg_water_intake, recommended_intake


# Scenario 7: Suggest nutritional improvements based on user's goals and recent calorie intake
def suggest_nutritional_improvements(user_id, custom_goal_calories=None):
    # Use the most recent BMR as the default goal unless a custom goal is provided
    if custom_goal_calories is None:
        latest_bmr = session.query(BodyComposition.basal_metabolic_rate).filter(
            BodyComposition.user_id == user_id
        ).order_by(BodyComposition.date.desc()).first()
        
        if latest_bmr is None:
            return "No body composition data available to suggest nutritional improvements."
        
        goal_calories = latest_bmr[0]
    else:
        goal_calories = custom_goal_calories

    avg_calories = average_daily_calories(user_id, datetime.now() - timedelta(days=30), datetime.now())
    if avg_calories is None:
        return "No dietary data available to suggest nutritional improvements."

    if avg_calories > goal_calories:
        return "Consider reducing calorie intake to meet your goals."
    elif avg_calories < goal_calories:
        return "You may need to increase your calorie intake to meet your goals."
    else:
        return "Your current calorie intake aligns with your goals."


# Scenario 8: Using the intensity and frequency of workouts to provide feedback on 
# the user's current fitness level and suggest changes if necessary.
def assess_fitness_level(user_id):
    recent_workouts = get_workouts_by_user_and_date(user_id, datetime.now() - timedelta(days=30), datetime.now())
    if not recent_workouts:
        return "No recent workouts found. Staying active is key to a healthy lifestyle."
    average_intensity = sum([{"Low": 1, "Medium": 2, "High": 3}[workout.intensity] for workout in recent_workouts]) / len(recent_workouts)
    if average_intensity < 2:
        return "Consider increasing the intensity of your workouts to improve your fitness level."
    else:
        return "Great job! Your workout intensity is on point."


# Scenario 9: Provide tips to improve sleep quality based on recent average sleep duration
def sleep_duration_tips(user_id):
    avg_sleep_duration = average_sleep_duration_last_month(user_id)
    if avg_sleep_duration is None:
        return "No sleep data available to suggest improvements."
    
    if avg_sleep_duration < 7:
        return "You might not be getting enough rest. Consider setting a regular bedtime and avoiding screens before sleep to improve sleep quality."
    elif avg_sleep_duration > 9:
        return "Too much sleep can also affect your health negatively. Try to wake up at a consistent time and avoid long daytime naps."
    else:
        return "Your sleep routine looks good. Maintain a consistent sleep schedule to keep up the good work!"


# Scenario 10: Provide tips to improve sleep consistency based on recent bedtime and wake-up time
def sleep_consistency_tips(user_id):
    # Calculate the average bedtime and wake-up time over the last month
    recent_date = datetime.now() - timedelta(days=30)
    avg_bedtime_hour = session.query(
        func.avg(func.strftime('%H', SleepLog.time_fell_asleep))
    ).filter(
        SleepLog.user_id == user_id,
        SleepLog.date >= recent_date
    ).scalar()

    avg_wakeup_hour = session.query(
        func.avg(func.strftime('%H', SleepLog.time_woke_up))
    ).filter(
        SleepLog.user_id == user_id,
        SleepLog.date >= recent_date
    ).scalar()

    # Provide recommendations based on the consistency of bedtime and wake-up time
    tips = []
    if avg_bedtime_hour is not None and avg_wakeup_hour is not None:
        avg_bedtime_hour = float(avg_bedtime_hour)
        avg_wakeup_hour = float(avg_wakeup_hour)
        
        # Assuming "inconsistent" means varying more than 1 hour on average
        if not (22 <= avg_bedtime_hour <= 24 or 0 <= avg_bedtime_hour <= 1):  # Not within 10 PM to 1 AM range
            tips.append("Try to go to bed between 10 PM and 1 AM for better sleep quality.")

        if not (5 <= avg_wakeup_hour <= 8):  # Not within 5 AM to 8 AM range
            tips.append("Aiming to wake up between 5 AM and 8 AM can help improve your daily rhythm.")

        if not tips:  # If no specific tips were added
            return "Your sleep routine looks good. Keep it up!"
        
        return " ".join(tips)
    else:
        return "Not enough data to assess your sleep routine."
    

# Scenario 11: Provide tips to improve dietary diversity based on the number of unique food items consumed
def dietary_diversity_tips(user_id):
    recent_food_items_count = session.query(
        func.count(distinct(MealFoodItem.food_item_id))
    ).join(Meal).filter(
        Meal.user_id == user_id,
        Meal.date >= datetime.now() - timedelta(days=30)
    ).scalar()

    # Thresholds and scoring can be adjusted based on nutritional guidelines
    if recent_food_items_count < 20:
        return "Your diet lacks diversity, which might miss out on essential nutrients. Try incorporating a variety of fruits, vegetables, and proteins."
    else:
        return "You have a good variety in your diet. Keep exploring different food items to ensure a balanced intake of nutrients."


# Scenario 12: Track goal progress based on the latest health metrics and workout data
def track_goal_progress(user_id):
    current_date = datetime.now()
    goal = session.query(Goal).filter(
        Goal.user_id == user_id,
        Goal.deadline >= current_date
    ).order_by(Goal.deadline.desc()).first()

    # Initialize progress to None
    progress = None

    if goal:
        if goal.goal_type == 'Weight Loss':
            latest_weight = session.query(BodyComposition).filter(
                BodyComposition.user_id == user_id
            ).order_by(BodyComposition.date.desc()).first().weight
            progress = (goal.current_value - latest_weight) / (goal.current_value - goal.target_value)
            
        elif goal.goal_type == 'Muscle Gain':
            latest_muscle_mass = session.query(BodyComposition).filter(
                BodyComposition.user_id == user_id
            ).order_by(BodyComposition.date.desc()).first().skeletal_muscle_mass
            progress = (latest_muscle_mass - goal.current_value) / (goal.target_value - goal.current_value)
        
        elif goal.goal_type == 'Stamina Building':
            recent_workouts = session.query(Workout).filter(
                Workout.user_id == user_id,
                Workout.date >= current_date - timedelta(days=30)
            ).all()
            if recent_workouts:
                total_difficulty = sum([{"Low": 1, "Medium": 2, "High": 3}[workout.intensity] for workout in recent_workouts])
                max_possible_score = len(recent_workouts) * 3
                progress = total_difficulty / max_possible_score
            else:
                return "No recent workouts to assess stamina building."

        progress_percentage = progress * 100
        return f"You have achieved {progress_percentage:.2f}% of your {goal.goal_type.lower()} goal."
    else:
        return "No active goals found."




# Usage example
if __name__ == "__main__":
    # user_id_example = 1  # Example user ID
    # Scenario 1
    print(get_workouts_by_user_and_date(17, '2023-04-01', '2024-01-31'))
    # Scenario 2
    print(average_daily_calories(36, '2023-04-01', '2024-01-31'))
    # Scenario 3
    print(average_sleep_duration_last_month(1))
    # Scenario 4
    print(weight_change_past_year(48))
    # Scenario 5
    print(last_recorded_health_metrics(27))
    # Scenario 6
    print(recommend_water_intake(43))
    # Scenario 7
    print(suggest_nutritional_improvements(45))
    # Scenario 8
    print(assess_fitness_level(12))
    # Scenario 9
    print(sleep_duration_tips(1))
    # Scenario 10
    print(sleep_consistency_tips(1))
    # Scenario 11
    print(dietary_diversity_tips(17))
    # Scenario 12
    print(track_goal_progress(11))
