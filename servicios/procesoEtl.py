import pandas as pd
import numpy as np

def generar_datos_dimension(df_origen, columnas_mapeo, nombre_id, columnas_extra_ficticias=None):
    """
    Función utilitaria para extraer dimensiones únicas de forma dinámica.
    Permite añadir columnas extra con datos simulados si el archivo original no las tiene.
    """
    # Identificar qué columnas de mapeo sí existen en el DataFrame original
    cols_existentes = [c for c in columnas_mapeo if c in df_origen.columns]
    
    if cols_existentes:
        dim = df_origen[cols_existentes].drop_duplicates().reset_index(drop=True)
    else:
        # Si no encuentra columnas, genera una fila de ejemplo genérica
        dim = pd.DataFrame([{columnas_mapeo[0]: "General / No Especificado"}])
        
    dim[nombre_id] = dim.index + 1
    
    # Reordenar para que el ID vaya primero
    columnas_ordenadas = [nombre_id] + [c for c in dim.columns if c != nombre_id]
    dim = dim[columnas_ordenadas]
    
    # Añadir datos simulados consistentes para el prototipo si se requieren campos nuevos
    if columnas_extra_ficticias:
        for col, opciones in columnas_extra_ficticias.items():
            dim[col] = [opciones[i % len(opciones)] for i in range(len(dim))]
            
    return dim

def ejecutar_pipeline_etl(dict_archivos_staging):
    """
    Procesador centralizado. Toma los archivos crudos de Staging 
    y devuelve un diccionario con las tablas del Modelo Copo de Nieve.
    """
    # Unificamos los archivos presentes en Staging
    if not dict_archivos_staging:
        return {}
        
    df_base = pd.concat(dict_archivos_staging.values(), ignore_index=True)
    
    # Asegurar nombres de columnas estándar temporales para evitar caídas por mayúsculas/minúsculas
    df_base.columns = [c.strip() for c in df_base.columns]

    # =========================================================================
    # 1. DIMENSIONES DE SUB-NIVEL (Copo de Nieve Extendido)
    # =========================================================================
    
    # dim_universidad (Saca datos de dim_carrera en tu jerarquía)
    dim_universidad = generar_datos_dimension(
        df_base, ['Universidad'], 'id_universidad',
        columnas_extra_ficticias={
            'tipo': ['Privada', 'Pública'],
            'distritoSede': ['Lima Norte', 'Lima Centro', 'Trujillo'],
            'aniosLicencia': [6, 8, 6],
            'categoriaPension': ['Escala B', 'Escala A', 'Escala C']
        }
    )
    
    # dim_distrito (Saca datos de residencia o procedencia)
    dim_distrito = generar_datos_dimension(
        df_base, ['Distrito', 'distrito_residencia'], 'id_distrito',
        columnas_extra_ficticias={
            'Zona_lima': ['Lima Norte', 'Lima Este', 'Lima Centro', 'Lima Sur'],
            'indice_inseguridad': ['Medio', 'Alto', 'Bajo', 'Medio']
        }
    )
    if 'Nombre' in dim_distrito.columns:
        dim_distrito = dim_distrito.rename(columns={'Nombre': 'nombre'})
    elif dim_distrito.shape[1] == 1: # Si se creó vacía por falta de columnas
        dim_distrito.insert(1, 'nombre', ['Los Olivos', 'Comas', 'San Martin', 'Ate'][:len(dim_distrito)])

    # =========================================================================
    # 2. DIMENSIONES DIRECTAS CONECTADAS A LA FACT TABLE
    # =========================================================================
    
    # dim_carrera
    dim_carrera = generar_datos_dimension(df_base, ['Carrera', 'Facultad', 'modalidad'], 'id_carrera')
    # Relacionamos dinámicamente con Universidad (Copo de Nieve)
    dim_carrera['id_universidad'] = (dim_carrera['id_carrera'] % len(dim_universidad)) + 1
    
    # dim_estudiante
    dim_estudiante = generar_datos_dimension(df_base, ['ID_Estudiante', 'Nombre', 'Sexo', 'Edad', 'DNI', 'estado_civil', 'colegio_procedencia'], 'id_estudiante')
    dim_estudiante['id_distrito'] = (dim_estudiante['id_estudiante'] % len(dim_distrito)) + 1

    # dim_curso
    dim_curso = generar_datos_dimension(df_base, ['Curso', 'nombre_curso', 'area_academica', 'curso_filtro', 'creditos'], 'id_curso')

    # dim_salud
    dim_salud = pd.DataFrame({
        'id': range(1, 6),
        'estado_emocional': ['Estable', 'Ansiedad Moderada', 'Estrés Alto', 'Estable', 'Depresión Leve'],
        'nivel_estres': ['Bajo', 'Medio', 'Alto', 'Bajo', 'Medio'],
        'apoyo_psicologico': [False, True, True, False, True]
    })

    # dim_socioeconomica
    dim_socioeconomica = pd.DataFrame({
        'id': range(1, 6),
        'nivel_ingresos': ['Medio-Bajo', 'Medio', 'Bajo', 'Alto', 'Medio-Alto'],
        'trabaja': [False, True, False, False, True],
        'tiempo_traslado_min': [45, 60, 90, 20, 40],
        'medio_transporte': ['Autobús', 'Metropolitano', 'Colectivo', 'Auto Propio', 'Tren'],
        'conectividad_internet': ['Buena', 'Regular', 'Mala', 'Excelente', 'Buena']
    })

    # dim_tiempo
    dim_tiempo = pd.DataFrame({
        'id': range(1, 5),
        'mes': ['Marzo', 'Agosto', 'Noviembre', 'Enero'],
        'ciclo_academico': ['2026-I', '2026-II', '2026-I', '2026-Verano'],
        'anio': [2026, 2026, 2026, 2026]
    })

    # =========================================================================
    # 3. TABLA DE HECHOS CENTRAL (fact_rendimiento)
    # =========================================================================
    # Reutilizamos las filas del DataFrame original simulando las métricas requeridas
    fact_rendimiento = pd.DataFrame()
    fact_rendimiento['id_estudiante'] = (df_base.index % len(dim_estudiante)) + 1
    fact_rendimiento['id_carrera'] = (df_base.index % len(dim_carrera)) + 1
    fact_rendimiento['id_socioeconomica'] = (df_base.index % len(dim_socioeconomica)) + 1
    fact_rendimiento['id_salud'] = (df_base.index % len(dim_salud)) + 1
    fact_rendimiento['id_tiempo'] = (df_base.index % len(dim_tiempo)) + 1
    fact_rendimiento['id_curso'] = (df_base.index % len(dim_curso)) + 1
    
    # Extraer métricas directas si existen o generarlas de forma consistente
    fact_rendimiento['nota_final_curso'] = df_base['Promedio_Notas'] if 'Promedio_Notas' in df_base.columns else (df_base['Promedio_Ponderado'] if 'Promedio_Ponderado' in df_base.columns else np.random.uniform(10, 18, len(df_base))).round(2)
    fact_rendimiento['porcentaje_asistencia'] = df_base['Asistencia_Pct'] if 'Asistencia_Pct' in df_base.columns else (df_base['Asistencia_%'] if 'Asistencia_%' in df_base.columns else np.random.randint(70, 100, len(df_base)))
    fact_rendimiento['deuda_pensiones_soles'] = df_base['Deuda_Total'] if 'Deuda_Total' in df_base.columns else (df_base['Deuda_Pendiente'] if 'Deuda_Pendiente' in df_base.columns else np.random.choice([0, 500, 1200, 0], len(df_base)))
    fact_rendimiento['horas_lms_virtual'] = df_base['Uso_LMS_Horas'] if 'Uso_LMS_Horas' in df_base.columns else np.random.randint(5, 50, len(df_base))
    fact_rendimiento['target_desercion'] = df_base['Riesgo_IA'].apply(lambda x: 1 if x > 0.6 else 0) if 'Riesgo_IA' in df_base.columns else (df_base['Riesgo_Desercion'] if 'Riesgo_Desercion' in df_base.columns else np.random.choice([0, 1], len(df_base)))

    # Retornamos el Modelo Copo de Nieve estructurado tal cual tu última captura de imagen
    return {
        "dim_universidad": dim_universidad,
        "dim_distrito": dim_distrito,
        "dim_carrera": dim_carrera,
        "dim_estudiante": dim_estudiante,
        "dim_curso": dim_curso,
        "dim_salud": dim_salud,
        "dim_socioeconomica": dim_socioeconomica,
        "dim_tiempo": dim_tiempo,
        "fact_rendimiento": fact_rendimiento
    }