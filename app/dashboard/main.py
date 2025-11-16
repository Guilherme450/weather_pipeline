import os
import pandas as pd
import plotly.express as px
#import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import create_engine, text
#from icecream import ic
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "pipeline", "db")
DB_FILE = os.path.join(DB_DIR, "weather_data.db")

engine = create_engine(f'sqlite:///{DB_FILE}')

@st.cache_data(ttl=60)
def load_weather_data():
    """
    Carrega dados do banco de dados com cache de 60 segundos.
    O cache se invalida automaticamente a cada minuto, permitindo atualizações frequentes.
    """
    with engine.connect() as con:
        query = con.execute(
            text(
            """
                SELECT 
                    timestamp, 
                    current_temperature, 
                    max_temperature, 
                    min_temperature, 
                    description,
                    humidity,
                    visibility
                FROM Weather_data;
            """
            ))
        
        df = pd.DataFrame(query.fetchall())
        df.columns = query.keys()
    
    return df

df = load_weather_data()

df['timestamp'] = pd.to_datetime(df['timestamp'])

# Sidebar com filtros
st.sidebar.title("🔍 Filtros")

# Botão de refresh manual
if st.sidebar.button("🔄 Atualizar Dados", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.sidebar.divider()

# Extrair meses disponíveis
df['year_month'] = df['timestamp'].dt.to_period('M')
meses_disponiveis = sorted(df['year_month'].unique(), reverse=True)
meses_labels = [str(mes) for mes in meses_disponiveis]

mes_selecionado = st.sidebar.selectbox(
    "Selecione o mês:",
    options=meses_labels,
    index=0
)

# Filtrar dados pelo mês selecionado
df_filtrado = df[df['year_month'] == pd.Period(mes_selecionado, 'M')]
df_filtrado['timestamp'] = pd.to_datetime(df_filtrado['timestamp'])

st.title("Histórico Climático")

st.markdown("Análise interativa do clima de Codó")

# Exibir timestamp da última atualização
with st.container():
    col_update = st.columns(1)[0]
    with col_update:
        st.caption(f"🔄 Última atualização: {pd.to_datetime(df['timestamp'].max()).strftime('%d/%m/%Y %H:%M:%S')}")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🌡️ Temperatura Atual",
        value=f"{df_filtrado['current_temperature'].iloc[-1]:.1f}°C" if len(df_filtrado) > 0 else "N/A",
        delta=f"{df_filtrado['current_temperature'].iloc[-1] - df_filtrado['current_temperature'].iloc[-2]:.1f}°C" if len(df_filtrado) > 1 else None
    )

with col2:
    st.metric(
        label="📈 Temperatura Máxima",
        value=f"{df_filtrado['max_temperature'].max():.1f}°C" if len(df_filtrado) > 0 else "N/A"
    )

with col3:
    st.metric(
        label="📉 Temperatura Mínima",
        value=f"{df_filtrado['min_temperature'].min():.1f}°C" if len(df_filtrado) > 0 else "N/A"
    )

with col4:
    st.metric(
        label="💧 Umidade",
        value=f"{df_filtrado['humidity'].mean():.1f}%" if len(df_filtrado) > 0 else "N/A"
    )

# Desenvolvimento do dadshbord web com streamlit

st.subheader('Variação da Temperatura')

fig_temperature = px.line(df_filtrado, x='timestamp', y='current_temperature', text="current_temperature")
fig_temperature.update_traces(
    textposition="bottom right",
    line=dict(shape="spline", smoothing=0.8)
)

st.plotly_chart(fig_temperature, use_container_width=True)

st.subheader('Frequência de Estado Atmosférico')

desc_counts = df_filtrado['description'].value_counts().reset_index()
desc_counts.columns = ['description', 'count']
fig_description = px.bar(desc_counts, x='count', y='description', orientation='h')
fig_description.update_traces(textposition="outside")

st.plotly_chart(fig_description, use_container_width=True)

