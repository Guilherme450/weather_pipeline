"""
Module for extracting weather data from an API using HTTP requests.

This module provides helper functions to validate the API key and extract weather data.
"""

import requests
from datetime import datetime
from logging_config import logger

# load_dotenv(dotenv_path='api_key.env')  # Initialize API key environment variable
# API_KEY = os.getenv('API_KEY')

def validate_api_key(api_key) -> bool:
    """
    Validate the API key.

    Args:
        api_key (str): API key to validate.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    if not api_key:
        logger.error('API KEY not found')
        return False
    return True

def extract_weather_data(api_url: str, api_key: str, city: str, params=None):
    """
    Extract weather data from the API for the specified city.

    Args:
        api_url (str): URL to the weather API.
        api_key (str): API key for authentication.
        city (str): City for which to extract weather data.
        params (dict, optional): Additional parameters for the API request.

    Returns:
        dict: A dictionary containing weather data with keys:
            - timestamp: Current datetime.
            - city: Name of the city.
            - country: Country code.
            - current_temperature: Current temperature value.
            - max_temperature: Maximum temperature value.
            - min_temperature: Minimum temperature value.
            - description: Weather description.
            - cloud_percentage: Cloud coverage percentage.
            - humidity: Humidity percentage.
            - visibility: Visibility distance.

    Raises:
        requests.exceptions.RequestException: If an HTTP request error occurs.
        Exception: For any other issues during data extraction.
    """
    if not validate_api_key(api_key):
        return

    logger.info('Extraction started')

    try:
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        main_data = data.get('main', {})
        weather_data = data.get('weather', [{}])[0]
        clouds_data = data.get('clouds', {})
        sys_data = data.get('sys', {})

        weather_info = {
            'timestamp': datetime.now(),
            'city': data.get('name', 'unknown'),
            'country': sys_data.get('country'),
            'current_temperature': main_data.get('temp'),
            'max_temperature': main_data.get('temp_max'),
            'min_temperature': main_data.get('temp_min'),
            'description': weather_data.get('description'),
            'cloud_percentage': clouds_data.get('all'),
            'humidity': main_data.get('humidity'),
            'visibility': data.get('visibility')
        }

        return weather_info
    except requests.exceptions.RequestException as e:
        logger.error(f'Error on HTTP request: {e}')
        raise
    except Exception as e:
        logger.error(f'Something went wrong - {e}')
        raise