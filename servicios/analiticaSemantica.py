import pandas as pd
import numpy as np

def calcular_capa_semantica(dw_data):
    """Calcula las métricas de negocio agregadas (KPIs) desde el Data Warehouse"""
    if not dw_data or 'fact_rendimiento' not in dw_data:
        return {}
        
    fact = dw_data['fact_rendimiento']
    dim_salud = dw_data['dim_salud']
    
    total_alumnos = len(fact)
    
    # KPI 1: Económico - Tasa de Morosidad
    alumnos_con_deuda = len(fact[fact['deuda_pensiones_soles'] > 0])
    tasa_morosidad = (alumnos_con_deuda / total_alumnos) * 100 if total_alumnos > 0 else 0
    
    # KPI 2: Clientes - Tasa de Deserción Cruda (Histórica)
    desertores = len(fact[fact['target_desercion'] == 1])
    tasa_desercion = (desertores / total_alumnos) * 100 if total_alumnos > 0 else 0
    
    # KPI 3: Procesos/Salud - Índice de Alerta Emocional
    # Cruzamos con la dimensión salud para ver cuántos registros tienen estrés Alto o Ansiedad
    ids_criticos_salud = dim_salud[dim_salud['nivel_estres'] == 'Alto']['id'].tolist()
    alumnos_estresados = len(fact[fact['id_salud'].isin(ids_criticos_salud)])
    indice_alerta_salud = (alumnos_estresados / total_alumnos) * 100 if total_alumnos > 0 else 0
    
    # KPI 4: Aprendizaje - Promedio de Horas LMS
    horas_lms_promedio = fact['horas_lms_virtual'].mean() if total_alumnos > 0 else 0
    
    return {
        "tasa_morosidad": round(tasa_morosidad, 1),
        "tasa_desercion_historica": round(tasa_desercion, 1),
        "indice_alerta_salud": round(indice_alerta_salud, 1),
        "horas_lms_promedio": round(horas_lms_promedio, 1),
        "total_alumnos": total_alumnos
    }

def ejecutar_predicciones_ia(dw_data):
    """Simula el motor de IA generando las 4 predicciones a nivel de estudiante"""
    if not dw_data or 'fact_rendimiento' not in dw_data:
        return pd.DataFrame()
        
    fact = dw_data['fact_rendimiento'].copy()
    dim_estudiante = dw_data['dim_estudiante']
    
    # Unimos con los datos del estudiante para mostrar nombres en las predicciones
    resultado_ia = fact.merge(dim_estudiante, on='id_estudiante')
    
    # Generamos las 4 Predicciones Analíticas solicitadas basándonos en sus features reales:
    
    # Predicción 1 (Clientes): Probabilidad de Deserción Individual (%)
    # Usamos combinaciones lógicas de sus datos (asistencia, notas) para simular la IA
    resultado_ia['prob_desercion_ia'] = (
        (100 - resultado_ia['porcentaje_asistencia']) * 0.4 + 
        (20 - resultado_ia['nota_final_curso']) * 3
    ).clip(5, 98).round(1)
    
    # Predicción 2 (Económico): Impacto Financiero Estimado en Soles si deserta
    resultado_ia['perdida_economica_soles'] = (resultado_ia['deuda_pensiones_soles'] + 3500).round(2)
    
    # Predicción 3 (Salud): Predicción de Causa Principal (¿Es Deserción por Estrés/Salud?)
    resultado_ia['causa_desercion_probable'] = np.where(
        resultado_ia['prob_desercion_ia'] > 50,
        np.where(resultado_ia['id_salud'].isin([2, 3]), 'Riesgo Crítico por Estrés/Salud', 'Riesgo Financiero/Académico'),
        'Estable / Bajo Riesgo'
    )
    
    # Predicción 4 (Aprendizaje): Pronóstico de Condición Final del Curso
    # Si la nota proyectada es menor a 10.5, el modelo predice "Desaprobado"
    resultado_ia['pronostico_curso'] = np.where(resultado_ia['nota_final_curso'] >= 10.5, 'Aprobado', 'Reprobado en Riesgo')
    
    # Devolvemos un dataframe limpio con los campos necesarios para las visualizaciones
    columnas_finales = [
        'id_estudiante', 'Nombre', 'nota_final_curso', 'prob_desercion_ia', 
        'perdida_economica_soles', 'causa_desercion_probable', 'pronostico_curso'
    ]
    # Retornamos solo las columnas mapeadas que existan en el merge
    cols_a_entregar = [c for c in columnas_finales if c in resultado_ia.columns]
    
    return resultado_ia[cols_a_entregar]