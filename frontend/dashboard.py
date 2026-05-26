import streamlit as st
# importaciones
from servicios.botones import verBotones

def mostrarDashboard():
    st.title("📈 7. Dashboard Final")
    st.write("Panel de Control Gerencial con visualizaciones interactivas en tiempo real conectadas a Neon Cloud.")

    # 1. Mensaje de advertencia técnica previo
    st.info("💡 **Guía de Navegación Gerencial:** El cuadro de mando se encuentra estructurado en 4 bloques funcionales superiores e inferiores. Utilice la fila de filtros desplegables de la parte superior para segmentar el análisis por sede universitaria, carrera o periodo académico.")

    # =========================================================================
    # 2. INCRUSTACIÓN DEL REPORTE DE POWER BI (EMBEDDED IFRAME)
    # =========================================================================
    # Reemplaza el enlace de abajo por la URL pública definitiva que genere tu compañero
    url_publica_powerbi = "https://app.powerbi.com/view?r=eyJrIjoiOTM2ZGE1NjYtYzQ0NS00OGZmLTk1ZTEtMTNjMWNlZWMyZGE1IiwidCI6ImM0YTY2YzM0LTJiYjctNDUxZi04YmUxLWIyYzI2YTQzMDE1OCIsImMiOjR9"
    
    # Renderizado responsivo con el tamaño ideal para pantallas Full HD
    # 'scrolling=True' permite que si el profesor maneja una pantalla pequeña, pueda moverse con comodidad
    st.components.v1.iframe(src=url_publica_powerbi, height=750, scrolling=True)

    st.divider()
    
    # 3. Documentación del Cuadro de Mando (Para impresionar al jurado)
    st.markdown("### 📋 Estructura General del Gobierno de Datos")
    
    col_doc1, col_doc2 = st.columns(2)
    
    with col_doc1:
        st.markdown("""
        *   **Zona Superior (Filtros Desplegables):** Segmentación por Universidad, Carrera, Distrito y Periodo.
        *   **Zona Izquierda (Tarjetas Operativas):** KPIs de Aprobación, Morosidad, Ausentismo y Engagement LMS procesados por el SP.
        """)
        
    with col_doc2:
        st.markdown("""
        *   **Zona Central (Métricas Predictivas IA):** Proporción de Alertas, Riesgo por Facultad/Salud y Pérdida Financiera en Soles.
        *   **Zona Derecha (Estadísticas de Soporte):** Histogramas poblacionales, ratios laborales, tendencias de notas y ranking crítico de alumnos.
        """)

    # 4. Navegación final del proyecto
    # Colocamos pantalla_siguiente=None para denotar que aquí culmina el flujo del software
    verBotones(pantalla_anterior="📊 6. Capa Semántica", pantalla_siguiente=None)

