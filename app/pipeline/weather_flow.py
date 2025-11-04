"""
Module for orchestrating the EL process and backup for weather data using Prefect.

This module defines tasks for:
  - Extracting weather data from an API.
  - Loading the extracted data into a database.
  - Realizando o backup da base de dados.

Two Prefect flows are defined:
  1. devto_etl: Executa o processo de EL para capturar e carregar os dados do clima.
  2. backup_flow: Inicializa o backup da base de dados, agendado para execução semanal (todo domingo à meia-noite).

The flows are servidos como deployments com cron schedules:
  - 'weather_flow_deployment' para o EL (a cada hora).
  - 'backup_deployment' para o backup (todo domingo à meia-noite).
"""

import os
from dotenv import load_dotenv
from prefect import flow, task
from EL.extract import extract_weather_data
from EL.load import LoadData, DB_DIR

load_dotenv(dotenv_path='config/api_key.env')
os.makedirs(DB_DIR, exist_ok=True)

API_KEY = os.getenv('API_KEY')

CITY = 'Codó'
API_URL = f'https://api.openweathermap.org/data/2.5/weather?&q={CITY}&appid={API_KEY}&units=metric&lang=pt_br'
DB_FILE = os.path.join(DB_DIR, "weather_data.db")

@task(retries=3, retry_delay_seconds=[5, 10, 15])
def extract_data() -> dict:
    """
    Extract weather data from the API.

    Uses the extract_weather_data function with the provided API configuration.

    Returns:
        dict: A dictionary containing the weather data.
    """
    return extract_weather_data(api_url=API_URL, api_key=API_KEY)

@task
def load_data(data: dict) -> None:
    """
    Load weather data into the database.

    Initializes the database connection using LoadData and inserts the provided data.

    Args:
        data (dict): The weather data to load into the database.
    """
    db = LoadData(DB_FILE)
    db.insert_weather_data(data)

'''
@task
def backup_init() -> None:
    """
    Initialize the backup process for the database.

    Instantiates the LoadData class using the database file and triggers the backup procedure.
    """
    db = LoadData(DB_FILE)

    db.initialize_backup()
'''

@flow(name='devto_etl', log_prints=True, timeout_seconds=10)
def weather_flow():
    """
    Orchestrate the ETL process for weather data.

    This Prefect flow executes the following steps:
        1. Extracts the weather data using the extract_data task.
        2. Loads the retrieved data into the database using the load_data task.
    """
    data = extract_data()
    load_data(data)

'''
@flow(name='backup_flow', log_prints=True)
def backup_flow():
    """
    Orchestrate the backup process for the database.

    Executes the backup_init task to initialize the database backup.
    """
    backup_init()
'''

if __name__ == '__main__':
    """
    Entry point of the application.

    Serves two Prefect deployments:
      - 'weather_flow_deployment': Executes the EL process every hour (cron: "0 * * * *").
      - 'backup_deployment': Executes the backup process every Sunday at midnight (cron: "0 0 * * SUN").
    """
    weather_flow.serve(name='weather_flow_deployment', cron="0 * * * *")
    #backup_flow.serve(name='backup_deployment', cron="0 0 * * SUN")