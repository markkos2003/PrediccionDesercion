import streamlit as st
# importaciones
from servicios.botones import verBotones

def mostrarModelo(conn): # <--- 1. Recibimos el parámetro 'conn' desde app.py
    st.title("❄️ 4. Modelo Copo de Nieve (Data Warehouse)")
    st.write("Explore las dimensiones y tablas de hechos normalizadas que alimentarán nuestro motor analítico e Inteligencia Artificial.")

    # =========================================================================
    # 2. VALIDACIÓN INTELIGENTE DIRECTA EN LA NUBE (Reemplaza al session_state)
    # =========================================================================
    try:
        # Consultamos rápidamente si existen registros reales en la tabla de hechos
        df_conteo = conn.query("SELECT COUNT(*) as total FROM fact_rendimiento;", ttl=0)
        dw_tiene_datos = int(df_conteo['total'].iloc[0]) > 0
    except Exception:
        dw_tiene_datos = False

    # Si no hay datos en la nube ni en el estado local de la sesión activa
    if not dw_tiene_datos and not st.session_state.get('etl_completado', False):
        st.info("📌 El Data Warehouse no registra datos aún. Por favor, ejecute el Proceso ETL primero.")
        verBotones(pantalla_anterior="⚙️ 3. Proceso ETL", pantalla_siguiente="🤖 5. Motor de IA")
        return

    # 3. Lista explícita de tus tablas reales creadas en Neon Cloud (Modelo Copo de Nieve)
    lista_tablas = [
        "dim_universidad",
        "dim_carrera",
        "dim_distrito",
        "dim_estudiante",
        "dim_curso",
        "dim_tiempo",
        "dim_socioeconomica",
        "dim_salud",
        "fact_rendimiento",
        "FactKPIs"
    ]
    
    st.subheader("🔍 Visor del Diccionario de Datos del DW")
    tabla_seleccionada = st.selectbox(
        "Seleccione una tabla del Modelo Copo de Nieve para inspeccionar sus registros cargados:",
        lista_tablas,
        format_func=lambda x: f"📋 {x.upper()}"
    )

    try:
        # 4. CONSULTA EN TIEMPO REAL A NEON CLOUD
        # Manejo de comillas dobles obligatorio por la nomenclatura de tu tabla "FactKPIs"
        query_tabla = f'SELECT * FROM "{tabla_seleccionada}";' if tabla_seleccionada == "FactKPIs" else f'SELECT * FROM {tabla_seleccionada};'
        
        # Traemos el dataframe de la nube sin caché (ttl=0) para ver cambios inmediatos
        df_ver = conn.query(query_tabla, ttl=0)
        
        # 5. Métricas e información en tiempo real
        col_inf1, col_inf2 = st.columns(2)
        col_inf1.metric("Registros Poblados en la Nube", len(df_ver))
        col_inf2.metric("Atributos (Columnas)", len(df_ver.columns))

        st.write(f"**Contenido actual de la tabla `{tabla_seleccionada}` en Neon:**")
        st.dataframe(df_ver, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Error al intentar leer la tabla '{tabla_seleccionada}' desde Neon Cloud: {e}")
        return

    # 6. Tu excelente documentación de linaje queda intacta
    st.markdown("---")
    st.markdown("### 📒 Detalles de Linaje de Datos")
    if "universidad" in tabla_seleccionada or "carrera" in tabla_seleccionada:
        st.caption("🔗 *Esta tabla forma parte de la jerarquía de carreras y sub-dimensiones universitarias normalizadas en el Copo de Nieve.*")
    elif "distrito" in tabla_seleccionada or "estudiante" in tabla_seleccionada:
        st.caption("🔗 *Esta tabla representa los datos demográficos y de geolocalización segregados del estudiante para evitar redundancia.*")
    elif "fact" in tabla_seleccionada or "Fact" in tabla_seleccionada:
        st.caption("📊 *Tabla de hechos central. Contiene las llaves foráneas correlacionadas y las métricas de rendimiento y riesgo calculadas.*")
    else:
        st.caption("🛡️ *Dimensión estática de soporte para métricas transversales.*")

    # Corrección menor de tu key de navegación de botones
    verBotones(pantalla_anterior="⚙️ 3. Proceso ETL", pantalla_siguiente="🤖 5. Motor de IA")