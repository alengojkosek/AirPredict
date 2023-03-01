from sklearn.metrics import mean_squared_error, mean_absolute_error
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

df = pd.read_csv('cleaned_arsopodatki.csv')

x = df.drop('pm10', axis=1)
y = df['pm10']

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = LinearRegression()

model.fit(X_train, y_train)

with open('linear_regression_0.2.0.pkl', 'wb') as f:
    pickle.dump(model, f)

y_pred_train = model.predict(X_train)

# Evaluate the performance of the model on the training data
train_score = model.score(X_train, y_train)
print(f"Training R-squared score: {train_score:.2f}")

# Calculate mean squared error (MSE) on the testing data
mse = mean_squared_error(y_train, y_pred_train)
print(f"Training MSE: {mse:.2f}")

# Calculate mean absolute error (MAE) on the testing data
mae = mean_absolute_error(y_train, y_pred_train)
print(f"Training MAE: {mae:.2f}")

# Use the model to make predictions on the testing data
y_pred_test = model.predict(X_test)

# Evaluate the performance of the model on the testing data
test_score = model.score(X_test, y_test)
print(f"Testing R-squared score: {test_score:.2f}")

# Calculate mean squared error (MSE) on the testing data
mse = mean_squared_error(y_test, y_pred_test)
print(f"Testing MSE: {mse:.2f}")

# Calculate mean absolute error (MAE) on the testing data
mae = mean_absolute_error(y_test, y_pred_test)
print(f"Testing MAE: {mae:.2f}")
