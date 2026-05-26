from supabase import create_client, Client

# Configuración con el estándar moderno por API
SUPABASE_URL = "https://jxpgxlchprnqxfbhlkcm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp4cGd4bGNocHJucXhmYmhsa2NtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk2Njg4NjIsImV4cCI6MjA5NTI0NDg2Mn0.sYdn-MbFQY2X9tK-1XBz31XPifrnlux2-cpEeMYhaxE"

def obtenerConexion():
    try:
        # Inicializamos el cliente oficial de Supabase
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ ¡Cliente de Supabase conectado con éxito mediante la API!")
        return supabase
    except Exception as e:
        print(f"❌ Error al inicializar el cliente de Supabase: {e}")
        return None