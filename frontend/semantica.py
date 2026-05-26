import streamlit as st
# importaciones
from servicios.botones import verBotones

def mostrarSemantica(conn): # <--- 1. Recibimos el parámetro 'conn' desde app.py
    st.title("📊 6. Capa Semántica y Reglas de Negocio") # Ajustado correlativo visual de tu menú
    st.write("Definición lógica de indicadores clave (KPIs) calculados desde el esquema Copo de Nieve.")

    # 2. Validar que el ETL y las lógicas previas ya se ejecutaron
    if not st.session_state.get('etl_completado', False):
        st.info("📌 No se registran datos agregados en la capa semántica. Por favor, ejecute el proceso ETL primero.")
        verBotones(pantalla_anterior="🤖 5. Motor de IA", pantalla_siguiente="📈 7. Dashboard Final")
        return

    try:
        # =========================================================================
        # 3. EXTRACCIÓN DE LOS KPIS REALES DESDE NEON CLOUD
        # =========================================================================
        # Jalamos los indicadores agregados calculados por tu procedimiento almacenado en Neon
        query_kpis = 'SELECT nombre_kpi, valor_calculado FROM "FactKPIs" ORDER BY fecha_calculo DESC LIMIT 10;'
        df_kpis_db = conn.query(query_kpis, ttl=0)
        
        # Jalamos las horas LMS directamente desde la tabla de hechos en modo Promedio
        query_lms = 'SELECT AVG(horas_lms_virtual) as promedio_lms FROM fact_rendimiento;'
        df_lms_db = conn.query(query_lms, ttl=0)
        
    except Exception as e:
        st.error(f"❌ Error al consultar la Capa Semántica en Neon: {e}")
        return

    # Mapeo por si la tabla de KPIs aún no se ha consolidado en el botón anterior
    # Creamos un diccionario base con valores de respaldo calculados sobre tu query
    kpis = {
        'tasa_morosidad': 0.0,
        'tasa_desercion_historica': 0.0,
        'indice_alerta_salud': 0.0,
        'horas_lms_promedio': 0.0
    }

    if not df_kpis_db.empty:
        # Extraemos dinámicamente los valores asignados en tu script SQL
        for _, fila in df_kpis_db.iterrows():
            nombre = fila['nombre_kpi']
            valor = round(float(fila['valor_calculado']), 1)
            
            if nombre == 'Morosidad Crítica Estudiantil':
                kpis['tasa_morosidad'] = valor
            elif nombre == 'Tasa Aprobación General':
                # Lo convertimos a tasa de desaprobación/deserción estimada para tu indicador visual
                kpis['tasa_desercion_historica'] = round(100.0 - valor, 1)
            elif nombre == 'Ausentismo Alarma (Menor al 70%)':
                kpis['indice_alerta_salud'] = valor

    if not df_lms_db.empty and df_lms_db['promedio_lms'].iloc[0] is not None:
        kpis['horas_lms_promedio'] = round(float(df_lms_db['promedio_lms'].iloc[0]), 1)

    # =========================================================================
    # 4. RENDERIZADO VISUAL (Conserva tu espectacular Balanced Scorecard intacto)
    # =========================================================================
    st.subheader("🏁 Tablero de Control de Mando (Balanced Scorecard)")
    
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
            label="👥 Dimensión Clientes: Tasa de Deserción Histórica Proyectada", 
            value=f"{kpis['tasa_desercion_historica']}%", 
            delta="Meta Institucional: < 8%",
            delta_color="inverse"
        )
        st.caption("Porcentaje de desaprobación y riesgo registrado formalmente en el lote de datos analizado.")

    st.divider()

    with col3:
        st.metric(
            label="🏥 Dimensión Interna: Ratio de Ausentismo de Alarma", 
            value=f"{kpis['indice_alerta_salud']}%", 
            delta="Meta Institucional: < 8%", 
            delta_color="inverse"
        )
        st.caption("Porcentaje de cursos donde la asistencia del estudiante es menor al 70% crítico.")
        
    with col4:
        st.metric(
            label="📚 Dimensión Aprendizaje: Engagement Plataforma LMS", 
            value=f"{kpis['horas_lms_promedio']} hrs", 
            delta="Óptimo: > 40 horas / ciclo"
        )
        st.caption("Tiempo promedio de interacción activa del estudiante dentro de las aulas virtuales de la institución.")

    verBotones(pantalla_anterior="🤖 5. Motor de IA", pantalla_siguiente="📈 7. Dashboard Final")