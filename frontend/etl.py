import streamlit as st
import time
from servicios.procesoEtl import ejecutar_pipeline_etl

def mostrarEtl():
    st.title("⚙️ 3. Proceso ETL")
    st.write("Extraiga los datos crudos validados, ejecute transformaciones y poble el Data Warehouse.")

    if 'staging_db_temporal' not in st.session_state or not st.session_state['staging_db_temporal']:
        st.warning("⚠️ No hay datos crudos listos en Staging. Confirme el guardado en la fase anterior.")
        return

    # Si ya corrió el ETL
    if st.session_state.get('etl_completado', False):
        st.success("🎉 ¡El pipeline se ejecutó con éxito! El Modelo Copo de Nieve está disponible para su visualización.")
        if st.button("🔄 Ejecutar de nuevo"):
            st.session_state['etl_completado'] = False
            st.rerun()
        return

    st.subheader("Archivos pendientes de Procesamiento:")
    pendientes = st.session_state['staging_db_temporal']
    
    for nombre in pendientes.keys():
        st.markdown(f"- 📁 `raw_{nombre.replace('.', '_')}` *(Esperando Normalización)*")

    st.divider()

    if st.button("🪄 Ejecutar Limpieza y Carga Dinámica", type="primary"):
        with st.status("Procesando ETL...", expanded=True) as status:
            st.write("📥 [Extracción] Leyendo tablas desde Staging Area...")
            time.sleep(0.8)
            st.write("🧼 [Transformación] Ejecutando reglas de limpieza e ingeniería de variables...")
            
            # Llamamos a nuestro servicio estructurado
            modelo_copo_nieve = ejecutar_pipeline_etl(pendientes)
            
            time.sleep(1.0)
            st.write("❄️ [Carga] Poblando tablas lógicas del Data Warehouse en memoria...")
            
            # Guardamos el resultado global en sesión
            st.session_state['dw_copo_nieve'] = modelo_copo_nieve
            time.sleep(0.5)
            status.update(label="¡Pipeline Finalizado!", state="complete")
            
        st.session_state['etl_completado'] = True
        st.success("🚀 Proceso completado. Avance a la pantalla 'Modelo Copo de Nieve' para ver los resultados.")
        st.balloons()
        st.rerun()
