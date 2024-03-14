from sqlalchemy import create_engine, Column, Date, DateTime, ForeignKey, func
from sqlalchemy import Integer, String, Float, Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import CheckConstraint
from datetime import datetime, timedelta
import bcrypt
import secrets
import enum

# basic configuration
engine = create_engine('sqlite:///health_and_fitness.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# User class
# Static information about the user that does not change frequently
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)  # For login
    # For account recovery and notifications
    email = Column(String(255), unique=True, nullable=False)
    # Securely storing the hashed password
    password_hash = Column(String(255), nullable=False)
    # Name might not be strictly required
    name = Column(String(255), nullable=True)
    # Age is optional but, if provided, must be non-negative integer
    age = Column(Integer, CheckConstraint('age>=0'), nullable=True)
    # Gender is optional, I may consider using Enum for predefined values
    gender = Column(String(50), nullable=True)
    # non-negative initial weight and height
    initial_weight = Column(Float, CheckConstraint('initial_weight>=0'),
                            nullable=False)
    height = Column(Float, CheckConstraint('height>=0'), nullable=False)

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
    # Ensuring uniqueness and non-nullability
    token = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # Ensure an expiration time is always provided
    expires_at = Column(DateTime, nullable=False)
    user = relationship("User", back_populates="sessions")

    __table_args__ = (
        CheckConstraint('expires_at > created_at',
                        name='check_expiration_after_creation'),
    )


# The following classes are for the user's health and fitness data

# Workout class
class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    # Assuming a max length for the workout type
    type = Column(String(255), nullable=False)
    # Ensure duration is non-negative
    duration = Column(Float, CheckConstraint('duration>=0'), nullable=False)
    # Max length for the intensity description
    intensity = Column(String(255), nullable=False)
    # Ensure non-negative calories burned
    calories_burned = Column(Float, CheckConstraint('calories_burned>=0'),
                             nullable=False)
    user = relationship("User", back_populates="workouts")


# Meal class
class Meal(Base):
    __tablename__ = 'meals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    meal_type = Column(String(255), nullable=False)  # Breakfast, Lunch, etc.
    eating_time = Column(DateTime, nullable=False)
    user = relationship("User", back_populates="meals")
    food_items = relationship("MealFoodItem", back_populates="meal")


# FoodItem class
class FoodItem(Base):
    __tablename__ = 'food_items'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    # nutritional information per serving
    calories = Column(Float, CheckConstraint('calories>=0'), nullable=False)
    proteins = Column(Float, CheckConstraint('proteins>=0'), nullable=False)
    carbs = Column(Float, CheckConstraint('carbs>=0'), nullable=False)
    fats = Column(Float, CheckConstraint('fats>=0'), nullable=False)
    fiber = Column(Float, CheckConstraint('fiber>=0'))
    vitamins = Column(String)  # Could be json
    minerals = Column(String)  # Could be json
    # relationships with other tables
    meal_food_items = relationship("MealFoodItem", back_populates="food_item")


# MealFoodItem class (Association Object), many-to-many relationship
# This allows recording which food items are part of which meals
class MealFoodItem(Base):
    __tablename__ = 'meal_food_items'
    id = Column(Integer, primary_key=True)
    meal_id = Column(Integer, ForeignKey('meals.id'))
    food_item_id = Column(Integer, ForeignKey('food_items.id'))
    servings_consumed = Column(Float, CheckConstraint('servings_consumed>=0'),
                               default=1, nullable=False)  # number of servings
    meal = relationship("Meal", back_populates="food_items")
    food_item = relationship("FoodItem")


# WaterIntake class
class WaterIntake(Base):
    __tablename__ = 'water_intake'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    # Ensuring water intake amount is non-negative
    amount = Column(Float, CheckConstraint('amount>=0'), nullable=False)
    user = relationship("User", back_populates="water_intakes")


# NutritionLog class
class NutritionLog(Base):
    __tablename__ = 'nutrition_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    # include total calories, water intake, etc.
    summary = Column(String(1000), nullable=False)
    user = relationship("User", back_populates="nutrition_logs")


# SleepLog class
class SleepLog(Base):
    __tablename__ = 'sleep_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    time_fell_asleep = Column(DateTime, nullable=False)
    time_woke_up = Column(DateTime, nullable=False)
    deep_sleep_duration = Column(Float, CheckConstraint(
        'deep_sleep_duration>=0'), nullable=True)  # Non-negative, optional
    rem_sleep_duration = Column(Float, CheckConstraint(
        'rem_sleep_duration>=0'), nullable=True)
    light_sleep_duration = Column(Float, CheckConstraint(
        'light_sleep_duration>=0'), nullable=True)
    interruptions = Column(Integer, CheckConstraint(
        'interruptions>=0'), nullable=True)
    sleep_quality_index = Column(Integer, CheckConstraint(
        'sleep_quality_index>=0'), nullable=True)  # An index of sleep quality
    notes = Column(String(
        1000), nullable=True)  # Optional, with a reasonable max length notes

    user = relationship("User", back_populates="sleep_logs")

    # Validate sleep time range
    __table_args__ = (
        CheckConstraint('time_fell_asleep < time_woke_up',
                        name='check_sleep_times'),
    )

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
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(DateTime, nullable=False)  # time of the day

    # Heart rate should be positive, optional
    heart_rate = Column(Integer,
                        CheckConstraint('heart_rate>0'), nullable=True)
    systolic_blood_pressure = Column(Integer, CheckConstraint(
        'systolic_blood_pressure>0'), nullable=True)  # Optional, positive
    diastolic_blood_pressure = Column(Integer, CheckConstraint(
        'diastolic_blood_pressure>0'), nullable=True)  # Optional, positive

    blood_oxygen_level = Column(Float, CheckConstraint(
        'blood_oxygen_level>=0 AND blood_oxygen_level<=100'),
        nullable=True)  # Optional, 0-100 range
    blood_glucose_level = Column(Float, CheckConstraint(
        'blood_glucose_level>0'), nullable=True)  # Optional, positive
    body_temperature = Column(Float, CheckConstraint(
        'body_temperature>0'), nullable=True)  # Optional, positive

    user = relationship("User", back_populates="health_metrics")


# BodyComposition class
class BodyComposition(Base):
    __tablename__ = 'body_compositions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)

    # Assuming weight can be optional but must be positive when provided
    weight = Column(Float, CheckConstraint('weight>0'), nullable=True)
    # height is assumed to be static and is provided in the user model
    # bmi = Column(Float)  # I will calculate this dynamically

    # detail body composition metrics
    body_fat_percentage = Column(
        Float, CheckConstraint(
            'body_fat_percentage >= 0 AND body_fat_percentage <= 100'),
        nullable=True)
    skeletal_muscle_mass = Column(
        Float, CheckConstraint('skeletal_muscle_mass > 0'),
        nullable=True)
    lean_body_mass = Column(
        Float, CheckConstraint('lean_body_mass > 0'), nullable=True)
    body_water = Column(
        Float, CheckConstraint('body_water > 0'), nullable=True)
    visceral_fat_level = Column(
        Integer, CheckConstraint('visceral_fat_level >= 0'), nullable=True)
    bone_mass = Column(Float, CheckConstraint('bone_mass > 0'), nullable=True)
    basal_metabolic_rate = Column(
        Integer, CheckConstraint('basal_metabolic_rate > 0'), nullable=True)
    metabolic_age = Column(Integer, CheckConstraint('metabolic_age > 0'),
                           nullable=True)

    user = relationship("User", back_populates="body_compositions")


# Goal class


# Define an enumeration for goal statuses
class GoalStatusEnum(enum.Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    ACHIEVED = "Achieved"
    FAILED = "Failed"


class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    goal_type = Column(String(255), nullable=False)
    target_value = Column(Float, CheckConstraint('target_value>=0'),
                          nullable=False)  # Targets should be non-negative
    current_value = Column(Float, CheckConstraint('current_value>=0'),
                           nullable=False)  # values should be non-negative
    deadline = Column(Date, nullable=True)  # A goal may not have a deadline
    # Use Enum for predefined statuses
    status = Column(Enum(GoalStatusEnum), nullable=False)

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
