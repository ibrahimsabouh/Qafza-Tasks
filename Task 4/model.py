import os
import logging
import joblib
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("model_training.log", mode="a")
    ]
)
logger = logging.getLogger(__name__)

# Database Configuration (from environment variables)
DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")
DB_HOST = os.getenv("HOST")
DB_PORT = os.getenv("PORT")
DB_NAME = os.getenv("DB_NAME")

# Step 1: Fetch data from PostgreSQL
def fetch_data_from_postgres() -> pd.DataFrame:
    """
    Fetch data from the PostgreSQL database and return it as a DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing stock data.
    """
    logger.info("Connecting to the PostgreSQL database...")
    try:
        engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        query = "SELECT * FROM stock_data;"
        stock_data = pd.read_sql_query(query, engine)
        logger.info(f"Fetched {len(stock_data)} records from the database.")
        stock_data.dropna(inplace=True)
        return stock_data
    except Exception as e:
        logger.error(f"Error fetching data from PostgreSQL: {e}")
        raise

# Step 2: Prepare data
def prepare_data(data: pd.DataFrame):
    """
    Prepare data for training by creating features and target labels.

    Args:
        data (pd.DataFrame): Raw stock data from the database.

    Returns:
        tuple: Features (X) and target (y) DataFrames.
    """
    logger.info("Preparing data for training...")
    
    # Target column: 1 if price goes up, 0 otherwise
    data['price_direction'] = (data['close_price'] > data['open_price']).astype(int)

    # Feature engineering
    data['daily_range'] = data['high_price'] - data['low_price']
    data['price_change_pct'] = ((data['close_price'] - data['open_price']) / data['open_price']) * 100
    data['volatility'] = (data['high_price'] - data['low_price']) / data['open_price']

    features = ['open_price', 'high_price', 'low_price', 'volume', 'daily_range', 'price_change_pct', 'volatility']
    target = 'price_direction'

    X = data[features]
    y = data[target]
    
    logger.info(f"Data prepared with {X.shape[0]} samples and {X.shape[1]} features.")
    return X, y

# Step 3: Train model
def train_model(X, y) -> XGBClassifier:
    """
    Train an XGBoost classifier on the provided data.

    Args:
        X (pd.DataFrame): Feature data.
        y (pd.Series): Target labels.

    Returns:
        XGBClassifier: The trained XGBoost classifier.
    """
    logger.info("Starting model training...")
    clf = XGBClassifier(random_state=42)

    # Cross-validation
    scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
    logger.info(f"Cross-Validation Accuracy Scores: {scores}")
    logger.info(f"Mean Accuracy: {scores.mean():.4f}")

    # Train on the full dataset
    clf.fit(X, y)
    logger.info("Model training completed.")

    # Save the trained model
    joblib.dump(clf, "model.joblib")
    logger.info("Trained model saved as 'model.joblib'.")
    return clf

# Main script
if __name__ == "__main__":
    try:
        data = fetch_data_from_postgres()
        X, y = prepare_data(data)
        model = train_model(X, y)
        logger.info("Model training pipeline completed successfully.")
    except Exception as e:
        logger.critical(f"An error occurred during the model training pipeline: {e}")
