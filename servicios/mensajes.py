import streamlit as st

def mostrarAdvertencia(mensaje="ADVERTENCIA: No se registran datos en esta fase."):
    """Renderiza un mensaje de advertencia llamativo con CSS personalizado"""
    st.markdown(f"""
        <div style="background-color: #fff3cd; color: #856404; padding: 15px; border-left: 6px solid #ffc107; border-radius: 6px; margin-bottom: 20px;">
            <strong>⚠️ Alerta del Sistema:</strong> {mensaje}
        </div>
    """, unsafe_allow_html=True)

def mostrarExito(mensaje="Operación procesada con éxito."):
    """Renderiza un mensaje de éxito con el check verde corporativo"""
    st.markdown(f"""
        <div style="background-color: #d4edda; color: #155724; padding: 15px; border-left: 6px solid #28a745; border-radius: 6px; margin-bottom: 20px;">
            <strong>✅ Log de Auditoría:</strong> {mensaje}
        </div>
    """, unsafe_allow_html=True)

def mostrarInfo(total_registros):
    """Muestra un mensaje informativo específico para el conteo de los 1,000 registros"""
    st.markdown(f"""
        <div style="background-color: #cce5ff; color: #004085; padding: 15px; border-left: 6px solid #007bff; border-radius: 6px; margin-bottom: 20px;">
            <strong>📋 Registro de Control:</strong> Se han detectado e indexado <b>{total_registros} registros</b> activos cruzando las capas de la arquitectura.
        </div>
    """, unsafe_allow_html=True)