-- SCRIPT 02: Proceso ETL utilizando Cursores Nativos con Limpieza e Integridad
-- OBJETIVO: Recorrer datos, aplicar UPPER/TRIM, transformar tipos y cargar el DW.
-- =============================================================================

USE DW_Rendimiento_Academico;
GO

-- 1. CREACIÓN DE UNA TABLA DE TRÁNSITO (STAGING)
-- Python dejará caer los datos del Excel aquí temporalmente para que el Cursor los procese.
IF OBJECT_ID('staging_excel_cursores', 'U') IS NOT NULL
    DROP TABLE staging_excel_cursores;
GO

CREATE TABLE staging_excel_cursores (
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
    trabaja VARCHAR(2), -- 'Sí' o 'No'
    tiempo_traslado_min INT,
    medio_transporte VARCHAR(30),
    conectividad_internet VARCHAR(20),
    estado_emocional VARCHAR(30),
    nivel_estres VARCHAR(15),
    apoyo_psicologico VARCHAR(2), -- 'Sí' o 'No'
    curso VARCHAR(50),
    area_academica VARCHAR(40),
    curso_filtro VARCHAR(2), -- 'Sí' o 'No'
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

-- 2. PROCEDIMIENTO ALMACENADO CON LA LÓGICA DE CURSORES DEL PROFESOR (CON BLINDAJE)
CREATE PROCEDURE sp_EjecutarETLCursores
AS
BEGIN
    SET NOCOUNT ON;

    -- Variables para almacenar los datos de cada fila durante el recorrido
    DECLARE @v_dni VARCHAR(8), @v_codigo VARCHAR(15), @v_nombre VARCHAR(100), @v_sexo VARCHAR(1), @v_edad INT, @v_estado_civil VARCHAR(20), @v_colegio VARCHAR(30),
            @v_distrito VARCHAR(50), @v_universidad VARCHAR(50), @v_tipo_uni VARCHAR(15), @v_cat_pension VARCHAR(15), @v_carrera VARCHAR(50), @v_facultad VARCHAR(50), 
            @v_modalidad VARCHAR(20), @v_nivel_ingresos VARCHAR(20), @v_trabaja VARCHAR(2), @v_tiempo_traslado INT, @v_medio_transporte VARCHAR(30), @v_conectividad VARCHAR(20),
            @v_estado_emocional VARCHAR(30), @v_nivel_estres VARCHAR(15), @v_apoyo_psicologico VARCHAR(2), @v_curso VARCHAR(50), @v_area_ac_curso VARCHAR(40), 
            @v_filtro_curso VARCHAR(2), @v_creditos DECIMAL(4,1), @v_mes VARCHAR(15), @v_ciclo VARCHAR(15), @v_anio INT, @v_nota DECIMAL(4,2), @v_asistencia INT, 
            @v_deuda DECIMAL(10,2), @v_horas_lms INT;

    -- Variables para capturar los IDs generados de las dimensiones
    DECLARE @id_distrito INT, @id_universidad INT, @id_carrera INT, @id_socio INT, @id_salud INT, @id_curso INT, @id_tiempo INT, @id_estudiante INT;

    -- DECLARACIÓN DEL CURSOR (Requerimiento pedagógico del Lab 6)
    DECLARE cursor_etl CURSOR FOR 
    SELECT 
        dni, codigo_universitario, nombre_completo, sexo, edad, estado_civil, colegio_procedencia,
        distrito, universidad, tipo_universidad, categoria_pension, carrera, facultad, modalidad,
        nivel_ingresos, trabaja, tiempo_traslado_min, medio_transporte, conectividad_internet,
        estado_emocional, nivel_estres, apoyo_psicologico, curso, area_academica, curso_filtro, creditos,
        mes, ciclo_academico, anio, nota_final_curso, porcentaje_asistencia, deuda_pensiones_soles, horas_lms_virtual
    FROM staging_excel_cursores;

    OPEN cursor_etl;

    -- Capturar la primera fila del staging
    FETCH NEXT FROM cursor_etl INTO 
        @v_dni, @v_codigo, @v_nombre, @v_sexo, @v_edad, @v_estado_civil, @v_colegio,
        @v_distrito, @v_universidad, @v_tipo_uni, @v_cat_pension, @v_carrera, @v_facultad, @v_modalidad,
        @v_nivel_ingresos, @v_trabaja, @v_tiempo_traslado, @v_medio_transporte, @v_conectividad,
        @v_estado_emocional, @v_nivel_estres, @v_apoyo_psicologico, @v_curso, @v_area_ac_curso, @v_filtro_curso, @v_creditos,
        @v_mes, @v_ciclo, @v_anio, @v_nota, @v_asistencia, @v_deuda, @v_horas_lms;

    -- Bucle de procesamiento secuencial
    WHILE @@FETCH_STATUS = 0
    BEGIN
        
        -- A. Procesar sub-dimensión: dim_distrito (Con UPPER y TRIM)
        SELECT @id_distrito = id FROM dim_distrito WHERE nombre = UPPER(TRIM(@v_distrito));
        IF @id_distrito IS NULL
        BEGIN
            INSERT INTO dim_distrito (nombre, zona_lima, indice_inseguridad) 
            VALUES (UPPER(TRIM(@v_distrito)), 'LIMA NORTE', 'MEDIA');
            SET @id_distrito = SCOPE_IDENTITY();
        END

        -- B. Procesar sub-dimensión: dim_universidad (Con UPPER y TRIM)
        SELECT @id_universidad = id FROM dim_universidad WHERE nombre = UPPER(TRIM(@v_universidad));
        IF @id_universidad IS NULL
        BEGIN
            INSERT INTO dim_universidad (nombre, tipo, distrito_sede, anios_licencia, categoria_pension) 
            VALUES (UPPER(TRIM(@v_universidad)), UPPER(TRIM(@v_tipo_uni)), UPPER(TRIM(@v_distrito)), 6, UPPER(TRIM(@v_cat_pension)));
            SET @id_universidad = SCOPE_IDENTITY();
        END

        -- C. Procesar dimensión padre: dim_carrera (Relacionada a Universidad)
        SELECT @id_carrera = id FROM dim_carrera WHERE nombre_carrera = UPPER(TRIM(@v_carrera)) AND id_universidad = @id_universidad;
        IF @id_carrera IS NULL
        BEGIN
            INSERT INTO dim_carrera (nombre_carrera, facultad, id_universidad, modalidad) 
            VALUES (UPPER(TRIM(@v_carrera)), UPPER(TRIM(@v_facultad)), @id_universidad, UPPER(TRIM(@v_modalidad)));
            SET @id_carrera = SCOPE_IDENTITY();
        END

        -- D. Procesar dimensión padre: dim_estudiante (Relacionada a Distrito)
        SELECT @id_estudiante = id FROM dim_estudiante WHERE dni = TRIM(@v_dni);
        IF @id_estudiante IS NULL
        BEGIN
            INSERT INTO dim_estudiante (dni, codigo_universitario, nombre_completo, sexo, edad, estado_civil, id_distrito, colegio_procedencia)
            VALUES (TRIM(@v_dni), TRIM(@v_codigo), UPPER(TRIM(@v_nombre)), UPPER(TRIM(@v_sexo)), @v_edad, UPPER(TRIM(@v_estado_civil)), @id_distrito, UPPER(TRIM(@v_colegio)));
            SET @id_estudiante = SCOPE_IDENTITY();
        END

        -- E. Procesar dimensión: dim_curso
        SELECT @id_curso = id FROM dim_curso WHERE nombre_curso = UPPER(TRIM(@v_curso));
        IF @id_curso IS NULL
        BEGIN
            INSERT INTO dim_curso (nombre_curso, area_academica, curso_filtro, creditos) 
            VALUES (UPPER(TRIM(@v_curso)), UPPER(TRIM(@v_area_ac_curso)), CASE WHEN UPPER(TRIM(@v_filtro_curso)) = 'SÍ' OR UPPER(TRIM(@v_filtro_curso)) = 'SI' THEN 1 ELSE 0 END, @v_creditos);
            SET @id_curso = SCOPE_IDENTITY();
        END

        -- F. Procesar dimensión: dim_tiempo
        SELECT @id_tiempo = id FROM dim_tiempo WHERE ciclo_academico = UPPER(TRIM(@v_ciclo));
        IF @id_tiempo IS NULL
        BEGIN
            INSERT INTO dim_tiempo (mes, ciclo_academico, anio) VALUES (UPPER(TRIM(@v_mes)), UPPER(TRIM(@v_ciclo)), @v_anio);
            SET @id_tiempo = SCOPE_IDENTITY();
        END

        -- G. Procesar dimensiones transaccionales (Generan registros directos mapeando los textos a BIT)
        INSERT INTO dim_socioeconomica (nivel_ingresos, trabaja, tiempo_traslado_min, medio_transporte, conectividad_internet)
        VALUES (
            UPPER(TRIM(@v_nivel_ingresos)), 
            CASE WHEN UPPER(TRIM(@v_trabaja)) = 'SÍ' OR UPPER(TRIM(@v_trabaja)) = 'SI' THEN 1 ELSE 0 END, 
            @v_tiempo_traslado, 
            UPPER(TRIM(@v_medio_transporte)), 
            UPPER(TRIM(@v_conectividad))
        );
        SET @id_socio = SCOPE_IDENTITY();

        INSERT INTO dim_salud (estado_emocional, nivel_estres, apoyo_psicologico)
        VALUES (
            UPPER(TRIM(@v_estado_emocional)), 
            UPPER(TRIM(@v_nivel_estres)), 
            CASE WHEN UPPER(TRIM(@v_apoyo_psicologico)) = 'SÍ' OR UPPER(TRIM(@v_apoyo_psicologico)) = 'SI' THEN 1 ELSE 0 END
        );
        SET @id_salud = SCOPE_IDENTITY();

        -- H. Carga y Consolidación final en la Tabla de Hechos
        INSERT INTO fact_rendimiento (
            id_estudiante, id_carrera, id_socioeconomica, id_salud, id_tiempo, id_curso,
            nota_final_curso, porcentaje_asistencia, deuda_pensiones_soles, horas_lms_virtual, target_desercion
        )
        VALUES (
            @id_estudiante, @id_carrera, @id_socio, @id_salud, @id_tiempo, @id_curso,
            @v_nota, @v_asistencia, @v_deuda, @v_horas_lms, 0
        );

        -- Avanzar a la siguiente fila del staging
        FETCH NEXT FROM cursor_etl INTO 
            @v_dni, @v_codigo, @v_nombre, @v_sexo, @v_edad, @v_estado_civil, @v_colegio,
            @v_distrito, @v_universidad, @v_tipo_uni, @v_cat_pension, @v_carrera, @v_facultad, @v_modalidad,
            @v_nivel_ingresos, @v_trabaja, @v_tiempo_traslado, @v_medio_transporte, @v_conectividad,
            @v_estado_emocional, @v_nivel_estres, @v_apoyo_psicologico, @v_curso, @v_area_ac_curso, @v_filtro_curso, @v_creditos,
            @v_mes, @v_ciclo, @v_anio, @v_nota, @v_asistencia, @v_deuda, @v_horas_lms;
    END;

    -- Liberación completa del cursor para evitar consumo fantasma de RAM
    CLOSE cursor_etl;
    DEALLOCATE cursor_etl;

    -- Vaciar tabla temporal de control tras un ETL exitoso
    TRUNCATE TABLE staging_excel_cursores;
END;
GO