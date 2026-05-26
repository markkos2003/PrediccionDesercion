import streamlit as st

def obtener_conexion():
    """
    Inicializa y retorna la conexión centralizada a Neon.
    Streamlit administra internamente el pool de conexiones.
    """
    return st.connection("postgresql", type="sql")