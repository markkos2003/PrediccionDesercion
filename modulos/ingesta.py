import streamlit as st
import pandas as pd

def mostrarIngesta():
     #st.title("📥 1. Ingesta de Datos")
     #st.write("Cargue el archivo Excel para iniciar el flujo dinámico.")
     #archivo = st.file_uploader("Seleccione el archivo de la Universidad", type=["xlsx", "csv"])
    
     #if archivo:
     #   st.session_state['df_original'] = pd.read_excel(archivo) if archivo.name.endswith('xlsx') else pd.read_csv(archivo)
     #   st.success("✅ ¡Archivo cargado con éxito! Ahora puede verlo en la fase de Staging.")

     st.title("📥 1. Ingesta de Datos Multiformato")
    
    # 1. Habilitamos la subida múltiple
     archivos = st.file_uploader(
        "Cargue uno o varios archivos (Excel, CSV o JSON)", 
        type=["xlsx", "csv", "json"],
        accept_multiple_files=True  # <--- Esto activa la magia
    )
    
     if archivos:
        st.subheader(f"📂 Archivos detectados: {len(archivos)}")
        
        # Diccionario para guardar todos los dataframes
        lista_dfs = {}

        # 2. Creamos pestañas (Tabs) para las vistas previas
        nombres_pestañas = [f.name for f in archivos]
        tabs = st.tabs(nombres_pestañas)

        for i, archivo in enumerate(archivos):
            with tabs[i]:
                # Leer según extensión
                if archivo.name.endswith('.csv'):
                    df = pd.read_csv(archivo)
                elif archivo.name.endswith('.json'):
                    df = pd.read_json(archivo)
                else:
                    df = pd.read_excel(archivo)

                # Guardar en nuestro diccionario temporal
                lista_dfs[archivo.name] = df

                # 3. Mostrar Vista Previa y Calidad
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Vista previa de: {archivo.name}**")
                    st.dataframe(df.head(5), use_container_width=True)
                
                with col2:
                    st.write("**Estadísticas rápidas:**")
                    st.write(f"📏 Filas: `{df.shape[0]}`")
                    st.write(f"📊 Columnas: `{df.shape[1]}`")
                    st.write(f"❓ Nulos: `{df.isna().sum().sum()}`")

        # 4. Guardar todo en el Session State para que las otras pantallas lo vean
        st.session_state['diccionario_datos'] = lista_dfs
        st.success("✅ Todos los archivos se han cargado en el Staging Area.")
