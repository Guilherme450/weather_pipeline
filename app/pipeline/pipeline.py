"""
Module for extracting and loading weather data, scheduling periodic tasks, and supporting
database backup. The module retrieves weather data from the OpenWeather API and stores it
in a local SQLite database.

Functions:
    job(db: LoadData):
        Fetches weather data and inserts it into the database.
        
    main():
        Initializes the database, performs an initial data extraction, and schedules periodic
        tasks including hourly data extraction and weekly backups.
"""

import os
import schedule
from time import sleep
from dotenv import load_dotenv
from icecream import ic
from extract import extract_weather_data
from load import LoadData, DB_DIR
from logging_config import logger

# Load environment variables from the specified file.
load_dotenv(dotenv_path='config/api_key.env')
os.makedirs(DB_DIR, exist_ok=True)

API_KEY = os.getenv('API_KEY')

CITY = 'Codó'
API_URL = f'https://api.openweathermap.org/data/2.5/weather?&q={CITY}&appid={API_KEY}&units=metric&lang=pt_br'
DB_FILE = os.path.join(DB_DIR, "weather_data.db")

def job(db: LoadData):
    """
    Execute a job to extract weather data and insert it into the database.

    Args:
        db (LoadData): The database interface for storing weather data.
    """
    data = extract_weather_data(API_URL, API_KEY, CITY)
    
    if data:
        db.insert_weather_data(data)

def main():
    """
    Main function to initialize database operations, perform initial weather data extraction,
    and schedule periodic tasks.

    Tasks:
        - Extract current weather data and insert it into the database.
        - Schedule hourly weather data extraction.
        - Schedule weekly database backup every Sunday at midnight.
        - Continuously run scheduled tasks until interrupted.
    """
    logger.info('=== INITIALIZING METEOROLOGICAL DATA COLLECTOR ===')

    try:
        db = LoadData(DB_FILE)  # Initialize the database.

        logger.info('Executing the first data collection...')
        info_data = extract_weather_data(API_URL, API_KEY, CITY)
        db.insert_weather_data(info_data)

        schedule.every(1).hours.do(job, db)
        schedule.every().sunday.at("00:00").do(db.initialize_backup)

        while True:
            schedule.run_pending()
            sleep(60)
    except KeyboardInterrupt:
        logger.info('Program interrupted by user')
    except Exception as e:
        logger.error(f'Error in the main program: {e}')

if __name__ == '__main__':
    main()