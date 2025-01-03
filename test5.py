import os
from transformers import pipeline

# Desactivar paralelismo en tokenizers
#os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Función de traducción
def traducir_a_espanol(texto):
    try:
        traduccion = pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es")
        
        # Dividir texto en bloques si es muy largo
        max_input_length = 400  # Límite recomendado para este modelo
        bloques = [texto[i:i + max_input_length] for i in range(0, len(texto), max_input_length)]
        
        traducciones = []
        for bloque in bloques:
            resultados = traduccion(bloque, max_length=400)
            if resultados and len(resultados) > 0:
                traducciones.append(resultados[0]['translation_text'])
        
        return " ".join(traducciones)
    except Exception as e:
        return f"Error en la traducción: {e}"

# Función de resumen mejorada
def agente_resumen(texto):
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Unificar texto en una sola línea
        texto_unificado = " ".join(texto.splitlines())
        
        # Dividir en bloques si es muy largo
        max_input_length = 800#1024  # Longitud máxima soportada por BART
        bloques = [texto_unificado[i:i + max_input_length] for i in range(0, len(texto_unificado), max_input_length)]
        print("Longitud de bloques:", len(bloques))
        # Generar resumen para cada bloque
        resúmenes = []
        for bloque in bloques:
            resumen = summarizer(bloque, max_length=130, min_length=30, do_sample=False)
            if resumen and len(resumen) > 0:
                resúmenes.append(resumen[0]['summary_text'])
        
        # Unir resúmenes y traducir
        resumen_completo = " ".join(resúmenes)
        resumen_espanol = traducir_a_espanol(resumen_completo)
        return resumen_espanol
    except Exception as e:
        return f"Error en el resumen: {e}"

# Leer un archivo de texto y generar resúmenes
def procesar_archivo(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read().strip()
        
        if not contenido:
            print("El archivo está vacío o no tiene texto válido.")
            return
        
        print("Generando resumen...")
        resumen = agente_resumen(contenido)
        
        print("\nResumen en español:")
        print(resumen)
        
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

# Ruta al archivo de texto
ruta_archivo = "/home/soporte/Documents/YOUTUBE_APP/yo_u_tu_be_app/Descargas/transcripcion/Adaboost.txt"  # Cambiar por la ruta real del archivo
procesar_archivo(ruta_archivo)