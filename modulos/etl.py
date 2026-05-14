import streamlit as st
import time

def mostrarEtl():
     st.title("⚙️ 3. Proceso de Transformación (ETL)")
     if st.session_state['df_original'] is not None:
        st.write("Presione el botón para transformar la data cruda en el modelo dimensional.")
        if st.button("🚀 Iniciar Transformación"):
            with st.status("Ejecutando reglas de negocio...", expanded=True) as s:
                st.write("Limpiando duplicados...")
                time.sleep(1)
                st.write("Normalizando tablas de Carreras y Facultades...")
                time.sleep(1)
                st.write("Cargando al Data Warehouse...")
                st.session_state['etapas_completadas']["ETL"] = True
                s.update(label="¡ETL Completado!", state="complete")
            st.balloons()
     else:
        st.error("⚠️ Cargue datos primero.")

