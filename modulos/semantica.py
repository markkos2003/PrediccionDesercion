import streamlit as st
from servicios.analiticaSemantica import calcular_capa_semantica

def mostrarSemantica():
    st.title("📊 5. Capa Semántica y Reglas de Negocio")
    st.write("Definición lógica de indicadores clave (KPIs) calculados desde el esquema Copo de Nieve.")

    if 'dw_copo_nieve' not in st.session_state:
        st.info("📌 No se registran datos agregados en la capa semántica. Por favor, ejecute el proceso ETL primero.")
        return

    # Calculamos las métricas usando el servicio consolidado
    kpis = calcular_capa_semantica(st.session_state['dw_copo_nieve'])

    if not kpis:
        st.warning("⚠️ Error al procesar los indicadores lógicos.")
        return

    st.subheader("🏁 Tablero de Control de Mando (Balanced Scorecard)")
    
    # Renderizado en cuadrícula de los 4 KPIs estratégicos
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        st.metric(
            label="💰 Dimensión Económica: Tasa de Morosidad", 
            value=f"{kpis['tasa_morosidad']}%", 
            delta="Límite Tolerable: < 15%", 
            delta_color="inverse"
        )
        st.caption("Mide el porcentaje de alumnos que registran cuotas o deudas pendientes en el ciclo actual.")
        
    with col2:
        st.metric(
            label="👥 Dimensión Clientes: Tasa de Deserción Histórica", 
            value=f"{kpis['tasa_desercion_historica']}%", 
            delta="Meta Institucional: < 8%",
            delta_color="inverse"
        )
        st.caption("Porcentaje de abandono registrado formalmente en el lote de datos analizado.")

    st.divider()

    with col3:
        st.metric(
            label="🏥 Dimensión Interna: Alerta de Salud Mental/Estrés", 
            value=f"{kpis['indice_alerta_salud']}%", 
            delta="Urgencia de Intervención", 
            delta_color="off"
        )
        st.caption("Proporción de estudiantes que se encuentran mapeados en rangos de Estrés Alto o Ansiedad Crítica.")
        
    with col4:
        st.metric(
            label="📚 Dimensión Aprendizaje: Engagement Plataforma LMS", 
            value=f"{kpis['horas_lms_promedio']} hrs", 
            delta="Óptimo: > 20 horas / mes"
        )
        st.caption("Tiempo promedio mensual de interacción activa del estudiante dentro de las aulas virtuales.")