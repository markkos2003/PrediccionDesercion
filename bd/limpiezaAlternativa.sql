-- SCRIPT 02 ALTERNATIVO: Carga Basada en Conjuntos (Enfoque Optimizado No-RBAR)
-- OBJETIVO: Cargar datos masivos eliminando bucles y reduciendo el consumo de RAM.
-- =============================================================================

USE DW_Rendimiento_Academico;
GO

-- 1. CREACIÓN DE LA TABLA DE TRÁNSITO EXCLUSIVA PARA EL PROCESO MASIVO
IF OBJECT_ID('staging_excel_conjuntos', 'U') IS NOT NULL
    DROP TABLE staging_excel_conjuntos;
GO

CREATE TABLE staging_excel_conjuntos (
    dni VARCHAR(8),
    codigo_universitario VARCHAR(15),
    nombre_completo VARCHAR(100),
    sexo VARCHAR(1),
    edad INT,
    estado_civil VARCHAR(20),
    colegio_procedencia VARCHAR(30),
    distrito VARCHAR(50),
    universidad VARCHAR(50),
    tipo_universidad VARCHAR(15),
    categoria_pension VARCHAR(15),
    carrera VARCHAR(50),
    facultad VARCHAR(50),
    modalidad VARCHAR(20),
    nivel_ingresos VARCHAR(20),
    trabaja VARCHAR(2),
    tiempo_traslado_min INT,
    medio_transporte VARCHAR(30),
    conectividad_internet VARCHAR(20),
    estado_emocional VARCHAR(30),
    nivel_estres VARCHAR(15),
    apoyo_psicologico VARCHAR(2),
    curso VARCHAR(50),
    area_academica VARCHAR(40),
    curso_filtro VARCHAR(2),
    creditos DECIMAL(4,1),
    mes VARCHAR(15),
    ciclo_academico VARCHAR(15),
    anio INT,
    nota_final_curso DECIMAL(4,2),
    porcentaje_asistencia INT,
    deuda_pensiones_soles DECIMAL(10,2),
    horas_lms_virtual INT
);
GO

-- 2. PROCEDIMIENTO ALMACENADO OPTIMIZADO POR CONJUNTOS
CREATE PROCEDURE sp_EjecutarETLMasivo
AS
BEGIN
    SET NOCOUNT ON;
    
    -- =========================================================================
    -- PASO A: POBLAR SUB-DIMENSIONES (Solo registros nuevos, con UPPER y TRIM)
    -- =========================================================================
    
    INSERT INTO dim_distrito (nombre, zona_lima, indice_inseguridad)
    SELECT DISTINCT UPPER(TRIM(distrito)), 'LIMA NORTE', 'MEDIA'
    FROM staging_excel_conjuntos s
    WHERE s.distrito IS NOT NULL
      AND NOT EXISTS (
          SELECT 1 FROM dim_distrito d WHERE d.nombre = UPPER(TRIM(s.distrito))
      );

    INSERT INTO dim_universidad (nombre, tipo, distrito_sede, anios_licencia, categoria_pension)
    SELECT DISTINCT UPPER(TRIM(universidad)), UPPER(TRIM(tipo_universidad)), UPPER(TRIM(distrito)), 6, UPPER(TRIM(categoria_pension))
    FROM staging_excel_conjuntos s
    WHERE s.universidad IS NOT NULL
      AND NOT EXISTS (
          SELECT 1 FROM dim_universidad u WHERE u.nombre = UPPER(TRIM(s.universidad))
      );

    INSERT INTO dim_curso (nombre_curso, area_academica, curso_filtro, creditos)
    SELECT DISTINCT UPPER(TRIM(curso)), UPPER(TRIM(area_academica)), 
                    CASE WHEN UPPER(TRIM(curso_filtro)) IN ('SÍ', 'SI') THEN 1 ELSE 0 END, creditos
    FROM staging_excel_conjuntos s
    WHERE s.curso IS NOT NULL
      AND NOT EXISTS (
          SELECT 1 FROM dim_curso c WHERE c.nombre_curso = UPPER(TRIM(s.curso))
      );

    INSERT INTO dim_tiempo (mes, ciclo_academico, anio)
    SELECT DISTINCT UPPER(TRIM(mes)), UPPER(TRIM(ciclo_academico)), anio
    FROM staging_excel_conjuntos s
    WHERE s.ciclo_academico IS NOT NULL
      AND NOT EXISTS (
          SELECT 1 FROM dim_tiempo t WHERE t.ciclo_academico = UPPER(TRIM(s.ciclo_academico))
      );

    -- =========================================================================
    -- PASO B: POBLAR DIMENSIONES PADRE (Estructura Copo de Nieve Cruzada)
    -- =========================================================================

    INSERT INTO dim_carrera (nombre_carrera, facultad, id_universidad, modalidad)
    SELECT DISTINCT UPPER(TRIM(s.carrera)), UPPER(TRIM(s.facultad)), u.id, UPPER(TRIM(s.modalidad))
    FROM staging_excel_conjuntos s
    INNER JOIN dim_universidad u ON UPPER(TRIM(s.universidad)) = u.nombre
    WHERE NOT EXISTS (
        SELECT 1 FROM dim_carrera c 
        WHERE c.nombre_carrera = UPPER(TRIM(s.carrera)) AND c.id_universidad = u.id
    );

    INSERT INTO dim_estudiante (dni, codigo_universitario, nombre_completo, sexo, edad, estado_civil, id_distrito, colegio_procedencia)
    SELECT DISTINCT TRIM(s.dni), TRIM(s.codigo_universitario), UPPER(TRIM(s.nombre_completo)), UPPER(TRIM(s.sexo)), s.edad, UPPER(TRIM(s.estado_civil)), d.id, UPPER(TRIM(s.colegio_procedencia))
    FROM staging_excel_conjuntos s
    INNER JOIN dim_distrito d ON UPPER(TRIM(s.distrito)) = d.nombre
    WHERE NOT EXISTS (
        SELECT 1 FROM dim_estudiante e WHERE e.dni = TRIM(s.dni)
    );

    -- =========================================================================
    -- PASO C: POBLAR DIMENSIONES TRANSACCIONALES EN PARALELO
    -- Mapeamos directamente cada fila del staging para mantener correspondencia 1 a 1.
    -- =========================================================================

    -- Generar ID de control de inicio para el amarre secuencial exacto
    DECLARE @base_socio INT = (SELECT ISNULL(MAX(id), 0) FROM dim_socioeconomica);
    DECLARE @base_salud INT = (SELECT ISNULL(MAX(id), 0) FROM dim_salud);

    INSERT INTO dim_socioeconomica (nivel_ingresos, trabaja, tiempo_traslado_min, medio_transporte, conectividad_internet)
    SELECT UPPER(TRIM(nivel_ingresos)), CASE WHEN UPPER(TRIM(trabaja)) IN ('SÍ', 'SI') THEN 1 ELSE 0 END, tiempo_traslado_min, UPPER(TRIM(medio_transporte)), UPPER(TRIM(conectividad_internet))
    FROM staging_excel_conjuntos;

    INSERT INTO dim_salud (estado_emocional, nivel_estres, apoyo_psicologico)
    SELECT UPPER(TRIM(estado_emocional)), UPPER(TRIM(nivel_estres)), CASE WHEN UPPER(TRIM(apoyo_psicologico)) IN ('SÍ', 'SI') THEN 1 ELSE 0 END
    FROM staging_excel_conjuntos;

    -- =========================================================================
    -- PASO D: ENLACE FINAL VECTORIAL A LA TABLA DE HECHOS (Uso de CTEs)
    -- =========================================================================
    
    WITH StagingOrdenado AS (
        SELECT *, ROW_NUMBER() OVER(ORDER BY (SELECT NULL)) as fila_num 
        FROM staging_excel_conjuntos
    ),
    SocioOrdenado AS (
        SELECT id, ROW_NUMBER() OVER(ORDER BY id) as fila_num 
        FROM dim_socioeconomica WHERE id > @base_socio
    ),
    SaludOrdenado AS (
        SELECT id, ROW_NUMBER() OVER(ORDER BY id) as fila_num 
        FROM dim_salud WHERE id > @base_salud
    )
    INSERT INTO fact_rendimiento (
        id_estudiante, id_carrera, id_socioeconomica, id_salud, id_tiempo, id_curso,
        nota_final_curso, porcentaje_asistencia, deuda_pensiones_soles, horas_lms_virtual, target_desercion
    )
    SELECT 
        e.id, ca.id, se.id, sa.id, t.id, cu.id,
        s.nota_final_curso, s.porcentaje_asistencia, s.deuda_pensiones_soles, s.horas_lms_virtual, 0
    FROM StagingOrdenado s
    INNER JOIN dim_estudiante e      ON TRIM(s.dni) = e.dni
    INNER JOIN dim_universidad u     ON UPPER(TRIM(s.universidad)) = u.nombre
    INNER JOIN dim_carrera ca        ON UPPER(TRIM(s.carrera)) = ca.nombre_carrera AND ca.id_universidad = u.id
    INNER JOIN dim_tiempo t          ON UPPER(TRIM(s.ciclo_academico)) = t.ciclo_academico
    INNER JOIN dim_curso cu          ON UPPER(TRIM(s.curso)) = cu.nombre_curso
    INNER JOIN SocioOrdenado se      ON s.fila_num = se.fila_num
    INNER JOIN SaludOrdenado sa      ON s.fila_num = sa.fila_num;

    -- 3. LIMPIEZA ATÓMICA DE SEGURIDAD
    TRUNCATE TABLE staging_excel_conjuntos;
END;
GO
PRINT 'Script 02 Alternativo: ETL por Conjuntos (Alta Velocidad) compilado con éxito.';