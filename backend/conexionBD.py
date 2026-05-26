import pyodbc

def obtenerConexion():
    try:
        # Cadena de conexión estándar para SQL Server (Autenticación Windows)
        # Nota: Cambia 'LOCALHOST' o '.' según el nombre de tu instancia de SQL Server
        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=LOCALHOST;"
            "DATABASE=DW_Rendimiento_Academico;"
            "Trusted_Connection=yes;"
        )
        conexion = pyodbc.connect(connection_string)
        return conexion
    except Exception as e:
        print(f"❌ Error al conectar a SQL Server: {e}")
        return None