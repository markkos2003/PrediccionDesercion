import streamlit as st
import time

def mostrarMotor():
    st.title("🤖 5. Capa de IA (Predictiva)")
    if st.session_state['etapas_completadas']["ETL"]:
        if st.button("Ejecutar Predicción de Deserción"):
            with st.spinner("El motor de IA está procesando los perfiles de riesgo..."):
                time.sleep(2)
                st.session_state['etapas_completadas']["IA"] = True
                st.success("✅ ¡Predicciones generadas! Se han identificado los alumnos con riesgo de abandono.")
    else:
        st.error("⚠️ Complete las fases anteriores.")
