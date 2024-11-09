import requests

# Test data
test_passenger = {
    "Pclass": 3,
    "Sex": 1,
    "Age": 29.0,
    "SibSp": 0,
    "Parch": 0,
    "Fare": 7.25,
    "Embarked_Q": False,
    "Embarked_S": True
}

# Make API request
response = requests.post(
    "http://127.0.0.1:8000/predict",
    json=test_passenger
)

print("Test Passenger:", test_passenger)
print("\nResponse:", response.json())