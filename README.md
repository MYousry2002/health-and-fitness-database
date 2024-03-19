# Health and Fitness Tracking App Database and Queries

## Overview

The Health and Fitness Tracking App is designed to serve as a comprehensive solution for individuals seeking to improve their physical health, gain insights into their fitness journey, and maintain a healthy lifestyle. The primary objective of this application is to provide users with a convenient platform to track a wide array of health and fitness metrics that are crucial for setting and achieving personal health goals.

### Primary Objectives

- **Comprehensive Tracking**: Offer users the ability to log and monitor various health-related metrics, including workouts, nutrition, sleep, and overall well-being.
- **Insightful Analysis**: Utilize the tracked data to analyze patterns, assess progress, and provide valuable insights that can guide users towards healthier choices and behaviors.
- **Personalized Recommendations**: Generate personalized fitness and nutrition recommendations based on the users' logs, goals, and progress to aid in achieving their specific health objectives.
- **Progress Monitoring**: Enable users to set and track goals, whether it be weight loss, muscle gain, or improving stamina, and provide feedback on their progress.

### Target Audience

The app caters to a diverse audience ranging from fitness enthusiasts and athletes to individuals just beginning their journey to a healthier lifestyle. It is designed to be adaptable to various fitness levels and personalized needs, making it a valuable tool for anyone looking to take charge of their health.

### Tracked Metrics

The application tracks a broad spectrum of metrics to provide a holistic view of health and fitness:

- **Workouts**: Records exercise type, duration, intensity, and calories burned.
- **Nutrition**: Logs daily meals and food intake, including calories, macronutrients, and micronutrients from vitamins and minerals.
- **Medications**: Track user's medications history
- **Sleep**: Monitors sleep patterns, such as time asleep, sleep cycles (REM, deep, light sleep), and interruptions.
- **Health Metrics**: Measures heart rate, blood pressure, blood oxygen, glucose levels, and body temperature.
- **Body Composition**: Tracks weight and detailed body composition metrics such as body fat percentage, skeletal muscle mass, lean body mass, bone mass, basal metabolic rate, and metabolic age.
- **Water Intake**: Logs daily water consumption to ensure hydration.
- **Goals**: Users can set specific health and fitness goals, track their progress towards achieving them, and adjust their strategies as needed.

### Benefits to Users

Using the Health and Fitness Tracking App provides multiple benefits:

- **Data-Driven Decisions**: By having a centralized repository of health data, users can make informed decisions about their diet, exercise, and lifestyle habits.
- **Goal Accountability**: Setting goals with deadlines and tracking progress helps users stay accountable and motivated.
- **Behavioral Insights**: Over time, users can identify patterns in their behaviors that lead to successful outcomes or areas that need improvement.
- **Health Awareness**: Regular monitoring of health metrics can increase awareness and prompt timely health-related actions.
- **Customization and Adaptability**: As the app learns more about the user, it can adapt its recommendations to fit changing health statuses and fitness levels.
- **Community and Support**: The app can serve as a platform for users to connect with a community of like-minded individuals for support and motivation.

By integrating various aspects of health and fitness into one platform, the app not only simplifies the management of health data but also acts as a personal health coach, empowering users to reach and maintain optimal health.



## Data Schema Design
The Health and Fitness Tracking App is designed to offer users a comprehensive platform to monitor and enhance their health and fitness levels. To achieve this, the app manages a variety of key data elements and their relationships, structured through a carefully designed SQL data schema. Here, we provide a description of what data is necessary and how it is organized within the database.

### Tables
#### User Data
- **Table**: `users`
- **Columns**: `id` and static information such as `username`, `email`, `password`, `name`, `age`, `gender`, `initial_weight`, and `height`.
- **Purpose**: To create personalized profiles and base
- **Design Justification**: User data is central to the schema, serving as a reference point for all other data entities through foreign keys, ensuring data integrity and enabling personalization. The values for `username` and `email` are constrained to be unique.

#### Session
- **Table**: `sessions`
- **Columns**: Includes `id`, `user_id` (FK), `token`, `created_at`, and `expires_at`.
- **Purpose**: Manages user login sessions, tracking session creation and expiration.
- **Design Justification**: Separates session information from user profiles for security and efficiency. The `expires_at > created_at` constraint ensures logical session timelines.

#### Nutrition Logs

##### `food_items` Table
- **Columns**: `id`, `name`, `calories`, `proteins`, `carbs`, `fats`, `fiber`
- **Purpose**: To store detailed nutritional information for each food item, including macronutrients and fiber content.
- **Design Justification**: Central to the nutrition tracking feature, this table allows for accurate calorie and nutrient intake calculation. It serves as a foundation for meal planning, dietary analysis, and nutritional recommendations. Having this table separate from the meals table helps avoid redunduncies in the data as we can have one food item in many meals.

##### `vitamin` Table
- **Columns**: `id`, `name`
- **Purpose**: To catalog various vitamins present in food items.
- **Design Justification**: By isolating vitamins into a separate table, we can have multiple vitamins associated with a food item while keeping the food item table simple and without redunduncies. It acts as a master list of vitamins.

##### `mineral` Table
- **Columns**: `id`, `name`
- **Purpose**: Similar to the `vitamin` table, it catalogs minerals.
- **Design Justification**: This separation facilitates having multiple minerals associated with a food item while keeping the food item table simple and without redunduncies. It acts as a master list of minerals.

##### `food_item_vitamins` Table
- **Columns**: `id`, `food_item_id` (FK), `vitamin_id` (FK), `amount`
- **Purpose**: To associate food items with their vitamin content and respective amounts.
- **Design Justification**: It exemplifies the use of an association object to bridge many-to-many relationships between food items and their vitamins contents, enabling detailed nutritional analysis and appropriate normalization.

##### `food_item_minerals` Table
- **Columns**: `id`, `food_item_id` (FK), `mineral_id` (FK), `amount`
- **Purpose**: To associate food items with their mineral content and respective amounts.
- **Design Justification**: Similar to `food_item_vitamins`, it exemplifies the use of an association object to bridge many-to-many relationships between food items and their minerals contents, enabling detailed nutritional analysis and appropriate normalization.

##### `meals` Table
- **Columns**: `id`, `user_id` (FK), `date`, `meal_type`, `eating_time`
- **Purpose**: To log user meals, including the type of meal and the time it was consumed.
- **Design Justification**: Central to dietary tracking, this table enables users to monitor their eating habits, meal timing, and nutritional intake, contributing to more informed dietary choices.

##### `meal_food_items` Table
- **Columns**: `id`, `meal_id` (FK), `food_item_id` (FK), `servings_consumed`
- **Purpose**: To detail which food items comprise a meal and in what quantity.
- **Design Justification**: Facilitates precise tracking of food intake within meals, supporting accurate calorie and nutrient consumption analysis. This assossiation object bridges many-to-many relationship that captures the complexity of dietary habits.

##### `NutritionLog` Table
- **Columns**: `id`, `user_id` (FK), `date`, `summary`
- **Purpose**: To provide a daily summary of the user's nutritional intake, including total calories, water intake, etc.
- **Design Justification**: Enables users to reflect on their daily dietary habits and receive a summarized view of their nutritional performance, offering a basis for adjustments and improvements in their diet.

#### Water Intake
- **Table**: `water_intake`
- **Columns**: `id`, `user_id` (FK), `date`, `amount`
- **Purpose**: To ensure users maintain adequate hydration.
- **Design Justification**: Simple yet essential metric for overall health, easy to track and analyze over time.

#### Medications
- **Table**: `medications`
- **Columns**: `id`, `user_id` (FK), `name`, `dosage`, `frequency`, `start_date`, `end_date`, `reason`
- **Purpose**: To track the user's medication schedule, dosage, and purpose.
- **Design Justification**: Medication tracking is crucial for users managing chronic conditions or those in a recovery phase. It allows for monitoring adherence to prescribed treatments and understanding the impact of medication on health metrics and overall well-being. The table is related to the `users` table via a foreign key (`user_id`), ensuring that medication logs are properly associated with the correct user profiles. This can also facilitate reminders, dosage tracking, and analysis of medication effects over time.

#### Workout Information
- **Table**: `workouts`
- **Columns**: `id`, `user_id` (FK), `date`, `type`, `duration`, `intensity`, `calories_burned`
- **Purpose**: To track physical activity, assess progress, and inform fitness goal adjustments.
- **Design Justification**: The workout data is linked to users through a foreign key, allowing for a detailed activity history and enabling analysis over time.

#### Sleep Patterns
- **Table**: `sleep_logs`
- **Columns**: `id`, `user_id` (FK), `date`, `time_fell_asleep`, `time_woke_up`, `deep_sleep_duration`, `rem_sleep_duration`, `light_sleep_duration`, `interruptions`, `sleep_quality_index`
- **Purpose**: To evaluate sleep quality.
- **Design Justification**: The sleep data is linked to users through a foreign key. Tracking sleep patterns over time allows for trend analysis and recommendations for improving sleep. 

#### Health Metrics
- **Table**: `health_metrics`
- **Columns**: `id`, `user_id` (FK), `date`, `time`, `heart_rate`, `systolic_blood_pressure`, `diastolic_blood_pressure`, `blood_oxygen_level`, `blood_glucose_level`, `body_temperature`
- **Purpose**: Crucial for detecting health patterns, risks, and tracking progress towards physical goals.
- **Design Justification**: This table ensure comprehensive health tracking, from daily metrics to changes in body composition over longer periods. It is linked to users through a foreign key.

#### Body Composition
- **Table**: `body_compositions`
- **Columns**: `id`, `user_id` (FK), `date`, `weight`, `body_fat_percentage`, `skeletal_muscle_mass`, `lean_body_mass`, `bone_mass`, `basal_metabolic_rate`, and `metabolic_age`.
- **Purpose**: To track changes in the user's physical composition over time. Provides a basis for recommendations on diet, exercise, and lifestyle.
- **Design Justification**: The detailed body composition metrics or columns enables specific input for goals tracking and recommendations. It is linked to users through a foriegn key.

#### Goals
- **Table**: `goals`
- **Columns**: `id`, `user_id` (FK), `goal_type`, `target_value`, `current_value`, `deadline`, `status`
- **Purpose**: Motivates users and guides app recommendations.
- **Design Justification**: Enumerations for goal types and statuses ensure data consistency and enable tailored progress tracking. It is linked to users through a foriegn key.


## Best Practices Adherance
### Constraints

The Health and Fitness Tracking App database extensively utilizes constraints to ensure data integrity and validity across the schema. Notable examples include `CheckConstraint`s for ensuring that numeric data (like age, calories, heart rate) falls within realistic and meaningful ranges, and unique constraints on `username` and `email` in the `users` table to prevent duplicate records. These constraints are critical for maintaining a high quality of data, preventing erroneous entries, and facilitating accurate data analysis and personalized recommendations.

### Normalization

Normalization is adhered to across the database to reduce redundancy, avoid anomalies, and ensure data integrity. The schema design reflects thoughtful normalization practices, including the separation of user profiles, health metrics, nutritional data, and workout logs into distinct tables. This separation allows for efficient data storage and manipulation. For example, the `FoodItem`, `Vitamin`, and `Mineral` tables are normalized to prevent the duplication of nutritional information, utilizing association tables (`FoodItemVitamin`, `FoodItemMineral`) to manage many-to-many relationships, which exemplifies normalization to improve database efficiency and integrity.

### Indices

Indices are strategically utilized to enhance query performance across the database. Examples include indexing `user_id` across tables where user-related data is queried frequently. Additionally, the schema stratigically uses composite indices such as indexing `user_id` and `date` in that same order in `workouts` and `sleep_logs`, and indexing `user_id`, `date`, and `time` in that same order in `health_metrics`. These indices enable rapid data retrieval operations, particularly beneficial in a user-centric application where timely access to personal health data is crucial. The use of indices represents a thoughtful balance between data retrieval performance and storage efficiency.

### Transactions

The application implements transactions to ensure data consistency and reliability during operations that involve multiple steps or depend on conditional outcomes. For instance, the user registration (in `create.py`) and data insertion processes (in `insert_data.py`) employ transactions to ensure that either all operations succeed or none, preventing partial updates that could lead to data inconsistency. The use of context managers in Python (via SQLAlchemy) to handle sessions and transactions demonstrates a commitment to maintaining the database's integrity, especially during complex operations like batch data inserts or updates that could affect multiple related tables.

Together, these practices of applying constraints, adhering to normalization principles, strategically using indices, and implementing transactions form the backbone of the database schema's robustness, efficiency, and reliability. They ensure that the Health and Fitness Tracking App can provide a seamless, fast, and reliable user experience while maintaining the integrity and accuracy of the health and fitness data it manages.

## Queries Examples

This section outlines various data queries implemented in the Health and Fitness Tracking App, as detailed in the `query_data.py` file. Each query is designed to leverage the comprehensive data schema to extract meaningful insights and support the app's functionality in monitoring and guiding users toward their health and fitness goals.

**Scenario 1 - Retrieving User Workouts Within a Date Range:**
The query fetches workout sessions for a specified user within a date range, allowing users to review their exercise history, frequency, and variations over time. It's essential for assessing progress and adapting workout plans.

**Scenario 2 - Calculating Average Daily Caloric Intake:**
This calculation determines the average calories consumed per day by a user, crucial for dietary planning and tracking nutritional intake against goals. It supports personalized dietary recommendations based on caloric needs and consumption patterns.

**Scenario 3 - Analyzing Average Sleep Duration:**
The query evaluates the average sleep duration for a user over the past month, providing insights into sleep quality and identifying patterns or issues that may impact overall health and wellness.

**Scenario 4 - Tracking Weight Change Over the Past Year:**
This function tracks a user's weight change over the past year, offering a longitudinal view of their physical transformation and the effectiveness of their fitness or dietary regimen.

**Scenario 5 - Accessing Last Recorded Health Metrics:**
Fetching the most recent health metrics for a user is vital for immediate assessments, understanding current health status, and identifying potential health issues early.

**Scenario 6 - Recommending Daily Water Intake:**
Calculates and compares a user's average water intake to recommended levels, highlighting the importance of hydration for health and suggesting adjustments as needed.

**Scenario 7 - Suggesting Caloric Intake Based on Goals:**
This scenario suggests adjustments to a user's daily caloric intake based on their health or fitness goals, aiding in achieving desired outcomes through dietary modifications.

**Scenario 8 - Assessing Fitness Level Based on Workout Intensity:**
By analyzing the intensity and frequency of recent workouts, this query provides feedback on a user's current fitness level, suggesting improvements or changes to optimize fitness outcomes.

**Scenario 9 - Providing Sleep Quality Improvement Tips:**
Offers personalized advice for improving sleep quality based on recent sleep duration data, emphasizing the role of sleep in overall health and recovery.

**Scenario 10 - Enhancing Sleep Routine Consistency:**
Provides recommendations for making a user's sleep routine more consistent, based on analysis of bedtime and wake-up time variability, to improve sleep quality and daytime functioning.

**Scenario 11 - Encouraging Dietary Diversity:**
Encourages users to diversify their diet for better nutritional balance, based on the variety of food items consumed, ensuring a comprehensive intake of essential nutrients.

**Scenario 12 - Tracking Progress Towards Fitness Goals:**
Monitors and reports a user's progress towards their specified fitness goals, using the latest health metrics and workout data for an in-depth analysis, supporting goal adjustment and personalized guidance.

**Scenario 13 - Calculating User's BMI:**
It provides users with an immediate understanding of their BMI, a key health metric that offers insight into their general health status regarding weight.

**Scenario 14 - Summarize Most Frequent Workouts**
This query assists in understanding the user's exercise preferences and patterns by summarizing the types of workouts they engage in most frequently and the total time dedicated to each type. It supports the app's goal of providing personalized fitness recommendations by identifying the user's preferred workout types, which can inform tailored workout plans that align with their interests and goals. By aggregating this data, the app can also help users see trends in their fitness routines, encouraging them to diversify their workouts or focus on specific areas for improvement. 

These queries are meticulously designed to exploit the relational structure and integrity of the database, enabling the app to provide actionable insights, personalized recommendations, and comprehensive progress tracking to its users. They demonstrate the application's use of advanced SQL features, normalization practices, and efficient data retrieval methods to enhance user experience and support health and fitness objectives.

## Example Data Insertions
A wide array of example data is inserted that ensures the Health and Fitness Tracking App's database reflects realistic scenarios. This data was created using Python Faker Library in `insert_data.py`. It encompasses user profiles, workouts, nutrition, sleep, health metrics, body compositions, and goals. This comprehensive dataset allows for thorough testing and demonstration of the app’s capabilities.
Data insertion is handled transactionally to maintain consistency and integrity, ensuring either complete success or rollback in case of errors. This methodical approach not only tests the system's reliability but also showcases its potential to manage diverse health and fitness data effectively.

## Installation and Excution
1. Clone the repository
```bash
git clone https://github.com/MYousry2002/health-and-fitness-database
```
2. Create virtual environment and install dependencies
```bash
python3 -m venv venv
venv/bin/activate
pip3 install -r requirements.txt
```

3. Run the code
```bash
# create the schema
python3 create.py
# insert example data
python3 insert_data.py
# run example queries
python3 query_data.py
```

## Contribution
Contributions are welcome. Please fork the repository and submit a pull request with your proposed changes.

## Licence
