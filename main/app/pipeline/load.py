"""
Module for loading and inserting weather data into a SQLite database.
"""

import os
import csv
import sqlite3
from datetime import datetime
from dataclasses import dataclass, field
from contextlib import contextmanager
from logging_config import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "db")
BACKUP_DIR = os.path.join(BASE_DIR, "app", "backup")

@dataclass
class LoadData:
    """
    Class for handling the loading and insertion of weather data
    into the SQLite database.

    Attributes:
        db_file (str): Path to the SQLite database file.
    """
    db_file: str = field(repr=False)

    def __post_init__(self):
        """
        Post-initialization to setup the database.
        """
        self._init_database()

    @contextmanager
    def get_connection(self):
        """
        Context manager that provides a safe database connection.

        Yields:
            sqlite3.Connection: A SQLite connection with row factory set.

        Raises:
            sqlite3.Error: If a database error occurs.
        """
        conn = None

        try:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f'Error in data base: {e}')
            raise
        finally:
            if conn:
                conn.close()

    def _init_database(self):
        """
        Initialize the database by creating tables and indexes if they do not already exist.
        """
        create_table_sql = """
                CREATE TABLE IF NOT EXISTS Weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    city VARCHAR(255) NOT NULL,
                    country VARCHAR(255) NOT NULL,
                    current_temperature REAL NOT NULL,
                    max_temperature REAL NOT NULL,
                    min_temperature REAL NOT NULL,
                    description TEXT NOT NULL,
                    cloud_percent INTEGER NOT NULL,
                    humidity INTEGER NOT NULL,
                    visibility INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
        """

        create_index_sql = """
                CREATE INDEX IF NOT EXISTS idx_timestamp ON Weather_data(timestamp);
        """

        try:
            with self.get_connection() as conn:
                conn.execute(create_table_sql)
                conn.execute(create_index_sql)
                conn.commit()
                logger.info('Data base initialized with success')
        except Exception as e:
            logger.error(f'Error during initialization of data base: {e}')

    def insert_weather_data(self, weather_info):
        """
        Insert a weather data record into the database.

        Args:
            weather_info (dict): A dictionary containing the weather data. Expected keys:
                - timestamp: Datetime of the record.
                - city: City name.
                - country: Country name.
                - current_temperature: Current temperature.
                - max_temperature: Maximum temperature.
                - min_temperature: Minimum temperature.
                - description: Weather description.
                - cloud_percentage: Cloud coverage percentage.
                - humidity: Humidity value.
                - visibility: Visibility distance.

        Raises:
            Exception: Propagates any exception encountered during database insertion.
        """
        insert_info_sql = """
                INSERT INTO Weather_data (
                    timestamp,
                    city,
                    country,
                    current_temperature,
                    max_temperature,
                    min_temperature,
                    description,
                    cloud_percent,
                    humidity,
                    visibility
                )
                VALUES (?,?,?,?,?,?,?,?,?,?);
        """

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(insert_info_sql, (
                    weather_info['timestamp'],
                    weather_info['city'],
                    weather_info['country'],
                    weather_info['current_temperature'],
                    weather_info['max_temperature'],
                    weather_info['min_temperature'],
                    weather_info['description'],
                    weather_info['cloud_percentage'],
                    weather_info['humidity'],
                    weather_info['visibility']
                ))
                conn.commit()
                logger.info('Meteorological data saved in DB successfully')
        except Exception as e:
            logger.error(f'Error while inserting data to data base: {e}')
            raise
    
    def get_latest_records(self, limit=10):
        """
        Retrieve the latest weather records from the database.

        Args:
            limit (int): Maximum number of records to fetch. Defaults to 10.

        Returns:
            list[sqlite3.Row]: List of weather records ordered by descending timestamp.
                               Returns an empty list if an error occurs.
        """
        select_records_sql = """
                SELECT * FROM Weather_data
                ORDER BY timestamp DESC
                LIMIT ?
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(select_records_sql, (limit,))

                return cursor.fetchall()
        except Exception as e:
            logger.error('Error while consulting data')
            return []

    def initialize_backup(self, file_name='weather_backup.csv'):
        """
        Export recent weather data records to a CSV backup file.

        This function retrieves up to 1000 latest weather records, writes them to a CSV file
        in the designated backup directory, and logs the outcome. No exceptions are raised;
        errors are logged instead.

        Args:
            file_name (str): Name of the CSV file to which data will be exported.
                             Defaults to 'weather_backup.csv'.
        """
        try:
            records = self.get_latest_records(1000)
            os.makedirs(BACKUP_DIR, exist_ok=True)
            file_path = os.path.join(BACKUP_DIR, file_name)

            if not records:
                logger.warning('No data to export')
                return
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
                field_names = [
                    'timestamp', 'city',
                    'country', 'current_temperature',
                    'max_temperature', 'min_temperature',
                    'description', 'cloud_percent',
                    'humidity', 'visibility'
                ]

                writer = csv.DictWriter(csv_file, fieldnames=field_names)
                writer.writeheader()

                for record in records:
                    writer.writerow(dict(record))
                
                logger.info(f'Data exported to {file_name} - {len(records)} registers')
        except Exception as e:
            logger.error(f'Error while exporting to backup: {e}')
