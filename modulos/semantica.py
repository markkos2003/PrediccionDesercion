import streamlit as st


def mostrarSemantica():
    st.title("📊 6. Capa Semántica (KPIs)")
    # Esto es visualmente lo que mostraste en tu captura
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Riesgo Crítico", "> 80%", "+2%")
    with col2:
        st.metric("Mora Financiera", "S/ 500", "Límite")
    with col3:
        st.metric("Asistencia Mínima", "70%", "-3%")
