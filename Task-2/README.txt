1. we can use the test.py file for passing test data to the API or
2. we can use the command curl (for git bash and command prompt):

for git bash:
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
    "Pclass": 1,
    "Sex": 1,
    "Age": 29.0,
    "SibSp": 0,
    "Parch": 0,
    "Fare": 211.3375,
    "Embarked_Q": false,
    "Embarked_S": true
}'

for command prompt:
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d "{\"Pclass\": 1, \"Sex\": 1, \"Age\": 29.0, \"SibSp\": 0, \"Parch\": 0, \"Fare\": 211.3375, \"Embarked_Q\": false, \"Embarked_S\": true}"
