import sqlite3
import os

# Definimos las rutas claramente
STAGING_DB_PATH = 'data/staging/staging.db'
DW_DB_PATH = 'data/dw/dw.db'

def guardar_en_staging(diccionario_dfs):
    try:
        # Asegurar que la carpeta 'data/staging' existe
        os.makedirs(os.path.dirname(STAGING_DB_PATH), exist_ok=True)
        
        conn = sqlite3.connect(STAGING_DB_PATH)
        
        for nombre, df in diccionario_dfs.items():
            # Limpiar nombre para tabla SQL
            nombre_tabla = f"raw_{nombre.replace('.', '_').replace(' ', '_')}"
            
            # Guardamos en la base de datos de STAGING
            df.to_sql(nombre_tabla, conn, if_exists='replace', index=False)
            
        conn.close()
        return True, "Tablas crudas guardadas en data/staging/mira_staging.db"
    except Exception as e:
        return False, f"Error en Staging: {str(e)}"