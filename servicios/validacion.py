import pandas as pd

def validar_archivos_entrada(archivos_subidos):
    dict_validados = {}
    errores = []
    
    # 🚀 OPTIMIZACIÓN: Añadimos 'nombre' y 'completo' para capturar 'nombre_completo' con seguridad
    COLUMNAS_MINIMAS = ['dni', 'alumno', 'nota', 'codigo', 'curso', 'id', 'pension', 'carrera', 'nombre', 'completo']

    for archivo in archivos_subidos:
        try:
            # --- CAPA 1: Lectura según formato ---
            if archivo.name.endswith('.csv'):
                # 🚀 SOLUCIÓN AL SEPARADOR: sep=None y engine='python' detectan automáticamente si usa coma (,) o punto y coma (;)
                df = pd.read_csv(archivo, sep=None, engine='python')
            elif archivo.name.endswith('.json'):
                df = pd.read_json(archivo)
            else:
                df = pd.read_excel(archivo)

            # --- CAPA 2: Validación de Contenido (Negocio) ---
            if df.empty:
                errores.append(f"⚠️ {archivo.name}: El archivo está vacío.")
                continue

            # Convertimos columnas a minúsculas para una validación flexible
            columnas_presentes = [str(c).lower() for c in df.columns]
            
            # 🚀 SOLUCIÓN A LAS CABECERAS COMPUESTAS:
            # Ahora verifica si la palabra clave (ej. 'codigo') está CONTENIDA dentro de alguna columna (ej. 'codigo_universitario')
            es_valido = any(
                any(minima in col for col in columnas_presentes) 
                for minima in COLUMNAS_MINIMAS
            )

            if not es_valido:
                errores.append(f"❌ {archivo.name}: No contiene campos reconocidos del proyecto (DNI, Notas, etc.).")
                continue

            # Si todo está bien, lo guardamos en el diccionario
            dict_validados[archivo.name] = df

        except Exception as e:
            errores.append(f"🔥 {archivo.name}: Error de formato o estructura ({str(e)})")

    return dict_validados, errores