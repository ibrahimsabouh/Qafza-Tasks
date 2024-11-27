import os
from datetime import datetime, timedelta
from typing import Dict, Any

import pandas as pd
import joblib
import uvicorn
import logging
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('stock_prediction.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

class StockPredictionApp:
    def __init__(self, env_path: str = '.env'):
        """
        Initialize the stock prediction application.
        
        Args:
            env_path (str): Path to the environment variables file
        """
        # Load environment variables
        load_dotenv(env_path)

        # Initialize FastAPI app
        self.app = FastAPI(
            title="Stock Market Prediction API",
            description="Real-time stock market movement prediction",
            version="1.1.0"
        )

        self._initialize_components()

    def _initialize_components(self) -> None:
        """Initialize all required components of the application."""
        try:
            self._setup_static_files()
            self._load_model()
            self._setup_database()
            self._setup_routes()
        except Exception as e:
            logger.critical(f"Initialization failed: {e}")
            raise

    def _setup_static_files(self) -> None:
        """Configure static files serving."""
        static_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if not os.path.exists(static_dir):
            raise FileNotFoundError("Templates directory not found")
        self.app.mount("/static", StaticFiles(directory=static_dir), name="static")

    def _load_model(self) -> None:
        """Load the trained machine learning model."""
        model_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
        if not os.path.exists(model_path):
            logger.error("Model file not found")
            raise FileNotFoundError("Model file not found")
        
        try:
            self.model = joblib.load(model_path)
            logger.info("Machine learning model loaded successfully")
        except Exception as e:
            logger.error(f"Model loading error: {e}")
            raise RuntimeError("Failed to load the model")

    def _setup_database(self) -> None:
        """Setup secure database connection."""
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            logger.error("Database URL not provided")
            raise ValueError("Missing DATABASE_URL environment variable")
        
        try:
            self.engine = create_engine(db_url, connect_args={"connect_timeout": 5})
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection established successfully")
        except SQLAlchemyError as e:
            logger.error(f"Database connection error: {e}")
            raise

    def _setup_routes(self) -> None:
        """Setup API routes."""
        self.app.get("/")(self.home)
        self.app.get("/latest-stock")(self.latest_stock)

    async def home(self):
        """Serve the main HTML page."""
        try:
            index_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
            with open(index_path, "r") as file:
                return HTMLResponse(content=file.read())
        except FileNotFoundError:
            logger.error("index.html not found")
            raise HTTPException(status_code=404, detail="Homepage not found")

    async def latest_stock(self) -> Dict[str, Any]:
        """
        Fetch latest stock data and make prediction.
        
        Returns:
            Dictionary with stock data and prediction details
        """
        try:
            query = text("SELECT * FROM stock_data ORDER BY date DESC LIMIT 1")
            latest_data = pd.read_sql_query(query, self.engine)

            if latest_data.empty:
                raise HTTPException(status_code=404, detail="No stock data available")
            
            X_latest = self.prepare_stock_features(latest_data)
            prediction = self.model.predict(X_latest)[0]
            prediction_text = "Up" if prediction == 1 else "Down"
            
            latest_date = latest_data['date'].iloc[0]
            next_date = self._get_next_business_day(latest_date)
            
            return {
                "latest_date": latest_date.strftime("%Y-%m-%d"),
                "next_date": next_date.strftime("%Y-%m-%d"),
                "open_price": float(latest_data['open_price'].iloc[0]),
                "close_price": float(latest_data['close_price'].iloc[0]),
                "volume": int(latest_data['volume'].iloc[0]),
                "prediction": prediction_text
            }
        except SQLAlchemyError as e:
            logger.error(f"Database query error: {e}")
            raise HTTPException(status_code=500, detail="Internal database error")
        except Exception as e:
            logger.error(f"Unexpected prediction error: {e}")
            raise HTTPException(status_code=500, detail="Prediction processing failed")

    def prepare_stock_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare and engineer features for stock prediction.
        """
        features = data.copy()
        features['daily_range'] = features['high_price'] - features['low_price']
        features['price_change_pct'] = ((features['close_price'] - features['open_price']) / features['open_price']) * 100
        features['volatility'] = (features['high_price'] - features['low_price']) / features['open_price']
        return features[['open_price', 'high_price', 'low_price', 'volume', 
                         'daily_range', 'price_change_pct', 'volatility']]

    @staticmethod
    def _get_next_business_day(date: datetime) -> datetime:
        """Calculate the next business day."""
        next_day = date + timedelta(days=1)
        while next_day.weekday() in [5, 6]:
            next_day += timedelta(days=1)
        return next_day

    def run(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        """Run the FastAPI application."""
        uvicorn.run(self.app, host=host, port=port)

def main():
    """Entry point for the application."""
    try:
        stock_app = StockPredictionApp()
        stock_app.run()
    except Exception as e:
        logger.critical(f"Application startup failed: {e}")

if __name__ == "__main__":
    main()
