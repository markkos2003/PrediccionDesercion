import streamlit as st
import pandas as pd
from servicios.database import guardar_en_staging # Necesitaremos crear esta función

def mostrarStaging():
    st.title("📂 2. Staging Area")
    st.write("Revise los datos validados antes de persistirlos en la base de datos cruda.")

    # 1. Recuperar datos del Session State
    diccionario_datos = st.session_state.get('diccionario_datos', {})

    if not diccionario_datos:
        st.warning("⚠️ No hay datos en memoria. Por favor, cargue archivos válidos en la fase de Ingesta.")
        return

    # 2. Visualización dinámica en Tabs
    nombres_archivos = list(diccionario_datos.keys())
    tabs = st.tabs(nombres_archivos)

    for i, nombre in enumerate(nombres_archivos):
        df = diccionario_datos[nombre]
        with tabs[i]:
            # Creamos dos columnas: una para el título y otra para el botón de eliminar
            col_tit, col_del = st.columns([4, 1])
            
            with col_tit:
                st.subheader(f"Datos de: {nombre}")
            
            with col_del:
                # Botón para eliminar este archivo específico del diccionario
                if st.button("🗑️ Quitar", key=f"del_{nombre}"):
                    del st.session_state['diccionario_datos'][nombre]
                    st.rerun() # Recargamos para que la pestaña desaparezca inmediatamente

            st.dataframe(df, use_container_width=True)
            
            # Botón de descarga individual (como pediste)
            st.download_button(
                label=f"📥 Descargar {nombre} (CSV)",
                data=df.to_csv(index=False),
                file_name=f"staging_{nombre}.csv",
                mime="text/csv",
                key=f"btn_{nombre}" # Key única para evitar errores
            )

    st.divider()

    # 3. EL BOTÓN MAESTRO DE GUARDADO
    st.info("Al presionar el botón, estos archivos se guardarán como tablas 'RAW' en SQLite.")
    if st.button("💾 Confirmar y Guardar en SQLite"):
        # Llamamos al servicio de base de datos
        exito, mensaje = guardar_en_staging(diccionario_datos)
        
        if exito:
            st.success(f"✅ {mensaje}")
            st.balloons()
        else:
            st.error(f"❌ Error al guardar: {mensaje}")