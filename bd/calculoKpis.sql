-- SCRIPT 03: Capa Semántica e Indicadores Clave de Rendimiento (Lab 7 Rúbrica)
-- OBJETIVO: Calcular agregaciones multidimensionales nativas y poblar FactKPIs.
-- =============================================================================

USE DW_Rendimiento_Academico;
GO

-- [NOTA PARA EL ALUMNO]: Python leerá este script y reemplazará la etiqueta 
-- {{CICLO_ACTIVO}} con el ciclo seleccionado en la interfaz (ej. '2026-I') 
-- antes de mandarlo a ejecutar.

-- 1. LIMPIEZA PREVIA (Evita registros duplicados si el usuario recalcula el ciclo)
DELETE f 
FROM FactKPIs f
INNER JOIN dim_tiempo t ON f.id_tiempo = t.id
WHERE t.ciclo_academico = '{{CICLO_ACTIVO}}';
GO

-- =============================================================================
-- 2. CÓMPUTO E INSERCIÓN DE KPIS NATIVOS (Operaciones Multidimensionales)
-- =============================================================================

-- KPI 1: Tasa de Aprobación Institucional
-- Mide el porcentaje de alumnos que superan la nota mínima de 10.5
INSERT INTO FactKPIs (id_tiempo, nombre_kpi, valor_calculado, meta_negocio, fecha_calculo)
SELECT 
    t.id,
    'Tasa Aprobación General',
    (COUNT(CASE WHEN f.nota_final_curso >= 10.5 THEN 1 END) * 100.0) / COUNT(*),
    75.0, -- Meta institucional establecida
    GETDATE()
FROM fact_rendimiento f
INNER JOIN dim_tiempo t ON f.id_tiempo = t.id
WHERE t.ciclo_academico = '{{CICLO_ACTIVO}}'
GROUP BY t.id;

-- KPI 2: Índice de Morosidad Crítica Financiera
-- Porcentaje de estudiantes únicos con deudas vigentes en Lima Norte
INSERT INTO FactKPIs (id_tiempo, nombre_kpi, valor_calculado, meta_negocio, fecha_calculo)
SELECT 
    t.id,
    'Morosidad Crítica Estudiantil',
    (COUNT(DISTINCT CASE WHEN f.deuda_pensiones_soles > 0 THEN f.id_estudiante END) * 100.0) / COUNT(DISTINCT f.id_estudiante),
    15.0, -- Tolerancia máxima del negocio (15%)
    GETDATE()
FROM fact_rendimiento f
INNER JOIN dim_tiempo t ON f.id_tiempo = t.id
WHERE t.ciclo_academico = '{{CICLO_ACTIVO}}'
GROUP BY t.id;

-- KPI 3: Ratio de Ausentismo de Alto Riesgo
-- Porcentaje de cursos donde el alumno asistió a menos del 70% de clases
INSERT INTO FactKPIs (id_tiempo, nombre_kpi, valor_calculado, meta_negocio, fecha_calculo)
SELECT 
    t.id,
    'Ausentismo Alarma (Menor al 70%)',
    (COUNT(CASE WHEN f.porcentaje_asistencia < 70 THEN 1 END) * 100.0) / COUNT(*),
    8.0, -- Meta: Mantener el ausentismo crítico por debajo del 8%
    GETDATE()
FROM fact_rendimiento f
INNER JOIN dim_tiempo t ON f.id_tiempo = t.id
WHERE t.ciclo_academico = '{{CICLO_ACTIVO}}'
GROUP BY t.id;

-- KPI 4: Intensidad de Interacción en Aula Virtual (LMS)
-- Promedio de horas dedicadas a la plataforma digital por ciclo académico
INSERT INTO FactKPIs (id_tiempo, nombre_kpi, valor_calculado, meta_negocio, fecha_calculo)
SELECT 
    t.id,
    'Promedio Mensual Horas LMS',
    AVG(CAST(f.horas_lms_virtual AS DECIMAL(6,2))),
    40.0, -- Meta: Mínimo 40 horas de actividad digital por ciclo
    GETDATE()
FROM fact_rendimiento f
INNER JOIN dim_tiempo t ON f.id_tiempo = t.id
WHERE t.ciclo_academico = '{{CICLO_ACTIVO}}'
GROUP BY t.id;
GO

PRINT 'Script 03: Capa Semántica computada. Los 4 KPIs nativos fueron guardados en FactKPIs.';