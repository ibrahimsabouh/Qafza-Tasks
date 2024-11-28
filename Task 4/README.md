# Stock Market Prediction Application
## 🚀 Project Overview
This is a sophisticated, end-to-end stock market prediction application that leverages machine learning, automated data pipelines, and web technologies to provide real-time stock price direction predictions.

## 📊 Key Features
- **Automated Data Collection**
  - Daily stock data extraction from Alpha Vantage API
  - Scheduled ETL (Extract, Transform, Load) process
  - PostgreSQL database integration
- **Machine Learning**
  - XGBoost classifier for stock price direction prediction
  - Advanced feature engineering
  - Cross-validation model evaluation
  - Model persistence and retraining
- **Web Application**
  - FastAPI backend
  - Real-time stock prediction endpoint
  - Responsive web interface
  - Comprehensive logging and error handling

## 📦 Prerequisites
- Python 3.8+
- PostgreSQL
- Alpha Vantage API key

## 📂 Project Structure
```
.
│
├── app.py              # FastAPI main application
├── model.py            # ML model training script
├── ETL.py              # Data extraction script
├── scheduler.py        # Automated task scheduler
├── requirements.txt    # Python dependencies
├── model.joblib        # Trained ML model
├── .env                # Environment variables
├── templates/
│   └── index.html      # Web interface
│
└── README.md           # Project documentation
```

## 🔧 Installation
1. Clone the repository and navigate to the folder
```bash
git clone --no-checkout https://github.com/ibrahimsabouh/Qafza-Tasks.git
cd Qafza-Tasks
```

2. Set up sparse checkout and download only the Task 4 folder
```bash
git sparse-checkout init
git sparse-checkout set "Task 4"
git checkout main
cd "Task 4"
```

3. Create a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Unix/macOS
python3 -m venv .venv
source .venv/bin/activate
```

4. Install dependencies
```bash
pip install -r requirements.txt
```

## 🔐 Configuration
Create a `.env` file in the project root with the following variables:
```
# Alpha Vantage API Configuration
API_KEY=your_alpha_vantage_api_key
STOCK_SYMBOL=AAPL

# PostgreSQL Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/your_database
DB_NAME=your_database_name
USER=your_postgres_username
PASSWORD=your_postgres_password
HOST=localhost
PORT=5432

# Scheduler Configuration
SCHEDULE_TIME=10:00
```

## 🚀 Running the Application
### 1. Database Setup
Create the `stock_data` table in PostgreSQL:
```sql
CREATE TABLE stock_data (
    date DATE PRIMARY KEY,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume BIGINT
);
```

### 2. ETL Process
Extract and load stock data:
```bash
python ETL.py
```

### 3. Train Machine Learning Model
Build predictive model:
```bash
python model.py
```

### 4. Start Web Application
Run the FastAPI application:
```bash
python app.py
```
- Web Interface: `http://127.0.0.1:8000`
- API Docs: `http://127.0.0.1:8000/docs`
- Latest Stock Data: `http://127.0.0.1:8000/latest-stock`

### 5. Start Scheduler (Optional)
Run automated daily data retrieval:
```bash
python scheduler.py
```

## 🔬 Machine Learning Details
- **Algorithm**: XGBoost Classifier
- **Target**: Stock Price Direction (Up/Down)
- **Features**:
  - Open Price
  - High Price
  - Low Price
  - Volume
  - Daily Price Range
  - Price Change Percentage
  - Price Volatility

## 🐞 Logging
Comprehensive logging across multiple log files:
- `stock_prediction.log`: Application events
- `scheduler.log`: Scheduler activities
- `etl.log`: Data extraction details
- `model_training.log`: Model training process

## 📧 Contact
Ibrahim Sabouh
- Email: ibrahim.sabouh7@gmail.com
- GitHub: [ibrahimsabouh](https://github.com/ibrahimsabouh/Qafza-Tasks)
