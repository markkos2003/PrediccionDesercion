import streamlit as st
from sqlalchemy import text
import time
# importaciones
from servicios.botones import verBotones

def mostrarEtl(conn): # <--- 1. Recibimos el parámetro 'conn' desde app.py
    st.title("⚙️ 3. Proceso ETL")
    st.write("Extraiga los datos crudos validados, ejecute transformaciones y poble el Data Warehouse.")

    # Consultar en tiempo real a Neon cuántos registros esperan en la tabla física de staging
    try:
        df_conteo = conn.query("SELECT COUNT(*) as total FROM staging_excel;", ttl=0)
        registros_pendientes = df_conteo.iloc[0]['total'] # Captura el número entero
    except Exception:
        registros_pendientes = 0

    # 2. Control de validación física o de sesión
    if registros_pendientes == 0 and ('staging_db_temporal' not in st.session_state or not st.session_state['staging_db_temporal']):
        st.warning("⚠️ No hay datos crudos listos en Staging. Confirme el guardado en la fase anterior.")
        return

    # Si ya corrió el ETL
    if st.session_state.get('etl_completado', False):
        st.success("🎉 ¡El pipeline se ejecutó con éxito! El Modelo Copo de Nieve está disponible en la nube de Neon.")
        if st.button("🔄 Ejecutar de nuevo"):
            st.session_state['etl_completado'] = False
            st.rerun()
        return

    st.subheader("Estado del Repositorio de Ingesta:")
    st.metric(label="📊 Registros pendientes en la nube (staging_excel)", value=registros_pendientes)
    
    if 'staging_db_temporal' in st.session_state and st.session_state['staging_db_temporal']:
        for nombre in st.session_state['staging_db_temporal'].keys():
            st.markdown(f"- 📁 `raw_{nombre.replace('.', '_')}` *(Esperando Normalización en Postgres)*")

    st.divider()

    # 3. EL BOTÓN QUE DISPARA LA MAGIA REAL EN NEON
    if st.button("🪄 Ejecutar Limpieza y Carga Dinámica", type="primary"):
        if registros_pendientes == 0:
            st.error("❌ Error: No existen registros físicos en la tabla 'staging_excel' de Neon para procesar.")
            return

        with st.status("Procesando ETL en Neon Cloud...", expanded=True) as status:
            st.write("📥 [Extracción] Validando registros listos en la zona transaccional...")
            time.sleep(0.6)
            
            st.write("🧼 [Transformación] Invocando reglas de limpieza e ingeniería de variables en PostgreSQL...")
            try:
                # LLAMADA REAL AL PROCEDIMIENTO ALMACENADO QUE COMPILAMOS EN NEON
                with conn.session as session:
                    session.execute(text("CALL sp_EjecutarETLMasivo();"))
                    session.commit()
                
                time.sleep(1.0)
                st.write("❄️ [Carga] Distribuyendo registros vectoriales y poblando el modelo Copo de Nieve...")
                time.sleep(0.6)
                
                # Desactivar la barra temporal de simulación guardando el estado
                st.session_state['dw_copo_nieve'] = True 
                status.update(label="¡Pipeline Finalizado con éxito en Neon!", state="complete")
                
                st.session_state['etl_completado'] = True
                st.success("🚀 Proceso completado en el Servidor Cloud. Avance a la pantalla 'Modelo Copo de Nieve' o actualice Power BI.")
                st.balloons()
                time.sleep(1.5)
                st.rerun()
                
            except Exception as e:
                status.update(label="💥 Fallo en el Pipeline", state="error")
                st.error(f"Error crítico en el procedimiento almacenado de Neon: {e}")

    verBotones(pantalla_anterior="🔍 2. Staging Area", pantalla_siguiente="❄️ 4. Modelo Copo de Nieve")