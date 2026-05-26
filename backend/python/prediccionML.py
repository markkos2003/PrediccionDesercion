# backend/python/prediccionML.py
import os
import joblib
import pandas as pd
import numpy as np
from sqlalchemy import text # Importación obligatoria

RUTA_MODELO = os.path.join(os.path.dirname(__file__), 'modeloPredictivo.pkl')

def ejecutarPrediccionEstudiantes(conn):
    """
    Carga el modelo pkl, consulta los alumnos en Neon, actualiza la columna 
    target_desercion en Postgres y calcula las métricas requeridas por el Frontend.
    """
    if not os.path.exists(RUTA_MODELO):
        return pd.DataFrame(), "Error: No se encontró el archivo modeloPredictivo.pkl"

    try:
        # 1. Cargar el modelo entrenado
        modelo = joblib.load(RUTA_MODELO)
        
        # 2. Consulta al DW
        query = """
            SELECT 
                f.id_fact, f.nota_final_curso, f.porcentaje_asistencia, 
                f.deuda_pensiones_soles, f.horas_lms_virtual, e.edad, e.nombre_completo AS "Nombre",
                t.ciclo_academico
            FROM fact_rendimiento f
            INNER JOIN dim_estudiante e ON f.id_estudiante = e.id
            INNER JOIN dim_tiempo t     ON f.id_tiempo = t.id;
        """
        df_nuevos = conn.query(query, ttl=0)
        
        if df_nuevos.empty:
            return pd.DataFrame(), "No existen alumnos cargados en el Data Warehouse."

        # 3. Extraer características para el modelo predictivo
        X_nuevos = df_nuevos[['nota_final_curso', 'porcentaje_asistencia', 'deuda_pensiones_soles', 'horas_lms_virtual', 'edad']]
        
        # 4. Ejecutar predicción real de tu archivo PKL
        df_nuevos['target_desercion'] = modelo.predict(X_nuevos)
        
        # 5. ACTUALIZAR LA BASE DE DATOS EN NEON ENVOLVIENDO EN text()
        with conn.session as session:
            for _, fila in df_nuevos.iterrows():
                session.execute(
                    text("""
                        UPDATE fact_rendimiento 
                        SET target_desercion = :target 
                        WHERE id_fact = :id_f;
                    """),
                    {"target": int(fila['target_desercion']), "id_f": int(fila['id_fact'])}
                )
            session.commit()

        # =========================================================================
        # 6. ENRIQUECER LOS DATOS PARA LAS 4 PREDICCIONES DEL FRONTEND
        # =========================================================================
        df_nuevos['prob_desercion_ia'] = (100 - df_nuevos['porcentaje_asistencia']) * 0.6 + (20 - df_nuevos['nota_final_curso']) * 2
        df_nuevos['prob_desercion_ia'] = np.where(df_nuevos['target_desercion'] == 1, df_nuevos['prob_desercion_ia'] + 20, df_nuevos['prob_desercion_ia'])
        df_nuevos['prob_desercion_ia'] = df_nuevos['prob_desercion_ia'].clip(5, 98).round(1)

        # Métrica 2: Pérdida Económica (S/.)
        df_nuevos['perdida_economica_soles'] = np.where(
            df_nuevos['prob_desercion_ia'] >= 50,
            (df_nuevos['deuda_pensiones_soles'] + 1500).round(2),
            0.0
        )

        # Métrica 3: Causa Probable
        condiciones = [
            (df_nuevos['nota_final_curso'] < 11) & (df_nuevos['porcentaje_asistencia'] < 70),
            (df_nuevos['deuda_pensiones_soles'] > 500),
            (df_nuevos['porcentaje_asistencia'] < 75)
        ]
        opciones = ['Rendimiento Académico Crítico', 'Problemas Socioeconómicos', 'Inasistencia Crítica']
        df_nuevos['causa_desercion_probable'] = np.select(condiciones, opciones, default='Bajo Riesgo / Estable')

        # Métrica 4: Pronóstico Académico
        df_nuevos['pronostico_curso'] = np.where(df_nuevos['nota_final_curso'] >= 10.5, 'APROBADO', 'DESAPROBADO')

        return df_nuevos, "OK"
        
    except Exception as e:
        return pd.DataFrame(), f"Error en procesamiento ML: {str(e)}"