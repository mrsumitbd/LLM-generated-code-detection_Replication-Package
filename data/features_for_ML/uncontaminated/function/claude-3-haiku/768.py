import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def run_analysis():
    # Load the dataset
    data = pd.read_csv('dataset.csv')

    # Split the data into features and target
    X = data.drop('target_variable', axis=1)
    y = data['target_variable']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate the model on the test set
    r_squared = model.score(X_test, y_test)
    print(f'R-squared score: {r_squared:.2f}')

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Calculate the mean squared error
    mse = np.mean((y_test - y_pred) ** 2)
    print(f'Mean Squared Error: {mse:.2f}')

    # Return the trained model
    return model