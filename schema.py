from sqlalchemy import create_engine, Column, Date, DateTime, ForeignKey, func
from sqlalchemy import Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import CheckConstraint
from datetime import datetime, timedelta
import bcrypt
import secrets

# basic configuration
engine = create_engine('sqlite:///health_and_fitness.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# User class
# Static information about the user that does not change frequently
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)  # For login
    # For account recovery and notifications
    email = Column(String, unique=True, nullable=False)
    # Securely storing the hashed password
    password_hash = Column(String, nullable=False)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    initial_weight = Column(Float)
    height = Column(Float)

    # relationships with other tables
    workouts = relationship("Workout", back_populates="user")
    meals = relationship("Meal", back_populates="user")
    water_intakes = relationship("WaterIntake", back_populates="user")
    nutrition_logs = relationship("NutritionLog", back_populates="user")
    sleep_logs = relationship("SleepLog", back_populates="user")
    health_metrics = relationship("HealthMetric", back_populates="user")
    body_compositions = relationship(
        "BodyComposition", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    # For session management
    sessions = relationship("UserSession", back_populates="user")

    # Password hashing methods
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'),
                                           bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'),
                              self.password_hash.encode('utf-8'))


# Session model
class UserSession(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    user = relationship("User", back_populates="sessions")


# The following classes are for the user's health and fitness data

# Workout class
class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date)
    type = Column(String)
    duration = Column(Float)  # in minutes
    intensity = Column(String)
    calories_burned = Column(Float)
    user = relationship("User", back_populates="workouts")


# Meal class
class Meal(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date)
    meal_type = Column(String)
    eating_time = Column(DateTime)  # The exact time of the meal
    user = relationship("User", back_populates="meals")
    food_items = relationship("MealFoodItem", back_populates="meal")


# FoodItem class
class FoodItem(Base):
    __tablename__ = 'food_items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # nutritional information
    calories = Column(Float, CheckConstraint('calories>=0'), nullable=False)
    proteins = Column(Float, CheckConstraint('proteins>=0'), nullable=False)
    carbs = Column(Float, CheckConstraint('carbs>=0'), nullable=False)
    fats = Column(Float, CheckConstraint('fats>=0'), nullable=False)
    fiber = Column(Float, CheckConstraint('fiber>=0'))
    vitamins = Column(String)  # Could be json
    minerals = Column(String)  # Could be json
    # relationships with other tables
    meal_food_items = relationship("MealFoodItem", back_populates="food_item")


# MealFoodItem class (Association Object)
class MealFoodItem(Base):
    __tablename__ = 'meal_food_items'
    id = Column(Integer, primary_key=True)
    meal_id = Column(Integer, ForeignKey('meals.id'))
    food_item_id = Column(Integer, ForeignKey('food_items.id'))
    serving_size = Column(Float)
    meal = relationship("Meal", back_populates="food_items")
    food_item = relationship("FoodItem")


# WaterIntake class
class WaterIntake(Base):
    __tablename__ = 'water_intake'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date)
    amount = Column(Float, CheckConstraint('amount>=0'), nullable=False)
    user = relationship("User", back_populates="water_intakes")


# NutritionLog class
class NutritionLog(Base):
    __tablename__ = 'nutrition_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date)
    summary = Column(String)  # include total calories, water intake, etc.
    user = relationship("User", back_populates="nutrition_logs")


# SleepLog class
class SleepLog(Base):
    __tablename__ = 'sleep_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date)
    time_fell_asleep = Column(DateTime)  # Timestamp when user fell asleep
    time_woke_up = Column(DateTime)  # Timestamp when user woke up
    deep_sleep_duration = Column(Float)  # Duration in deep sleep
    rem_sleep_duration = Column(Float)  # Duration in REM sleep
    light_sleep_duration = Column(Float)  # Duration in light sleep
    interruptions = Column(Integer)  # Number of interruptions
    sleep_quality_index = Column(Integer)  # An index of sleep quality
    notes = Column(String)  # Additional notes about the sleep session
    user = relationship("User", back_populates="sleep_logs")

    @hybrid_property
    def total_sleep_duration(self):
        if self.time_fell_asleep and self.time_woke_up:
            # Calculate total sleep duration based on the timestamps
            total_seconds = (
                self.time_woke_up - self.time_fell_asleep).total_seconds()
            return total_seconds / 3600  # Convert seconds to hours
        return 0

    @total_sleep_duration.expression
    def total_sleep_duration(cls):
        # Use database function to calculate duration for queries
        return (func.julianday(
            cls.time_woke_up) - func.julianday(cls.time_fell_asleep)) * 24


# HealthMetric class
class HealthMetric(Base):
    __tablename__ = 'health_metrics'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date)
    weight = Column(Float)
    # bmi = Column(Float) I will calculate this dynamically
    heart_rate = Column(Integer)
    systolic_blood_pressure = Column(String)
    diastolic_blood_pressure = Column(String)
    user = relationship("User", back_populates="health_metrics")


# BodyComposition class
class BodyComposition(Base):
    __tablename__ = 'body_compositions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date)
    body_weight = Column(Float)  # Overall body weight
    body_fat_percentage = Column(Float)  # Body fat percentage
    skeletal_muscle_mass = Column(Float)  # Skeletal muscle mass
    lean_body_mass = Column(Float)  # Lean body mass (muscle and other non-fat)
    body_water = Column(Float)  # Total body water
    visceral_fat_level = Column(Integer)  # Visceral fat level
    bone_mass = Column(Float)  # Bone mass
    basal_metabolic_rate = Column(Integer)  # BMR (Basal Metabolic Rate)
    metabolic_age = Column(Integer)  # Metabolic age
    user = relationship("User", back_populates="body_compositions")


# Goal class
class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    goal_type = Column(String)
    target_value = Column(Float)
    current_value = Column(Float)
    deadline = Column(Date)
    # like 'Not Started', 'In Progress', 'Achieved', 'Failed'
    status = Column(String)
    user = relationship("User", back_populates="goals")


# Create the tables
Base.metadata.create_all(engine)


# User registration and login functions

# User registration
def register_user(username, email, password):
    session = Session()
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    try:
        session.add(new_user)
        session.commit()
        print("User registered successfully.")
    except IntegrityError:
        session.rollback()
        print("Error: The username or email is already in use.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"An error occurred while registering: {e}")
    finally:
        session.close()


# User login
def login_user(username, password):
    session = Session()
    try:
        user = session.query(User).filter(User.username == username).first()
        if user and user.check_password(password):
            # Generate a session token using secrets module
            token = secrets.token_urlsafe()
            user_session = UserSession(
                user_id=user.id, token=token,
                expires_at=datetime.utcnow() + timedelta(days=1))
            session.add(user_session)
            session.commit()
            print(f"User logged in successfully. Session token:{token}")
            return token
        else:
            print("Invalid username or password.")
            return None
    except SQLAlchemyError as e:
        print(f"An error occurred while logging in: {e}")
    finally:
        session.close()
