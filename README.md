# 🌦️ Weather Data Pipeline

A data pipeline project to **extract and load (EL)** weather data from **OpenWeatherMap API** to a local SQLite database.
The extraction runs automatically **every hour**, ensuring the database is always up to date.  
The project also includes logging, configuration management, and a simple dashboard for data visualization.

---

## 📌 Features
- 🔑 Secure API key management using `.env` files  
- 📥 Extract weather data from an external API **every hour**    
- 💾 Load data into a local SQLite database (`weather_data.db`)  
- 📝 Logging system for monitoring pipeline execution  
- 📊 Simple dashboard for viewing weather data  

---

## 📂 Project Structure
```shell
  $ tree
  WEATHER_PIPELINE/
├── app/
│ ├── backup/ # Backup files
│ ├── dashboard/ # Visualization/dashboard code
│ │ └── main.py
│ ├── db/ # Database
│ │ └── weather_data.db
│ └── pipeline/ # Pipeline scripts
│ ├── pycache/ # Python cache (ignored in git)
│ ├── config/ # Configuration files
│ │ └── api_key.env
│ ├── log/ # Log files
│ │ └── app.log
│ ├── extract.py # Extraction logic
│ ├── load.py # Load logic
│ ├── logging_config.py # Logging configuration
│ └── pipeline.py # Main pipeline execution
│
├── requirements.txt # Python dependencies
├── .gitignore
└── README.md
```

## ⚙️ Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/Guilherme450/weather_pipeline.git
    cd weather_pipeline

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Linux/Mac
    venv\Scripts\activate      # On Windows

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Create a .env file inside `app/pipeline/config/`:
    ```bash
    API_KEY=your_api_key_here

## ▶️ Usage
1. Run the pipeline
    ```bash
    python app/pipeline/pipeline.py

2. Run the dashboard:
    ```bash
    python app/dashboard/main.py

## 🗂️ Logs & Backups
- Logs are stored in `app/pipeline/log/app.log`
- Database backups are saved in `app/backup/`

## 🚀 Future Improvements
- Add cloud storage support (S3, GCP, Azure)

- Automate pipeline scheduling (Airflow/Prefect)

- Enhance dashboard with Plotly or Dash
