import streamlit as st
from sqlalchemy import text
import pandas as pd
# IMPORTACIÓN CLAVE: Conectamos directamente con el script corregido de tu backend
from backend.python.prediccionML import ejecutarPrediccionEstudiantes
# importaciones
from servicios.botones import verBotones

def mostrarMotor(conn): # <--- 1. Recibimos el parámetro 'conn' desde app.py
    st.title("🧠 5. Motor de Inteligencia Artificial (Python Prediction Engine)")
    st.write("Generación de analítica predictiva cruzando las dimensiones estructuradas del Data Warehouse.")

    # =========================================================================
    # 2. VALIDACIÓN INTELIGENTE DIRECTA EN LA NUBE (Agregado para evitar bloqueos por F5)
    # =========================================================================
    try:
        # Validamos en un milisegundo si existen registros en la tabla de hechos en Neon
        df_conteo = conn.query("SELECT COUNT(*) as total FROM fact_rendimiento;", ttl=0)
        dw_tiene_datos = int(df_conteo['total'].iloc[0]) > 0
    except Exception:
        dw_tiene_datos = False

    # Condicional que evalúa tanto la base de datos física como la sesión activa
    if not dw_tiene_datos and not st.session_state.get('etl_completado', False):
        st.info("📌 El motor predictivo requiere que el Data Warehouse esté poblado. Ejecute el ETL primero.")
        verBotones(pantalla_anterior="❄️ 4. Modelo Copo de Nieve", pantalla_siguiente="📊 6. Capa Semántica")
        return

    st.subheader("🤖 Ejecución de Algoritmos Predictivos en Tiempo Real")
    st.write("Las características del estudiante han pasado por el Pipeline de Machine Learning para arrojar 4 predicciones críticas:")

    # =========================================================================
    # 3. EJECUCIÓN REAL DEL BACKEND (Modelo .pkl + Actualización en Neon)
    # =========================================================================
    with st.spinner("Cargando modelo `.pkl` y ejecutando inferencias en Neon Cloud..."):
        # Llamamos a tu función del backend pasándole la conexión compartida
        df_predicciones, estado_ml = ejecutarPrediccionEstudiantes(conn)

    if estado_ml != "OK":
        st.error(f"❌ Fallo en el motor de IA: {estado_ml}")
        return

    if df_predicciones.empty:
        st.warning("⚠️ No se pudieron estructurar características suficientes para inicializar las predicciones.")
        return

    # Capturar de forma dinámica el ciclo académico que vino en los datos (ej. '2026-I')
    ciclo_detectado = str(df_predicciones['ciclo_academico'].iloc[0])

    # =========================================================================
    # 4. INTERFAZ VISUAL: FILTRADO INTERACTIVO (Tu Slider original)
    # =========================================================================
    filtro_riesgo = st.slider("Filtrar estudiantes con Probabilidad de Deserción mayor a (%):", 0, 100, 30)
    df_filtrado = df_predicciones[df_predicciones['prob_desercion_ia'] >= filtro_riesgo]

    st.write(f"**Registros predictivos generados (Mostrando {len(df_filtrado)} estudiantes en alerta para el ciclo {ciclo_detectado}):**")
    
    # Renombrar columnas para la visualización final del Frontend (Tu diseño intacto)
    df_interfaz = df_filtrado.rename(columns={
        'Nombre': 'Estudiante',
        'nota_final_curso': 'Nota Base',
        'prob_desercion_ia': '🔮 1. Prob. Deserción (%)',
        'perdida_economica_soles': '🔮 2. Pérdida Económica (S/. )',
        'causa_desercion_probable': '🔮 3. Causa de Deserción Probable',
        'pronostico_curso': '🔮 4. Pronóstico Académico'
    })

    # Selector de columnas para mostrar exactamente lo que tu Frontend requiere
    columnas_mostrar = [
        'Estudiante', 'Nota Base', '🔮 1. Prob. Deserción (%)', 
        '🔮 2. Pérdida Económica (S/. )', '🔮 3. Causa de Deserción Probable', '🔮 4. Pronóstico Académico'
    ]
    st.dataframe(df_interfaz[columnas_mostrar], use_container_width=True, hide_index=True)

    # =========================================================================
    # 5. CIERRE ANALÍTICO: PASO DE PARÁMETRO DINÁMICO AL PROCEDIMIENTO ALMACENADO
    # =========================================================================
    st.divider()
    st.info(f"💡 Las predicciones individuales han reescrito el Data Warehouse. Presione el botón inferior para consolidar los KPIs globales del ciclo **{ciclo_detectado}** en la nube.")
    
    if st.button("📈 Consolidar y Calcular KPIs en la Nube", type="primary"):
        with st.spinner(f"Invocando 'sp_CalcularKPIs(\'{ciclo_detectado}\')' en Neon Cloud..."):
            try:
                # Ejecución transaccional inyectando el ciclo detectado como parámetro de texto
                with conn.session as session:
                    session.execute(text(f"CALL sp_CalcularKPIs('{ciclo_detectado}');"))
                    session.commit()
                
                st.success(f"🎉 ¡Éxito rotundo! Los indicadores globales macro para el ciclo {ciclo_detectado} se han guardado en la tabla 'FactKPIs' de Neon Cloud. Power BI está listo para actualizar sus gráficos.")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Error crítico al ejecutar el procedimiento almacenado analítico: {e}")

    verBotones(pantalla_anterior="❄️ 4. Modelo Copo de Nieve", pantalla_siguiente="📊 6. Capa Semántica")