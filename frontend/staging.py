import streamlit as st
import pandas as pd
from servicios.database import guardar_en_staging # Necesitaremos crear esta función
#importaciones
from servicios.botones import verBotones

def mostrarStaging(conn):
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
    #st.info("Al presionar el botón, estos archivos se guardarán como tablas 'RAW' en SQLite.")
    #if st.button("💾 Confirmar y Guardar en SQLite"):
        # Llamamos al servicio de base de datos
     #   exito, mensaje = guardar_en_staging(diccionario_datos)
        
     #   if exito:
     #       st.success(f"✅ {mensaje}")
     #       st.balloons()
     #   else:
     #       st.error(f"❌ Error al guardar: {mensaje}")


     # 3. EL BOTÓN MAESTRO DE GUARDADO (SIMULADO EN MEMORIA)
    st.info("💡 Al presionar el botón, estos archivos se guardarán temporalmente en la zona de Staging listos para el proceso ETL.")
    
    if st.button("💾 Confirmar y Guardar en Staging", type="primary"):
        progreso_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            total_registros = 0
            archivos_procesados = list(diccionario_datos.keys())
            num_archivos = len(archivos_procesados)
            
            for index, nombre_archivo in enumerate(archivos_procesados):
                status_text.text(f"Preparando y transfiriendo: {nombre_archivo}...")
                df_actual = diccionario_datos[nombre_archivo].copy() # Usamos una copia para no alterar la vista previa
                
                # -------------------------------------------------------------
                # MAGIA DEL ETL DE STAGING: ADAPTACIÓN DE ESTRUCTURA IOT
                # -------------------------------------------------------------
                if "IoT_Lector" in nombre_archivo:
                    # 1. Renombramos las columnas para que coincidan EXACTAMENTE con tu tabla de Neon
                    df_actual = df_actual.rename(columns={
                        "dni_estudiante": "dni",
                        "id_curso_ref": "curso" # Temporalmente mapeamos el ID al campo curso en staging
                    })
                    
                    # 2. Creamos las columnas faltantes con None (NULL) para que pandas arme el match perfecto
                    columnas_neon = [
                        "nombre_completo", "sexo", "edad", "estado_civil", "colegio_procedencia", 
                        "distrito", "universidad", "tipo_universidad", "categoria_pension", "carrera", 
                        "facultad", "modalidad", "nivel_ingresos", "trabaja", "tiempo_traslado_min", 
                        "medio_transporte", "conectividad_internet", "estado_emocional", "nivel_estres", 
                        "apoyo_psicologico", "area_academica", "curso_filtro", "creditos", "mes", 
                        "ciclo_academico", "anio", "nota_final_curso", "deuda_pensiones_soles", "horas_lms_virtual"
                    ]
                    for col in columnas_neon:
                        if col not in df_actual.columns:
                            df_actual[col] = None
                    
                    # 3. Eliminamos columnas excedentes que creamos en el simulador y que Neon no espera
                    columnas_a_eliminar = ["horas_presenciales_aula", "origen_datos", "fecha_captura"]
                    df_actual = df_actual.drop(columns=[c for c in columnas_a_eliminar if c in df_actual.columns])
                # -------------------------------------------------------------
                
                # Volcado directo a la tabla unificada en Neon Cloud
                df_actual.to_sql("staging_excel", con=conn.engine, if_exists="append", index=False)
                
                total_registros += len(df_actual)
                progreso_bar.progress(int((index + 1) / num_archivos * 100))
            
            # Guardamos copia de control en memoria
            st.session_state['staging_db_temporal'] = diccionario_datos.copy()
            st.session_state['etl_completado'] = False
            st.session_state['datos_subidos_a_neon'] = True 
            
            status_text.empty()
            progreso_bar.empty()
            
            st.success(f"✅ ¡Éxito! Se insertaron {total_registros:,} registros crudos en la tabla 'staging_excel' de Neon.")
            st.balloons()

        except Exception as e:
            status_text.empty()
            progreso_bar.empty()
            st.error(f"❌ Error crítico de escritura en Neon Cloud: {e}")
    
    if st.session_state.get('datos_subidos_a_neon', False):
        st.divider()
        st.subheader("☁️ Base de Datos Física: Tabla `staging_excel` en Neon")
        st.write("La siguiente tabla representa una consulta directa en tiempo real (`SELECT *`) a tu infraestructura en la nube:")
        
        with st.spinner("Realizando consulta a Neon Cloud..."):
            try:
                # 1. Consultamos los últimos 500 registros ingresados a la tabla de staging
                # Usamos ctid DESC en PostgreSQL para traer los registros más recientes muy rápido
                query_muestra = "SELECT * FROM staging_excel ORDER BY ctid DESC LIMIT 500;"
                df_neon_real = pd.read_sql(query_muestra, con=conn.engine)
                
                # 2. Consultamos la cantidad total histórica de filas en la tabla para mostrar métricas reales
                query_conteo = "SELECT COUNT(*) as total FROM staging_excel;"
                total_en_bd = pd.read_sql(query_conteo, con=conn.engine).iloc[0]['total']
                
                # Diseño de métricas superiores para impresionar en la sustentación
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.metric(label="📊 Volumen Total en Staging (Neon)", value=f"{total_en_bd:,} filas")
                with col_m2:
                    st.metric(label="🌐 Estado del Servidor", value="Conectado (Cloud)", delta="Online")
                
                # 3. Renderizado del DataFrame directo de la Nube
                st.dataframe(df_neon_real, use_container_width=True)
                st.caption("ℹ️ Muestra de los últimos 500 registros indexados en Neon Cloud. Los datos están listos para la Fase 3: Proceso ETL.")
                
            except Exception as e:
                st.warning(f"⚠️ Los datos se subieron, pero hubo un problema al leer la vista previa de Neon: {e}")

    st.divider()
       

    verBotones(pantalla_anterior="📥 1. Fuentes de Datos", pantalla_siguiente="⚙️ 3. Proceso ETL")   