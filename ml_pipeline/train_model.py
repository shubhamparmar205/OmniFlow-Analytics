import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os

# 1. Load the dataset from the raw data folder
df = pd.read_csv('data/raw/traffic_data.csv')

# 2. Extract specific math-friendly values from the Timestamp text (like Hour and Month)
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['Hour'] = df['Timestamp'].dt.hour
df['DayOfWeek'] = df['Timestamp'].dt.dayofweek
df['Month'] = df['Timestamp'].dt.month

# 3. Convert text Weather categories into simple integers so the math model can read it
weather_mapping = {'Clear': 0, 'Cloudy': 1, 'Rain': 2, 'Snow': 3}
df['Weather_Encoded'] = df['Weather'].map(weather_mapping)

# 4. Convert True/False Events into 1/0
df['Events_Encoded'] = df['Events'].astype(int)

# 5. Gather all the input features (X) to predict the target Traffic Volume (y)
X = df[['Hour', 'DayOfWeek', 'Month', 'Weather_Encoded', 'Events_Encoded']]
y = df['Traffic Volume']

# 6. Split 20% of the data out so we can honestly test the model on data it hasn't seen
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7. Create and train the XGBoost ML algorithm to learn the traffic patterns
model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# 8. Let the model predict on the test data and calculate its average error
predictions = model.predict(X_test)
error = mean_absolute_error(y_test, predictions)
print(f"Model trained successfully! Average Prediction Error: {error:.2f} vehicles.")

# 9. Save the trained model memory to your hard drive so the API can load it instantly
model_path = 'ml_pipeline/saved_models/traffic_model.joblib'
joblib.dump(model, model_path)
print(f"Model saved automatically to: {model_path}")
