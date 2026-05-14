import streamlit as st


def mostrarModelo():
    st.title("❄️ 4. Data Warehouse (Copo de Nieve)")
    if st.session_state['etapas_completadas']["ETL"]:
        st.subheader("Esquema Dimensional Generado")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("**Tablas de Dimensiones:**")
            st.markdown("- `Dim_Estudiante`\n- `Dim_Carrera`\n- `Dim_Facultad`\n- `Dim_Tiempo`")
            st.write("**Tabla de Hechos:**")
            st.markdown("- `Fact_Rendimiento`")
        with col2:
            # Aquí podrías mostrar una vista previa de la tabla de hechos limpia
            st.write("Vista previa de la Tabla de Hechos:")
            st.dataframe(st.session_state['df_original'].head(5))
    else:
        st.warning("⚠️ Debe ejecutar el ETL en la Fase 3 primero.")
