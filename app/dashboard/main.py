import os
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
#import dash_bootstrap_components as dbc
#from dash import Dash, html, dcc, callback, Output, Input


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "pipeline", "db")
DB_FILE = os.path.join(DB_DIR, "weather_data.db")

conn = sqlite3.connect(DB_FILE)

df = pd.read_sql('SELECT * FROM Weather_data', con=conn)

copy_df = df.copy()
copy_df['timestamp'] = pd.to_datetime(copy_df['timestamp'])
count_desc = copy_df.value_counts('description', ascending=True)

# Desenvolvimento do dadshbord web com streamlit

st.title("Clima Histórico")

st.markdown("Análise interativa do clima")

st.subheader('Variação da Temperatura')

fig_temperature = px.scatter(copy_df, x='timestamp', y='current_temperature')

st.plotly_chart(fig_temperature, use_container_width=True)

