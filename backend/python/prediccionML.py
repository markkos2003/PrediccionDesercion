import os
import pandas as pd
import numpy as np

def ejecutarPrediccionEstudiantes(conn):
    """
    VERSIÓN DE CONTINGENCIA ULTRA RÁPIDA:
    Lee los 4,980 registros del Data Warehouse y genera las métricas visuales
    en la memoria local en milisegundos, omitiendo el guardado pesado en la nube.
    """
    try:
        # 1. Consulta directa y rápida al Data Warehouse en Neon
        query = """
            SELECT 
                f.id_fact, f.nota_final_curso, f.porcentaje_asistencia, 
                f.deuda_pensiones_soles, f.horas_lms_virtual, e.nombre_completo AS "Nombre",
                t.ciclo_academico
            FROM fact_rendimiento f
            INNER JOIN dim_estudiante e ON f.id_estudiante = e.id
            INNER JOIN dim_tiempo t     ON f.id_tiempo = t.id;
        """
        df_nuevos = conn.query(query, ttl=0)
        
        if df_nuevos.empty:
            return pd.DataFrame(), "No existen alumnos cargados en el Data Warehouse."

        # 2. Marcamos un target temporal en memoria (Sin hacer UPDATE en la nube)
        df_nuevos['target_desercion'] = np.where(df_nuevos['porcentaje_asistencia'] < 70, 1, 0)
        
        # 3. Cálculo instantáneo de métricas para la interfaz de Streamlit
        df_nuevos['prob_desercion_ia'] = (100 - df_nuevos['porcentaje_asistencia']) * 0.6 + (20 - df_nuevos['nota_final_curso']) * 2
        df_nuevos['prob_desercion_ia'] = df_nuevos['prob_desercion_ia'].clip(5, 98).round(1)

        # Métrica: Pérdida Económica (S/.)
        df_nuevos['perdida_economica_soles'] = np.where(
            df_nuevos['prob_desercion_ia'] >= 50,
            (df_nuevos['deuda_pensiones_soles'] + 1500).round(2),
            0.0
        )

        # Métrica: Causa Probable
        condiciones = [
            (df_nuevos['nota_final_curso'] < 11) & (df_nuevos['porcentaje_asistencia'] < 70),
            (df_nuevos['deuda_pensiones_soles'] > 500),
            (df_nuevos['porcentaje_asistencia'] < 75)
        ]
        opciones = ['Rendimiento Académico Crítico', 'Problemas Socioeconómicos', 'Inasistencia Crítica']
        df_nuevos['causa_desercion_probable'] = np.select(condiciones, opciones, default='Bajo Riesgo / Estable')

        # Métrica: Pronóstico Académico
        df_nuevos['pronostico_curso'] = np.where(df_nuevos['nota_final_curso'] >= 10.5, 'APROBADO', 'DESAPROBADO')

        return df_nuevos, "OK"
        
    except Exception as e:
        return pd.DataFrame(), f"Error en procesamiento analítico: {str(e)}"