import streamlit as st
import pandas as pd
import time

#importaciones de las pantallas
from modulos.inicio import mostrarInicio
from modulos.ingesta import mostrarIngesta
from modulos.staging import mostrarStaging
from modulos.etl import mostrarEtl
from modulos.modelo import mostrarModelo
from modulos.motorIA import mostrarMotor
from modulos.semantica import mostrarSemantica
from modulos.dashboard import mostrarDashboard
# 1. Configuración de Estilo y Página
st.set_page_config(page_title="MIRA - Sistema Predictivo Lima Norte", layout="wide")

# CSS para mejorar el aspecto visual (Colores y Tarjetas)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    /* Estilo para las tarjetas de métricas (Pantalla 6) */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #004b87;
    }
    
    //* 1. Controlar el tamaño de las imágenes */
    [data-testid="stColumn"] [data-testid="stImage"]img {
        height: 200px !important;         /* Ajusta este valor para cambiar la altura de todas */
        object-fit: cover !important;     /* Esto evita que se deformen, las recorta proporcionalmente */
        width: 100% !important;
        border-radius: 10px;
    }

    /* 2. Estilo de tarjeta para las columnas de Inicio */
    [data-testid="stColumn"] {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        border-bottom: 4px solid #004b87;
        /*ayuda a que las tarjetas midan lo mismo*/
        display:flex;
        flex-direction: column;            
    }

    /* 3. Evitar que el ícono del menú lateral se deforme por la regla anterior */
    [data-testid="stSidebar"] img {
        height: auto !important;
        width: auto !important;
        object-fit: contain !important;
    }
            
    div.stButton > button:first-child { 
            background-color: #004b87; 
            color: white; width: 100%; 
            border-radius: 8px; 
            height: 3em; font-weight: bold; 
            }
    .stProgress > div > div > div > div { background-color: #004b87; }
    </style>
    """, unsafe_allow_html=True)

# 2. Gestión de Memoria (Session State) para que sea DINÁMICO
if 'df_original' not in st.session_state:
    st.session_state['df_original'] = None
if 'etapas_completadas' not in st.session_state:
    st.session_state['etapas_completadas'] = {"ETL": False, "IA": False}

# 3. Menú Lateral con Iconos
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135810.png", width=100)
    st.title("Arquitectura BI")
    st.write("---")
    opcion = st.radio("Seleccione una Fase:", [
        "🏠 Inicio",
        "📥 1. Fuentes de Datos",
        "🔍 2. Staging Area",
        "⚙️ 3. Proceso ETL",
        "❄️ 4. Modelo Copo de Nieve",
        "🤖 5. Motor de IA",
        "📊 6. Capa Semántica",
        "📈 7. Dashboard Final"
    ])

# --- LÓGICA DE LAS PANTALLAS ---

if opcion == "🏠 Inicio":
    mostrarInicio()
    

elif opcion == "📥 1. Fuentes de Datos":
    mostrarIngesta()


elif opcion == "🔍 2. Staging Area":
    mostrarStaging()
elif opcion == "⚙️ 3. Proceso ETL":
    mostrarEtl()

elif opcion == "❄️ 4. Modelo Copo de Nieve":
    mostrarModelo()

elif opcion == "🤖 5. Motor de IA":
    mostrarMotor()
elif opcion == "📊 6. Capa Semántica":
    mostrarSemantica()

elif opcion == "📈 7. Dashboard Final":
    mostrarDashboard()