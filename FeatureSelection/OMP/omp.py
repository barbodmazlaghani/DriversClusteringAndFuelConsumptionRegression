import pandas as pd
import numpy as np
from sklearn.linear_model import OrthogonalMatchingPursuit
from sklearn.model_selection import train_test_split


def load_data(filepath):
    # Load data from Excel file
    data = pd.read_excel(filepath)
    return data


def preprocess_data(data):
    # Remove non-numeric and non-relevant columns
    df = data.select_dtypes(include=[np.number])
    return df


def select_features(df):
    # Define the feature matrix X and the target variable y
    X = df.drop(columns='fuel_consumption_avg')
    y = df['fuel_consumption_avg']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and fit Orthogonal Matching Pursuit with 8 non-zero coefficients
    omp = OrthogonalMatchingPursuit(n_nonzero_coefs=8)
    omp.fit(X_train, y_train)

    # Extract the names of the selected features
    selected_features = X.columns[omp.coef_ != 0]
    return selected_features


def main():
    file_path = 'drivers_mean_base.xlsx'

    # Load and preprocess the data
    data = load_data(file_path)
    processed_data = preprocess_data(data)

    # Select features
    important_features = select_features(processed_data)

    # Output the selected features
    print("Selected features for predicting fuel consumption average:")
    for feature in important_features:
        print(feature)


# Run the main function
if __name__ == "__main__":
    main()
