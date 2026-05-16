import streamlit as st

def mostrarModelo():
    st.title("❄️ 4. Modelo Copo de Nieve (Data Warehouse)")
    st.write("Explore las dimensiones y tablas de hechos normalizadas que alimentarán nuestro motor analítico e Inteligencia Artificial.")

    # Validar si el ETL ya dejó los datos listos
    if 'dw_copo_nieve' not in st.session_state or not st.session_state['dw_copo_nieve']:
        st.info("📌 El Data Warehouse no registra datos aún. Por favor, ejecute el Proceso ETL primero.")
        return

    dw = st.session_state['dw_copo_nieve']

    # Selector de tablas basado exactamente en tu nuevo diagrama
    lista_tablas = list(dw.keys())
    
    st.subheader("🔍 Visor del Diccionario de Datos del DW")
    tabla_seleccionada = st.selectbox(
        "Seleccione una tabla del Modelo Copo de Nieve para inspeccionar sus registros cargados:",
        lista_tablas,
        format_func=lambda x: f"📋 {x.upper()}"
    )

    # Mostrar la tabla seleccionada con sus estadísticas
    df_ver = dw[tabla_seleccionada]
    
    col_inf1, col_inf2 = st.columns(2)
    col_inf1.metric("Registros Poblados", len(df_ver))
    col_inf2.metric("Atributos (Columnas)", len(df_ver.columns))

    st.write(f"**Contenido actual de la tabla `{tabla_seleccionada}`:**")
    st.dataframe(df_ver, use_container_width=True)

    # Mostrar documentación pequeña de la jerarquía de la tabla seleccionada para impresionar al profesor
    st.markdown("---")
    st.markdown("### 📒 Detalles de Linaje de Datos")
    if "universidad" in tabla_seleccionada or "carrera" in tabla_seleccionada:
        st.caption("🔗 *Esta tabla forma parte de la jerarquía de carreras y sub-dimensiones universitarias normalizadas en el Copo de Nieve.*")
    elif "distrito" in tabla_seleccionada or "estudiante" in tabla_seleccionada:
        st.caption("🔗 *Esta tabla representa los datos demográficos y de geolocalización segregados del estudiante para evitar redundancia.*")
    elif "fact" in tabla_seleccionada:
        st.caption("📊 *Tabla de hechos central. Contiene las llaves foráneas correlacionadas y las métricas de rendimiento y riesgo calculadas.*")
    else:
        st.caption("🛡️ *Dimensión estática de soporte para métricas transversales.*")