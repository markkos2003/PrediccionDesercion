import streamlit as st
from servicios.analiticaSemantica import ejecutar_predicciones_ia

def mostrarMotor():
    st.title("🧠 6. Motor de Inteligencia Artificial (Python Prediction Engine)")
    st.write("Generación de analítica predictiva cruzando las dimensiones estructuradas del Data Warehouse.")

    if 'dw_copo_nieve' not in st.session_state:
        st.info("📌 El motor predictivo requiere que el Data Warehouse esté poblado. Ejecute el ETL primero.")
        return

    st.subheader("🤖 Ejecución de Algoritmos Predictivos en Tiempo Real")
    st.write("Las características del estudiante han pasado por el Pipeline de Machine Learning para arrojar 4 predicciones críticas:")

    # Ejecutar motor analítico
    df_predicciones = ejecutar_predicciones_ia(st.session_state['dw_copo_nieve'])

    if df_predicciones.empty:
        st.warning("⚠️ No se pudieron estructurar características suficientes para inicializar las predicciones.")
        return

    # Filtro interactivo rápido de riesgo para impresionar al profesor
    filtro_riesgo = st.slider("Filtrar estudiantes con Probabilidad de Deserción mayor a (%):", 0, 100, 30)
    df_filtrado = df_predicciones[df_predicciones['prob_desercion_ia'] >= filtro_riesgo]

    st.write(f"**Registros predictivos generados (Mostrando {len(df_filtrado)} estudiantes en alerta):**")
    
    # Renombrar columnas para la visualización final del Frontend
    df_interfaz = df_filtrado.rename(columns={
        'Nombre': 'Estudiante',
        'nota_final_curso': 'Nota Base',
        'prob_desercion_ia': '🔮 1. Prob. Deserción (%)',
        'perdida_economica_soles': '🔮 2. Pérdida Económica (S/. )',
        'causa_desercion_probable': '🔮 3. Causa de Deserción Probable',
        'pronostico_curso': '🔮 4. Pronóstico Académico'
    })

    st.dataframe(df_interfaz, use_container_width=True, hide_index=True)

    # Nota de valor de la arquitectura
    st.info("💡 Estas 4 predicciones se actualizan automáticamente en memoria cada vez que nuevos archivos pasan el flujo de Ingesta y ETL.")