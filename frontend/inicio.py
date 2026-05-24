import streamlit as st

#importaciones
from servicios.botones import verBotones

def mostrarInicio():
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
    verBotones(pantalla_anterior=None, pantalla_siguiente="📥 1. Fuentes de Datos")