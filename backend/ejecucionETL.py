import os
from conexionBD import obtenerConexion

def ejecutarScriptSQL(nombreArchivo, parametros=None):
    """Lee un archivo .sql de la carpeta bd/ y lo ejecuta en el servidor"""
    # Construir la ruta dinámica hacia la carpeta 'bd'
    ruta_script = os.path.join(os.path.dirname(__file__), '..', 'bd', nombreArchivo)
    
    if not os.path.exists(ruta_script):
        print(f"⚠️ El archivo {nombreArchivo} no existe en la carpeta bd/")
        return False
        
    with open(ruta_script, 'r', encoding='utf-8') as archivo:
        sql_script = archivo.read()
        
    # Reemplazar parámetros dinámicos si se necesitan (como el ciclo activo en KPIs)
    if parametros:
        for clave, valor in parametros.items():
            sql_script = sql_script.replace(f"{{{{{clave}}}}}", str(valor))
            
    conexion = obtenerConexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            # SQL Server no permite GO dentro de scripts ejecutados por ODBC, lo separamos por bloques
            bloques = sql_script.split('GO')
            for bloque in bloques:
                if bloque.strip():
                    cursor.execute(bloque)
            conexion.commit()
            cursor.close()
            conexion.close()
            print(f"🚀 {nombreArchivo} ejecutado con éxito.")
            return True
        except Exception as e:
            print(f"❌ Error al ejecutar {nombreArchivo}: {e}")
            return False
    return False

# Funciones listas para ser invocadas por tus interfaces visuales
def inicializarDataWarehouse():
    return ejecutarScriptSQL('crearDataWarehouse.sql')

def cargarEtlCursores():
    return ejecutarScriptSQL('cursoresETL.sql')

def cargarEtlConjuntos():
    return ejecutarScriptSQL('limpiezaAlternativa.sql')

def procesarCapaSemanticaKpis(ciclo):
    return ejecutarScriptSQL('calculoKpis.sql', {'CICLO_ACTIVO': ciclo})