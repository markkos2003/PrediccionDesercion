import streamlit as st
import pandas as pd
from servicios.validacion import validar_archivos_entrada # Importamos tu servicio

def mostrarIngesta():
    st.title("📥 1. Ingesta de Datos Multiformato")
    st.write("Cargue los archivos de la universidad para su validación técnica.")

    # 1. Subida múltiple
    archivos = st.file_uploader(
        "Cargue uno o varios archivos (Excel, CSV o JSON)", 
        type=["xlsx", "csv", "json"],
        accept_multiple_files=True
    )
    
    if archivos:
        # 2. LLAMADA AL SERVICIO DE VALIDACIÓN
        # El servicio hace el trabajo sucio de leer y chequear columnas
        dfs_validados, errores = validar_archivos_entrada(archivos)
        
        # Mostramos errores si el "Excel de cocina" o archivos vacíos intentan entrar
        for err in errores:
            st.error(err)

        if dfs_validados:
            st.subheader(f"📂 Archivos Validados: {len(dfs_validados)}")
            
            # 3. Creamos pestañas solo para los archivos que pasaron la validación
            nombres_tabs = list(dfs_validados.keys())
            tabs = st.tabs(nombres_tabs)

            for i, nombre in enumerate(nombres_tabs):
                df = dfs_validados[nombre]
                with tabs[i]:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**Vista previa técnica de: {nombre}**")
                        st.dataframe(df.head(5), use_container_width=True)
                    
                    with col2:
                        st.write("**Calidad de Datos:**")
                        st.write(f"📏 Filas: `{df.shape[0]}`")
                        st.write(f"📊 Columnas: `{df.shape[1]}`")
                        st.write(f"❓ Nulos totales: `{df.isna().sum().sum()}`")

            # 4. Guardar en Session State para Staging
            # IMPORTANTE: Aquí solo guardamos en memoria. 
            # El botón de "Confirmar y Guardar en SQLite" estará en la pantalla de STAGING.
            #st.session_state['diccionario_datos'] = dfs_validados
            #st.info("💡 Los archivos han sido validados. Diríjase a la pestaña **2. Staging Area** para confirmar el guardado en la base de datos.")

            # 4. GUARDADO ACUMULATIVO EN EL SESSION STATE (CAMBIO CLAVE)
            # Si la caja de datos no existe en memoria, la inicializamos vacía
            if 'diccionario_datos' not in st.session_state:
                st.session_state['diccionario_datos'] = {}
            
            # Usamos .update() para AÑADIR los nuevos dataframes sin borrar los anteriores
            st.session_state['diccionario_datos'].update(dfs_validados)
            
            # Mensaje informativo dinámico para el usuario
            total_acumulado = len(st.session_state['diccionario_datos'])
            st.success(f"✨ Archivos procesados con éxito. Total acumulado para Staging: {total_acumulado} archivo(s).")
            st.info("💡 Diríjase a la pestaña **2. Staging Area** para revisar el contenido total y confirmar el guardado.")
        else:
            st.warning("No hay archivos válidos para procesar.")