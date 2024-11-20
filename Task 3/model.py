import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler

# Load sample data, e.g., Iris dataset for a quick model
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define the Logistic Regression model and hyperparameters to tune
model = LogisticRegression(max_iter=10000)
param_grid = {
    'C': [0.01, 0.1, 1, 10, 100],  # Regularization parameter
    'solver': ['lbfgs', 'liblinear'],  # Solvers
    'penalty': ['l2'],  # Regularization type
}

# Perform Grid Search to find the best hyperparameters
grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train_scaled, y_train)

# Best model and accuracy
best_model = grid_search.best_estimator_
accuracy = best_model.score(X_test_scaled, y_test)
print(f"Accuracy: {accuracy:.4f}")

# Save the model
joblib.dump(best_model, "model.joblib")