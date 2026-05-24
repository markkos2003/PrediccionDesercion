import streamlit as st

def verBotones(pantalla_anterior=None, pantalla_siguiente=None, texto_aceptar="Aceptar y Continuar ➡️"):
    """
    Renderiza los 3 botoncitos básicos de interacción solicitados por el profesor:
    Cancelar (limpia sesión), Regresar (va atrás) y Aceptar (va adelante).
    """
    st.divider()
    col_cancelar, col_regresar, col_aceptar = st.columns(3)
    
    # Recuperamos el nombre de la fase actual para construir un ID único por pantalla
    fase_act = st.session_state.get('fase_actual', 'global')
    
    # 1. BOTÓN CANCELAR
    with col_cancelar:
        if st.button("❌ Cancelar Operación", use_container_width=True, key=f"btn_cxl_{fase_act}"):
            st.session_state.clear()  # Vacía la memoria por completo
            st.toast("Operación abortada. Datos restablecidos.", icon="🧹")
            st.session_state['fase_actual'] = "📂 1. Ingesta"
            st.rerun()
            
    # 2. BOTÓN REGRESAR
    with col_regresar:
        deshabilitar_regresar = True if pantalla_anterior is None else False
        if st.button("⬅️ Regresar", use_container_width=True, disabled=deshabilitar_regresar, key=f"btn_reg_{fase_act}"):
            st.session_state['fase_actual'] = pantalla_anterior
            st.rerun()
            
    # 3. BOTÓN ACEPTAR / CONTINUAR
    with col_aceptar:
        deshabilitar_siguiente = True if pantalla_siguiente is None else False
        if st.button(texto_aceptar, type="primary", use_container_width=True, disabled=deshabilitar_siguiente, key=f"btn_ok_{fase_act}"):
            st.session_state['fase_actual'] = pantalla_siguiente
            st.rerun()