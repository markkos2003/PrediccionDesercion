USE master;
GO

IF EXISTS (SELECT name FROM sys.databases WHERE name = N'DW_Rendimiento_Academico')
BEGIN
    ALTER DATABASE DW_Rendimiento_Academico SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE DW_Rendimiento_Academico;
END
GO

CREATE DATABASE DW_Rendimiento_Academico;
GO

USE DW_Rendimiento_Academico;
GO

-- 1. SUB-DIMENSIONES (Copo de Nieve)
CREATE TABLE dim_distrito (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    zona_lima VARCHAR(30) NOT NULL,
    indice_inseguridad VARCHAR(15) NOT NULL
);

CREATE TABLE dim_universidad (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    tipo VARCHAR(15) NOT NULL,
    distrito_sede VARCHAR(50) NOT NULL,
    anios_licencia INT NOT NULL,
    categoria_pension VARCHAR(15) NOT NULL
);

-- 2. DIMENSIONES INDEPENDIENTES
CREATE TABLE dim_socioeconomica (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nivel_ingresos VARCHAR(20) NOT NULL,
    trabaja BIT NOT NULL,
    tiempo_traslado_min INT NOT NULL,
    medio_transporte VARCHAR(30) NOT NULL,
    conectividad_internet VARCHAR(20) NOT NULL
);

CREATE TABLE dim_salud (
    id INT IDENTITY(1,1) PRIMARY KEY,
    estado_emocional VARCHAR(30) NOT NULL,
    nivel_estres VARCHAR(15) NOT NULL,
    apoyo_psicologico BIT NOT NULL
);

CREATE TABLE dim_curso (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_curso VARCHAR(50) NOT NULL,
    area_academica VARCHAR(40) NOT NULL,
    curso_filtro BIT NOT NULL,
    creditos DECIMAL(4,1) NOT NULL
);

CREATE TABLE dim_tiempo (
    id INT IDENTITY(1,1) PRIMARY KEY,
    mes VARCHAR(15) NOT NULL,
    ciclo_academico VARCHAR(15) NOT NULL,
    anio INT NOT NULL
);

-- 3. DIMENSIONES PADRE
CREATE TABLE dim_estudiante (
    id INT IDENTITY(1,1) PRIMARY KEY,
    dni VARCHAR(8) NOT NULL UNIQUE,
    codigo_universitario VARCHAR(15) NOT NULL UNIQUE,
    nombre_completo VARCHAR(100) NOT NULL,
    sexo VARCHAR(1) NOT NULL,
    edad INT NOT NULL,
    estado_civil VARCHAR(20) NOT NULL,
    id_distrito INT NOT NULL,
    colegio_procedencia VARCHAR(30) NOT NULL,
    FOREIGN KEY (id_distrito) REFERENCES dim_distrito(id)
);

CREATE TABLE dim_carrera (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_carrera VARCHAR(50) NOT NULL,
    facultad VARCHAR(50) NOT NULL,
    id_universidad INT NOT NULL,
    modalidad VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_universidad) REFERENCES dim_universidad(id)
);

-- 4. TABLA DE HECHOS
CREATE TABLE fact_rendimiento (
    id_fact INT IDENTITY(1,1) PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_carrera INT NOT NULL,
    id_socioeconomica INT NOT NULL,
    id_salud INT NOT NULL,
    id_tiempo INT NOT NULL,
    id_curso INT NOT NULL,
    nota_final_curso DECIMAL(4,2) NOT NULL,
    porcentaje_asistencia INT NOT NULL,
    deuda_pensiones_soles DECIMAL(10,2) NOT NULL,
    horas_lms_virtual INT NOT NULL,
    target_desercion INT NOT NULL DEFAULT 0,
    FOREIGN KEY (id_estudiante) REFERENCES dim_estudiante(id),
    FOREIGN KEY (id_carrera) REFERENCES dim_carrera(id),
    FOREIGN KEY (id_socioeconomica) REFERENCES dim_socioeconomica(id),
    FOREIGN KEY (id_salud) REFERENCES dim_salud(id),
    FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id),
    FOREIGN KEY (id_curso) REFERENCES dim_curso(id)
);

-- 5. TABLA ANALÍTICA DE KPIS CENTRALIZADOS (Lab 7)
CREATE TABLE FactKPIs (
    id_kpi INT IDENTITY(1,1) PRIMARY KEY,
    id_tiempo INT NOT NULL,
    nombre_kpi VARCHAR(100) NOT NULL,
    valor_calculado DECIMAL(5,2) NOT NULL,
    meta_negocio DECIMAL(5,2) NOT NULL,
    fecha_calculo DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id)
);
GO
PRINT 'Script 01: Estructura Copo de Nieve creada exitosamente.';