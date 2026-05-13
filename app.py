import streamlit as st
import pandas as pd
import time

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
    # Título Principal con estilo
    st.markdown("<h1 style='text-align: center; color: #004b87;'>MIRA: Monitor de Indicadores de Riesgo Académico</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #475569;'>Predicción de Deserción Universitaria - Lima Norte</h3>", unsafe_allow_html=True)
    
    st.write("---") # Línea divisoria
    # Creamos 3 columnas para las tarjetas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🏛️ Campus Lima Norte")
        try:
            st.image("imagenes/campusproyect.png", use_container_width=True)
        except:
            st.info("Imagen: Campus")
        st.caption("Sedes monitoreadas en el sector norte.")

    with col2:
        st.markdown("### 👥 Comunidad Estudiantil")
        try:
            st.image("imagenes/estudiantes.jpg", use_container_width=True)
        except:
            st.info("Imagen: Estudiantes")
        st.caption("Análisis de perfiles socioeconómicos.")

    with col3:
        st.markdown("### 🤖 Tecnología IA")
        try:
            st.image("imagenes/Random forest.jpg", use_container_width=True)
        except:
            st.info("Imagen: IA")
        st.caption("Motor predictivo de última generación.")
    # Resumen Ejecutivo
    st.markdown("""
    ###  Objetivo del Proyecto
    Esta plataforma implementa una Arquitectura BI diseñada para identificar patrones de abandono universitario de forma temprana. 
    A través de las 7 capas del sistema, transformamos datos crudos en decisiones estratégicas.
    
    
    """)
    st.info("¿Cómo empezar? Navegue al menú de la izquierda y comience cargando los archivos en la fase 1: Fuentes de Datos.")
    

elif opcion == "📥 1. Fuentes de Datos":
    st.title("📥 1. Ingesta de Datos")
    st.write("Cargue el archivo Excel para iniciar el flujo dinámico.")
    archivo = st.file_uploader("Seleccione el archivo de la Universidad", type=["xlsx", "csv"])
    
    if archivo:
        st.session_state['df_original'] = pd.read_excel(archivo) if archivo.name.endswith('xlsx') else pd.read_csv(archivo)
        st.success("✅ ¡Archivo cargado con éxito! Ahora puede verlo en la fase de Staging.")

elif opcion == "🔍 2. Staging Area":
    st.title("🔍 2. Staging Area (Landing Zone)")
    if st.session_state['df_original'] is not None:
        st.write("Datos crudos detectados en el sistema:")
        st.dataframe(st.session_state['df_original'], use_container_width=True)
        st.caption(f"Total de registros cargados: {len(st.session_state['df_original'])}")
    else:
        st.error("⚠️ No hay datos. Por favor, regrese a la Fase 1 y suba un archivo.")

elif opcion == "⚙️ 3. Proceso ETL":
    st.title("⚙️ 3. Proceso de Transformación (ETL)")
    if st.session_state['df_original'] is not None:
        st.write("Presione el botón para transformar la data cruda en el modelo dimensional.")
        if st.button("🚀 Iniciar Transformación"):
            with st.status("Ejecutando reglas de negocio...", expanded=True) as s:
                st.write("Limpiando duplicados...")
                time.sleep(1)
                st.write("Normalizando tablas de Carreras y Facultades...")
                time.sleep(1)
                st.write("Cargando al Data Warehouse...")
                st.session_state['etapas_completadas']["ETL"] = True
                s.update(label="¡ETL Completado!", state="complete")
            st.balloons()
    else:
        st.error("⚠️ Cargue datos primero.")

elif opcion == "❄️ 4. Modelo Copo de Nieve":
    st.title("❄️ 4. Data Warehouse (Copo de Nieve)")
    if st.session_state['etapas_completadas']["ETL"]:
        st.subheader("Esquema Dimensional Generado")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("**Tablas de Dimensiones:**")
            st.markdown("- `Dim_Estudiante`\n- `Dim_Carrera`\n- `Dim_Facultad`\n- `Dim_Tiempo`")
            st.write("**Tabla de Hechos:**")
            st.markdown("- `Fact_Rendimiento`")
        with col2:
            # Aquí podrías mostrar una vista previa de la tabla de hechos limpia
            st.write("Vista previa de la Tabla de Hechos:")
            st.dataframe(st.session_state['df_original'].head(5))
    else:
        st.warning("⚠️ Debe ejecutar el ETL en la Fase 3 primero.")

elif opcion == "🤖 5. Motor de IA":
    st.title("🤖 5. Capa de IA (Predictiva)")
    if st.session_state['etapas_completadas']["ETL"]:
        if st.button("Ejecutar Predicción de Deserción"):
            with st.spinner("El motor de IA está procesando los perfiles de riesgo..."):
                time.sleep(2)
                st.session_state['etapas_completadas']["IA"] = True
                st.success("✅ ¡Predicciones generadas! Se han identificado los alumnos con riesgo de abandono.")
    else:
        st.error("⚠️ Complete las fases anteriores.")

elif opcion == "📊 6. Capa Semántica":
    st.title("📊 6. Capa Semántica (KPIs)")
    # Esto es visualmente lo que mostraste en tu captura
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Riesgo Crítico", "> 80%", "+2%")
    with col2:
        st.metric("Mora Financiera", "S/ 500", "Límite")
    with col3:
        st.metric("Asistencia Mínima", "70%", "-3%")

elif opcion == "📈 7. Dashboard Final":
    st.title("📈 7. Visualización en Power BI")
    st.write("Análisis ejecutivo final para la toma de decisiones.")
    # Simulación de Dashboard
    st.image("https://docs.microsoft.com/en-us/power-bi/fundamentals/media/desktop-report-view/report-view-new.png", use_container_width=True)
    st.info("💡 En la versión final, aquí se integra el iframe de Power BI Service.")