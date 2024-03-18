from create import (
    Base, engine, Session,
    User, Workout, FoodItem, Vitamin, Mineral,
    FoodItemVitamin, FoodItemMineral, Meal, MealFoodItem,
    WaterIntake, NutritionLog, Medication, SleepLog,
    HealthMetric, BodyComposition, Goal, GoalStatusEnum
)
from faker import Faker
from datetime import timedelta
import random
import bcrypt

# Initialize Faker instance
fake = Faker()

# Connect to the database and create a session
Base.metadata.create_all(engine)
session = Session()


# Helper function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt()).decode('utf-8')


# Function to create fake users
def create_users(num_users=50):
    users = []
    for _ in range(num_users):
        password = fake.password()
        hashed_password = hash_password(password)
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password_hash=hashed_password,
            name=fake.name(),
            age=random.randint(18, 80),
            gender=random.choice(['Male', 'Female', 'Other']),
            initial_weight=random.uniform(50, 100),
            height=random.uniform(150, 200)
        )
        users.append(user)
    return users


# Function to create fake workouts
def create_workouts(users, num_workouts=200):
    workouts = []
    for _ in range(num_workouts):
        user = random.choice(users)
        workout = Workout(
            user_id=user.id,
            date=fake.date_between(start_date='-1y', end_date='today'),
            type=random.choice(['Running', 'Cycling', 'Swimming', 'Gym']),
            duration=random.uniform(0.5, 2),
            intensity=random.choice(['Low', 'Medium', 'High']),
            calories_burned=random.randint(100, 1000)
        )
        workouts.append(workout)
    return workouts


# Function to create fake food items
def create_food_items(num_items=100):
    food_items = []
    for _ in range(num_items):
        food_item = FoodItem(
            name=fake.word().capitalize(),
            calories=random.randint(100, 500),
            proteins=random.uniform(0, 30),
            carbs=random.uniform(0, 100),
            fats=random.uniform(0, 50),
            fiber=random.uniform(0, 10)
        )
        food_items.append(food_item)
    return food_items


# Function to create fake vitamins
def create_vitamins(num_vitamins=10):
    vitamins = []
    for _ in range(num_vitamins):
        vitamin = Vitamin(
            name=f'Vitamin {fake.word().capitalize()}'
        )
        vitamins.append(vitamin)
    return vitamins


# Function to create fake minerals
def create_minerals(num_minerals=10):
    minerals = []
    for _ in range(num_minerals):
        mineral = Mineral(
            name=f'Mineral {fake.word().capitalize()}'
        )
        minerals.append(mineral)
    return minerals


# Function to create fake food items vitamins
def create_food_item_vitamins(food_items, vitamins):
    food_item_vitamins = []
    for food_item in food_items:
        for _ in range(random.randint(1, 3)):  # Each item has 1-3 vitamins
            vitamin = random.choice(vitamins)
            food_item_vitamin = FoodItemVitamin(
                food_item_id=food_item.id,
                vitamin_id=vitamin.id,
                amount=random.uniform(0.1, 100.0)  # Random amount of vitamin
            )
            food_item_vitamins.append(food_item_vitamin)
    return food_item_vitamins


# Function to create fake food item minerals
def create_food_item_minerals(food_items, minerals):
    food_item_minerals = []
    for food_item in food_items:
        for _ in range(random.randint(1, 3)):  # Each item has 1-3 minerals
            mineral = random.choice(minerals)
            food_item_mineral = FoodItemMineral(
                food_item_id=food_item.id,
                mineral_id=mineral.id,
                amount=random.uniform(0.1, 100.0)  # Random amount of mineral
            )
            food_item_minerals.append(food_item_mineral)
    return food_item_minerals


# Function to create fake meals
def create_meals(users, num_meals=200):
    meals = []
    for _ in range(num_meals):
        user = random.choice(users)
        meal = Meal(
            user_id=user.id,
            date=fake.date_between(start_date='-1y', end_date='today'),
            meal_type=random.choice(['Breakfast', 'Lunch', 'Dinner', 'Snack']),
            eating_time=fake.date_time()
        )
        meals.append(meal)
    return meals


# Function to create fake meal food items
def create_meal_food_items(meals, food_items):
    meal_food_items = []
    for meal in meals:
        for _ in range(random.randint(1, 5)):  # Each meal has 1-5 food items
            food_item = random.choice(food_items)
            meal_food_item = MealFoodItem(
                meal_id=meal.id,
                food_item_id=food_item.id,
                servings_consumed=random.randint(1, 3)  # 1-3 servings per item
            )
            meal_food_items.append(meal_food_item)
    return meal_food_items


# Function to create fake water intakes
def create_water_intakes(users, num_intakes=200):
    water_intakes = []
    for _ in range(num_intakes):
        user = random.choice(users)
        water_intake = WaterIntake(
            user_id=user.id,
            date=fake.date_between(start_date='-1y', end_date='today'),
            amount=random.uniform(0.5, 5)  # Liters
        )
        water_intakes.append(water_intake)
    return water_intakes


# Function to create fake nutrition logs
def create_nutrition_logs(users, num_logs=200):
    nutrition_logs = []
    for _ in range(num_logs):
        user = random.choice(users)
        nutrition_log = NutritionLog(
            user_id=user.id,
            date=fake.date_between(start_date='-1y', end_date='today'),
            summary=fake.text(max_nb_chars=500)
        )
        nutrition_logs.append(nutrition_log)
    return nutrition_logs


# Function to create fake medications
def create_medications(users, num_medications=50):
    medications = []
    for _ in range(num_medications):
        user = random.choice(users)
        medication = Medication(
            user_id=user.id,
            name=fake.word().capitalize(),
            dosage=f'{random.randint(1, 500)} mg',
            frequency=f'{random.randint(1, 4)} times a day',
            start_date=fake.date_between(start_date='-1y', end_date='today'),
            end_date=fake.date_between(
                start_date='today', end_date='+1y') if random.choice(
                    [True, False]) else None,
            reason=fake.sentence()
        )
        medications.append(medication)
    return medications


# Function to create fake sleep logs
def create_sleep_logs(users, num_logs=200):
    sleep_logs = []
    for _ in range(num_logs):
        user = random.choice(users)
        sleep_time = fake.date_time_between(start_date='-1y', end_date='now')
        wake_time = sleep_time + timedelta(hours=random.randint(6, 9))
        sleep_log = SleepLog(
            user_id=user.id,
            date=sleep_time.date(),
            time_fell_asleep=sleep_time,
            time_woke_up=wake_time,
            deep_sleep_duration=random.uniform(1, 3),
            rem_sleep_duration=random.uniform(0.5, 2),
            light_sleep_duration=random.uniform(3, 5),
            interruptions=random.randint(0, 5),
            sleep_quality_index=random.randint(1, 100),
            notes=fake.sentence()
        )
        sleep_logs.append(sleep_log)
    return sleep_logs


# Function to create fake health metrics
def create_health_metrics(users, num_metrics=500):
    health_metrics = []
    for _ in range(num_metrics):
        user = random.choice(users)
        health_metric = HealthMetric(
            user_id=user.id,
            date=fake.date_between(start_date='-1y', end_date='today'),
            time=fake.date_time_between(start_date='-1y', end_date='now'),
            heart_rate=random.randint(60, 100),
            systolic_blood_pressure=random.randint(90, 120),
            diastolic_blood_pressure=random.randint(60, 80),
            blood_oxygen_level=random.uniform(95, 100),
            blood_glucose_level=random.uniform(70, 140),
            body_temperature=random.uniform(36.5, 37.5)
        )
        health_metrics.append(health_metric)
    return health_metrics


# Function to create fake body compositions
def create_body_compositions(users, num_compositions=200):
    body_compositions = []
    for _ in range(num_compositions):
        user = random.choice(users)
        body_composition = BodyComposition(
            user_id=user.id,
            date=fake.date_between(start_date='-1y', end_date='today'),
            weight=random.uniform(50, 100),
            body_fat_percentage=random.uniform(10, 30),
            skeletal_muscle_mass=random.uniform(10, 40),
            lean_body_mass=random.uniform(40, 60),
            body_water=random.uniform(50, 70),
            visceral_fat_level=random.randint(1, 10),
            bone_mass=random.uniform(2, 5),
            basal_metabolic_rate=random.randint(1200, 2000),
            metabolic_age=random.randint(20, 60)
        )
        body_compositions.append(body_composition)
    return body_compositions


# Function to create fake goals
def create_goals(users, num_goals=100):
    goals = []
    for _ in range(num_goals):
        user = random.choice(users)
        goal = Goal(
            user_id=user.id,
            goal_type=random.choice(['Weight Loss', 'Muscle Gain',
                                     'Stamina Building']),
            target_value=random.uniform(5, 20),
            current_value=random.uniform(0, 5),
            deadline=fake.date_between(start_date='today', end_date='+1y'),
            status=random.choice(list(GoalStatusEnum))
        )
        goals.append(goal)
    return goals


# Add data to the session and commit
def add_to_session(data):
    for record in data:
        session.add(record)


# Insert data into the database
def main():
    # Create users and add them to the session
    users = create_users(num_users=50)
    add_to_session(users)

    # Create workouts and add them to the session
    workouts = create_workouts(users)
    add_to_session(workouts)

    # Create water intakes and add them to the session
    water_intakes = create_water_intakes(users)
    add_to_session(water_intakes)

    # Create nutrition logs and add them to the session
    nutrition_logs = create_nutrition_logs(users)
    add_to_session(nutrition_logs)

    # Create medications and add them to the session
    medications = create_medications(users)
    add_to_session(medications)

    # Create sleep logs and add them to the session
    sleep_logs = create_sleep_logs(users)
    add_to_session(sleep_logs)

    # Create health metrics and add them to the session
    health_metrics = create_health_metrics(users)
    add_to_session(health_metrics)

    # Create body compositions and add them to the session
    body_compositions = create_body_compositions(users)
    add_to_session(body_compositions)

    # Create goals and add them to the session
    goals = create_goals(users)
    add_to_session(goals)

    # Generate and add food items, vitamins, minerals
    food_items = create_food_items(num_items=100)
    add_to_session(food_items)
    vitamins = create_vitamins(num_vitamins=10)
    add_to_session(vitamins)
    minerals = create_minerals(num_minerals=10)
    add_to_session(minerals)

    # Generate and add relationships between food items and vitamins/minerals
    food_item_vitamins = create_food_item_vitamins(food_items, vitamins)
    add_to_session(food_item_vitamins)
    food_item_minerals = create_food_item_minerals(food_items, minerals)
    add_to_session(food_item_minerals)

    # Generate meals and associate food items with meals
    meals = create_meals(users, num_meals=200)
    add_to_session(meals)
    meal_food_items = create_meal_food_items(meals, food_items)
    add_to_session(meal_food_items)

    # Add all to session and commit
    try:
        session.commit()
        print("All data added successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    main()
