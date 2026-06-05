# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error
# df = pd.read_csv("data/city_day.csv")
# # print(df.head())
# # print("\nColumns:")
# # print(df.columns)
# # print("\nInfo:")
# # print(df.info())
# # print("\nMissing values count:")
# # print(df.isnull().sum())
# df=df.drop(columns=["Xylene"])
# # print("\nAfter dropping xylene:")
# # print(df.columns)
# df = df.dropna(subset=["AQI"])

# # print("\nAfter removing missing AQI:")
# # print(df.isnull().sum())

# # print("\nNew shape of dataset:")
# # print(df.shape)
# df = df.fillna(df.mean(numeric_only=True))

# # print("\nAfter filling missing values:")
# # print(df.isnull().sum())
# df["Date"] = pd.to_datetime(df["Date"])

# # print("\nDate column type:")
# # print(df["Date"].dtype)

# df = df.sort_values(by="Date")

# # bengaluru_df = df[df["City"] == "Bengaluru"]
# # delhi_df = df[df["City"] == "Delhi"]
# # bengaluru_df = bengaluru_df.set_index("Date")
# # delhi_df = delhi_df.set_index("Date")
# # bengaluru_monthly = bengaluru_df["AQI"].resample("ME").mean()
# # delhi_monthly = delhi_df["AQI"].resample("ME").mean()
# # plt.figure()
# # plt.plot(bengaluru_monthly.index, bengaluru_monthly.values, label="Bengaluru")
# # plt.plot(delhi_monthly.index, delhi_monthly.values, label="Delhi")
# # plt.xlabel("Date")
# # plt.ylabel("AQI")
# # plt.title("AQI Comparison: Bengaluru vs Delhi")
# # plt.legend()
# # plt.show()
# # print("\nAverage AQI:")

# # print("Bengaluru:", bengaluru_df["AQI"].mean())
# # print("Delhi:", delhi_df["AQI"].mean())
# df = pd.get_dummies(df, columns=["City"])
# X = df.drop(columns=["AQI", "AQI_Bucket", "Date"])
# y = df["AQI"]
# print("X shape:", X.shape)
# print("y shape:", y.shape)

# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42
# )

# print("Training data:", X_train.shape)
# print("Testing data:", X_test.shape)

# # Create model
# model = LinearRegression()

# # Train model
# model.fit(X_train, y_train)
# y_pred = model.predict(X_test)

# print("Predictions:", y_pred[:5])
# mse = mean_squared_error(y_test, y_pred)

# print("Mean Squared Error:", mse)
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.linear_model import LinearRegression

# # Create polynomial features
# poly = PolynomialFeatures(degree=2)
# X_poly = poly.fit_transform(X)

# # Split again
# from sklearn.model_selection import train_test_split

# X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
#     X_poly, y, test_size=0.2, random_state=42
# )

# # Train model
# model_p = LinearRegression()
# model_p.fit(X_train_p, y_train_p)

# # Predict
# y_pred_p = model_p.predict(X_test_p)

# # Evaluate
# from sklearn.metrics import mean_squared_error
# mse_p = mean_squared_error(y_test_p, y_pred_p)

# print("Polynomial MSE:", mse_p)
# #random forest model
# from sklearn.ensemble import RandomForestRegressor
# rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
# rf_model.fit(X_train, y_train)
# y_pred_rf = rf_model.predict(X_test)
# from sklearn.metrics import mean_squared_error

# mse_rf = mean_squared_error(y_test, y_pred_rf)

# print("Random Forest MSE:", mse_rf)

# #xgboost model
# from xgboost import XGBRegressor

# xgb_model = XGBRegressor(
#     n_estimators=800,
#     learning_rate=0.03,
#     max_depth=5,
#     subsample=0.8,
#     colsample_bytree=0.8,
#     gamma=0.1,
#     reg_alpha=0.1,
#     reg_lambda=1,
#     random_state=42
# )

# xgb_model.fit(X_train, y_train)

# y_pred_xgb = xgb_model.predict(X_test)

# from sklearn.metrics import mean_squared_error
# mse_xgb = mean_squared_error(y_test, y_pred_xgb)

# print("Tuned XGBoost MSE:", mse_xgb)

# import joblib

# joblib.dump(xgb_model, "aqi_model.pkl")