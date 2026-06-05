import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import joblib

# -----------------------------
# 1. Load Dataset
# -----------------------------
df = pd.read_csv("data/city_day.csv")

# -----------------------------
# 2. Data Cleaning
# -----------------------------
df = df.drop(columns=["Xylene"])
df = df.dropna(subset=["AQI"])
df = df.fillna(df.mean(numeric_only=True))

# Convert Date
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(by="Date")

# -----------------------------
# 3. Feature Engineering
# -----------------------------
# City Average Pollutant Values

city_avg = df.groupby("City").mean(numeric_only=True)

joblib.dump(city_avg, "models/city_avg.pkl")

df = pd.get_dummies(df, columns=["City"])

# Define X and y
X = df.drop(columns=["AQI", "AQI_Bucket", "Date"])
y = df["AQI"]

# -----------------------------
# 4. Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 5. Train Best Model (XGBoost)
# -----------------------------
xgb_model = XGBRegressor(
    n_estimators=800,
    learning_rate=0.03,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    gamma=0.1,
    reg_alpha=0.1,
    reg_lambda=1,
    random_state=42
)

xgb_model.fit(X_train, y_train)

# -----------------------------
# 6. Evaluate Model
# -----------------------------
y_pred = xgb_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print("Final Model MSE:", mse)

# -----------------------------
# 7. Save Model + Features
# -----------------------------
import os
os.makedirs("models", exist_ok=True)
joblib.dump(df.mean(numeric_only=True), "models/mean_values.pkl")
joblib.dump(xgb_model, "models/aqi_model.pkl")
joblib.dump(X.columns, "models/model_features.pkl")

print("Model and features saved successfully ✅")