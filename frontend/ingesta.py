import streamlit as st
import pandas as pd
from servicios.validacion import validar_archivos_entrada # Importamos tu servicio
from servicios.botones import verBotones
def mostrarIngesta():
    st.title("📥 1. Ingesta de Datos Multiformato")
    st.write("Cargue los archivos de la universidad para su validación técnica.")

    if 'diccionario_datos' not in st.session_state:
        st.session_state['diccionario_datos'] = {}

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
            
            
            # Usamos .update() para AÑADIR los nuevos dataframes sin borrar los anteriores
            st.session_state['diccionario_datos'].update(dfs_validados)
            
            # Mensaje informativo dinámico para el usuario
            total_acumulado = len(st.session_state['diccionario_datos'])
            st.success(f"✨ Archivos procesados con éxito. Total acumulado para Staging: {total_acumulado} archivo(s).")
            st.info("💡 Diríjase a la pestaña **2. Staging Area** para revisar el contenido total y confirmar el guardado.")
        else:
            st.warning("No hay archivos válidos para procesar.")
    
    
    st.divider()
    st.write("### 🤖 Dispositivos Automatizados")

    
    if st.button(" DATOS DEL DISPOSITIVO  IOT LECTOR DE ASISTENCIA",type="primary",icon="📥",):
        with st.spinner("Conectando con el dispositivo IoT y extrayendo logs..."):
            import random
            from datetime import datetime, timedelta

            datos_iot = []
            for _ in range(5000):
                dni_ficticio = f"{random.randint(10000000, 99999999)}"
                cod_univ = f"U202{random.randint(1,6)}{random.randint(10000, 99999)}"
                id_curso_ficticio = random.randint(1, 10)
                porcentaje_asistencia = random.randint(40, 100)
                horas_marcas = random.randint(2, 6)

                datos_iot.append({
                    "dni_estudiante": dni_ficticio,
                    "codigo_universitario": cod_univ,
                    "id_curso_ref": id_curso_ficticio,
                    "porcentaje_asistencia": porcentaje_asistencia,
                    "horas_presenciales_aula": horas_marcas,
                    "origen_datos": "DISPOSITIVO_IOT_RFID_AULA",
                    "fecha_captura": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M:%S")
                })

            df_iot = pd.DataFrame(datos_iot)

            
            # Nombre único para este lote
            nombre_lote_iot = f"IoT_Lector_Asistencia_{datetime.now().strftime('%H%M%S')}"
            
            # Guardamos en el diccionario global (para que Staging lo vea)
            st.session_state['diccionario_datos'][nombre_lote_iot] = df_iot
            
            # Guardamos una referencia al ÚLTIMO IoT cargado solo para mostrarlo en esta pantalla
            st.session_state['ultimo_iot_cargado'] = {
                'nombre': nombre_lote_iot,
                'df': df_iot
            }
            st.rerun()
    if 'ultimo_iot_cargado' in st.session_state:

        iot_info = st.session_state['ultimo_iot_cargado']
        st.subheader(f"📊 Vista Previa en Tiempo Real: {iot_info['nombre']}")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("**Primeros registros capturados por el sensor:**")
            # Mostramos las primeras filas y usamos todo el ancho
            st.dataframe(iot_info['df'].head(10), use_container_width=True)
        with col2:
            st.write("**Métricas de Carga IoT:**")
            st.metric(label="Registros Totales", value=f"{iot_info['df'].shape[0]} 📥")
            st.metric(label="Campos Capturados", value=f"{iot_info['df'].shape[1]} 📊")
            st.info("✨ Estos datos ya están indexados en la memoria de Staging.")        

       
        

     
     
     
   
    
    
        
    



    
    
    verBotones(pantalla_anterior="🏠 Inicio", pantalla_siguiente="🔍 2. Staging Area")       