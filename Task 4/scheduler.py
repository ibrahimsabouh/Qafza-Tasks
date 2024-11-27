import schedule
import subprocess
import time
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename="scheduler.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define the ETL job
def run_etl_job():
    logging.info("Triggering ETL script...")
    try:
        result = subprocess.run(["python", "ETL.py"], capture_output=True, text=True)
        logging.info(result.stdout)
        if result.returncode != 0:
            logging.error(f"ETL script failed with error: {result.stderr}")
        else:
            logging.info("ETL script ran successfully!")
    except Exception as e:
        logging.error(f"Exception occurred while running ETL: {e}")

# Schedule the ETL job to run daily at 10:00 AM
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "10:00")
schedule.every().day.at(SCHEDULE_TIME).do(run_etl_job)

if __name__ == "__main__":
    logging.info("Scheduler started, running ETL job at scheduled times.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Prevent CPU overuse
    except KeyboardInterrupt:
        logging.info("Scheduler stopped manually.")
    except Exception as e:
        logging.error(f"Scheduler stopped due to an error: {e}")
