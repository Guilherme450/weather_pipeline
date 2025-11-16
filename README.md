# 🌦️ Weather Data Pipeline

This project is a data pipeline that extracts weather data from the OpenWeatherMap API and loads it into a local SQLite database. The pipeline runs automatically every hour, ensuring the data is always up to date. The project also includes logging, configuration management, and a simple dashboard for data visualization.

## 📋 Table of Contents

- [Features](#-features)
- [Technologies](#-technologies)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Logs & Backups](#-logs--backups)
- [Future Improvements](#-future-improvements)

---

## 📌 Features

- 🔑 **Secure API Key Management**: Uses `.env` files to keep API keys safe and secure.
- **Hourly Data Extraction**: Automatically extracts weather data from the OpenWeatherMap API every hour.
- 💾 **SQLite Database Storage**: Loads the extracted data into a local SQLite database (`weather_data.db`).
- 📝 **Logging System**: Keeps a detailed log of the pipeline's execution for easy monitoring.
- 📊 **Simple Data Dashboard**: Includes a simple and intuitive dashboard for viewing the collected weather data.

---

## 🚀 Technologies

- 🐍 **Python**: The core language for the project.
- 🐘 **SQLAlchemy**: For database interaction and management.
- 💨 **Alembic**: For database schema migrations.
- 📝 **dotenv**: For managing environment variables.

---

## 📂 Project Structure

```shell
.
├── README.md
├── app/
│ ├── backup/
│ ├── dashboard/
│ │ └── main.py
│ ├── db/
│ │ └── weather_data.db
│ └── pipeline/
│ ├── config/
│ │ └── api_key.env
│ ├── log/
│ │ └── app.log
│ ├── extract.py
│ ├── load.py
│ ├── logging_config.py
│ └── pipeline.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Guilherme450/weather_pipeline.git
   cd weather_pipeline
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate  # On Windows
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key:**

   Create a `.env` file in the `app/pipeline/config/` directory and add your OpenWeatherMap API key:

   ```
   API_KEY=your_api_key_here
   ```

---

## ▶️ Usage

1. **Run the pipeline:**

   ```bash
   python app/pipeline/pipeline.py
   ```

2. **Run the dashboard:**

   ```bash
   python app/dashboard/main.py
   ```

---

## 🗂️ Logs & Backups

- **Logs**: The pipeline's execution logs are stored in `app/pipeline/log/app.log`.
- **Backups**: Database backups are saved in the `app/backup/` directory.

---

## 🚀 Future Improvements

- **Cloud Storage**: Add support for cloud storage services like AWS S3, Google Cloud Storage, or Azure Blob Storage.
- **Workflow Automation**: Automate the pipeline scheduling using a tool like Airflow or Prefect.
- **Enhanced Dashboard**: Improve the data dashboard with more advanced visualization libraries like Plotly or Dash.
