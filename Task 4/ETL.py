import os
import requests
import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("etl.log", mode="a")
    ]
)
logger = logging.getLogger(__name__)

# API Configuration
API_KEY = os.getenv("API_KEY")
STOCK_SYMBOL = os.getenv("STOCK_SYMBOL")
BASE_URL = "https://www.alphavantage.co/query"

# PostgreSQL Configuration
DB_NAME = os.getenv("DB_NAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

# Extract: Fetch data from Alpha Vantage
def fetch_stock_data() -> pd.DataFrame:
    """
    Fetch daily stock data from Alpha Vantage API and return as a DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame containing stock data.
    """
    logger.info("Fetching stock data from Alpha Vantage API...")
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK_SYMBOL,
        "apikey": API_KEY,
        "datatype": "json"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        time_series = data.get("Time Series (Daily)", {})

        if not time_series:
            logger.warning("No data received from API.")
            return pd.DataFrame()

        df = pd.DataFrame.from_dict(time_series, orient="index").reset_index()
        df.columns = ["date", "open", "high", "low", "close", "volume"]
        df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": int})
        df["date"] = pd.to_datetime(df["date"])

        logger.info(f"Successfully fetched {len(df)} records.")
        return df
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        raise

# Load: Save data to PostgreSQL
def load_to_postgres(df: pd.DataFrame) -> None:
    """
    Load the given DataFrame into the PostgreSQL database.
    
    Args:
        df (pd.DataFrame): DataFrame containing stock data.
    """
    if df.empty:
        logger.info("No data to load into the database.")
        return

    logger.info("Loading data into PostgreSQL...")
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        cursor = conn.cursor()

        for _, row in df.iterrows():
            insert_query = sql.SQL("""
                INSERT INTO stock_data (date, open_price, high_price, low_price, close_price, volume)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (date) DO NOTHING
            """)
            cursor.execute(insert_query, (row["date"], row["open"], row["high"], row["low"], row["close"], row["volume"]))

        conn.commit()
        logger.info("Data loaded successfully!")
    except psycopg2.Error as e:
        logger.error(f"Error loading data to PostgreSQL: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

# ETL Process
def run_etl() -> None:
    """
    Execute the ETL process: Extract, Transform, Load.
    """
    logger.info("Starting ETL process...")
    try:
        stock_df = fetch_stock_data()
        load_to_postgres(stock_df)
    except Exception as e:
        logger.critical(f"ETL process failed: {e}")
    else:
        logger.info("ETL process completed successfully!")

if __name__ == "__main__":
    run_etl()
