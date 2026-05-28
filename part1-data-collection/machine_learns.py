import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib


train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

target_column = "current_players"

y_train = train_df[target_column]
X_train = train_df.drop(columns=["name", target_column])

y_test = test_df[target_column]
X_test = test_df.drop(columns=["name", target_column])

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

joblib.dump(model, "steam_model.pkl")

rmse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Metrics:")
print(f"RMSE: {rmse:.4f}")
print(f"R^2 Score: {r2:.4f}")

plt.figure(figsize=(8, 6))
sns.scatterplot(x=y_test, y=predictions, alpha = 0.6, color='blue')

max_val = max(max(y_test), max(predictions))
plt.plot([0, max_val], [0, max_val], color = 'red', label = "Perfect Predictions")

plt.xlabel("Real Player Count")
plt.ylabel("Predicted Player Count")
plt.title("Linear Regression: Actual vs Predicted Player Counts")
plt.savefig("actual_vs_predicted.png")

plt.show()