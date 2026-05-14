import pandas as pd

def validar_archivos_entrada(archivos_subidos):
    dict_validados = {}
    errores = []
    
    # Columnas que esperamos encontrar (en minúsculas para comparar)
    # Si es JSON, al menos debe tener alguna de estas llaves
    COLUMNAS_MINIMAS = ['dni', 'alumno', 'nota', 'codigo', 'curso', 'id', 'pension','carrera']

    for archivo in archivos_subidos:
        try:
            # --- CAPA 1: Lectura según formato ---
            if archivo.name.endswith('.csv'):
                df = pd.read_csv(archivo)
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
            
            # Verificamos si hay intersección entre lo que subió y lo que necesitamos
            es_valido = any(col in columnas_presentes for col in COLUMNAS_MINIMAS)

            if not es_valido:
                errores.append(f"❌ {archivo.name}: No contiene campos reconocidos del proyecto (DNI, Notas, etc.).")
                continue

            # Si todo está bien, lo guardamos en el diccionario
            dict_validados[archivo.name] = df

        except Exception as e:
            errores.append(f"🔥 {archivo.name}: Error de formato o estructura ({str(e)})")

    return dict_validados, errores