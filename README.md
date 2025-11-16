<div align="center">
  <img src="https://raw.githubusercontent.com/Guilherme450/weather_pipeline/main/app/dashboard/assets/banner.png" alt="Banner do Projeto Weather Pipeline">
</div>

# 🌦️ Weather Data Pipeline

**Weather Data Pipeline** is a robust data engineering project designed to extract, load (EL), and visualize weather data from the OpenWeatherMap API. The pipeline is orchestrated using **Prefect**, ensuring reliable and scheduled data extraction every hour. The collected data is stored in a local SQLite database, and a real-time, interactive dashboard is provided through a **Streamlit** web application.

---

## 🛠️ Technologies Used

<div align="center">
  <a href="https://www.python.org/" target="_blank">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://www.prefect.io/" target="_blank">
    <img src="https://img.shields.io/badge/Prefect-0052FF?style=for-the-badge&logo=prefect&logoColor=white" alt="Prefect">
  </a>
  <a href="https://streamlit.io/" target="_blank">
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  </a>
  <a href="https://plotly.com/python/" target="_blank">
    <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
  </a>
  <a href="https://pandas.pydata.org/" target="_blank">
    <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  </a>
  <a href="https://www.sqlalchemy.org/" target="_blank">
    <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  </a>
  <a href="https://www.sqlite.org/index.html" target="_blank">
    <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  </a>
</div>

---

## 📌 Features

- **Automated Data Extraction:** The pipeline is scheduled to run every hour, ensuring that the weather data is always up-to-date.
- **Interactive Dashboard:** A real-time dashboard built with Streamlit allows for interactive visualization of historical weather data.
- **Secure API Key Management:** API keys are managed securely using `.env` files, keeping sensitive information out of the codebase.
- **Robust Data Orchestration:** Prefect is used to orchestrate the data pipeline, providing reliability, retries, and logging.
- **Local Database:** Weather data is stored in a local SQLite database, making it easy to set up and manage.
- **Data Filtering:** The dashboard provides filtering options, allowing users to analyze weather data for specific months.

---

## 📂 Project Structure

```bash
.
├── app
│   ├── dashboard
│   │   ├── assets
│   │   │   └── banner.png
│   │   └── main.py
│   ├── db_schema
│   │   ├── __init__.py
│   │   └── tables.py
│   └── pipeline
│       ├── EL
│       │   ├── __init__.py
│       │   ├── extract.py
│       │   └── load.py
│       ├── config
│       │   └── api_key.env
│       ├── db
│       │   └── weather_data.db
│       ├── logging_config.py
│       └── weather_flow.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Guilherme450/weather_pipeline.git
   cd weather_pipeline
   ```

2. **Create and activate a virtual environment:**

   - **Linux/Mac:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the API key:**

   - Create a `.env` file inside the `app/pipeline/config/` directory.
   - Add your OpenWeatherMap API key to the `.env` file as follows:
     ```
     API_KEY=your_api_key_here
     ```

---

## ▶️ Usage

1. **Run the data pipeline:**

   - To start the Prefect worker and deploy the data extraction flow, run:
     ```bash
     prefect worker start --pool "default-agent-pool"
     ```
   - In a separate terminal, run the pipeline script to create the deployment:
     ```bash
     python app/pipeline/weather_flow.py
     ```

2. **Run the dashboard:**

   - To launch the Streamlit dashboard, run the following command:
     ```bash
     streamlit run app/dashboard/main.py
     ```

---

## 🚀 Future Improvements

- **Cloud Storage Integration:** Add support for storing data in cloud storage solutions like Amazon S3, Google Cloud Storage, or Azure Blob Storage.
- **Enhanced Dashboard Features:** Improve the dashboard with more advanced visualizations, such as heatmaps and time series analysis.
- **CI/CD Implementation:** Implement a CI/CD pipeline to automate testing and deployment.
- **Containerization:** Dockerize the application to simplify deployment and ensure consistency across different environments.
- **Data Quality Tests:** Add data quality tests to the pipeline to ensure the reliability and accuracy of the data.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 📬 Contact

- **Guilherme** - [LinkedIn](https://www.linkedin.com/in/guilherme-ferreira-340534201/) - [GitHub](https://github.com/Guilherme450)
