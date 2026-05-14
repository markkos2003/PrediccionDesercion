import streamlit as st


def mostrarStaging():
    st.title("🔍 2. Staging Area (Zona de Aterrizaje)")
    st.info("En esta capa se visualizan los datos crudos (Raw Data) antes de cualquier transformación.")

    # Verificamos si hay datos en el diccionario que creamos en Ingesta
    if 'diccionario_datos' in st.session_state and st.session_state['diccionario_datos']:
        datos = st.session_state['diccionario_datos']
        
        # Creamos pestañas dinámicas con los nombres de los archivos
        nombres_archivos = list(datos.keys())
        tabs = st.tabs(nombres_archivos)

        for i, nombre in enumerate(nombres_archivos):
            with tabs[i]:
                st.subheader(f"Datos Crudos: {nombre}")
                
                # Mostramos el DataFrame original sin filtros
                df_actual = datos[nombre]
                
                st.dataframe(df_actual, use_container_width=True)
                
                # Análisis técnico rápido para el profesor
                st.write("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("**Estructura Interna**")
                    st.write(df_actual.dtypes) # Muestra si son números o texto
                with col2:
                    st.write("**Calidad de Datos**")
                    null_count = df_actual.isnull().sum()
                    st.write(null_count[null_count > 0] if null_count.sum() > 0 else "No hay nulos")
                with col3:
                    st.write("**Muestra Aleatoria**")
                    st.write("Verificando consistencia...")
                    st.dataframe(df_actual.sample(min(len(df_actual), 3)))

    elif 'df_original' in st.session_state and st.session_state['df_original'] is not None:
        # Si solo subiste UN archivo (el flujo antiguo)
        st.subheader("Vista del archivo único cargado")
        st.dataframe(st.session_state['df_original'], use_container_width=True)
    else:
        st.error("⚠️ No se detectaron datos. Por favor, cargue archivos en la Fase 1.")