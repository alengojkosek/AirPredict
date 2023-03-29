from sklearn.metrics import mean_squared_error, mean_absolute_error
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import mlflow


MLFLOW_TRACKING_URI='https://dagshub.com/alengojkosek/AirPredict.mlflow'

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
#mlflow.set_experiment('AirPredict')

mlflow.autolog(exclusive=False)

with mlflow.start_run():

    # Load the dataset
    df = pd.read_csv('data/processed/current_data.csv')

    x = df.drop('pm10', axis=1)
    y = df['pm10']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    model = LinearRegression()

    model.fit(X_train, y_train)

    # Save the model to disk
    with open('LG_model_3.pkl', 'wb') as f:
        pickle.dump(model, f)


    # Use the model to make predictions on the training data
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

    mlflow.log_metric("MAE", mae)
    mlflow.log_metric("MSE", mse)
    mlflow.log_metric("Train score", train_score)

autolog_run = mlflow.last_active_run()