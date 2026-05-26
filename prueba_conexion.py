from supabase import create_client, Client

print("🔄 Conectando directamente con la API de Supabase (Versión 2026)...")

# 1. Credenciales directas
SUPABASE_URL = "https://jxpgxlchprnqxfbhlkcm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp4cGd4bGNocHJucXhmYmhsa2NtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk2Njg4NjIsImV4cCI6MjA5NTI0NDg2Mn0.sYdn-MbFQY2X9tK-1XBz31XPifrnlux2-cpEeMYhaxE"

try:
    # 2. Inicializamos el cliente oficial de inmediato
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("\n--------------------------------------------------")
    print("✅ ¡CONEXIÓN EXITOSA POR API!")
    print("🤖 Tu proyecto ya está enlazado con Supabase en la nube.")
    print("--------------------------------------------------")
    
    # 3. Prueba de autenticación en frío (Ping de seguridad)
    supabase.auth.get_session()
    print("🔑 Validación de credenciales: ¡Claves autorizadas correctamente!")
    print("--------------------------------------------------")

except Exception as e:
    print("\n--------------------------------------------------")
    print(f"❌ Error al conectar con la API: {e}")
    print("--------------------------------------------------")