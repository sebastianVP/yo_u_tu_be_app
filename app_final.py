import yt_dlp
from pydub import AudioSegment
import os
from tqdm import tqdm
import whisper
import pandas as pd
from transformers import pipeline
import streamlit as st


import warnings

warnings.filterwarnings("ignore")


class DownloadProgress:
    def __init__(self):
        self.pbar = None

    def hook(self, d):
        if d['status'] == 'downloading':
            if not self.pbar:
                self.pbar = tqdm(total=float(d['total_bytes']), unit='B', unit_scale=True, desc="Descargando")
            self.pbar.update(d['downloaded_bytes'] - self.pbar.n)
        elif d['status'] == 'finished':
            if self.pbar:
                self.pbar.close()
                print("\n¡Descarga completada!")



def convertYOUTUBE_MP3(link_url,preferredcodec,base_dir,folder_name,output_filename):
    """
    link_url       : Link de video youtube
    preferredcodec : mp3,m4a
    base_dir       : Directorio base donde se creará la carpeta
    folder_name    : Nombre de la carpeta dentro del directorio base
    output_filename: Nombre del archivo de salida
    """
    # Crear la carpeta dentro del directorio base
    output_dir = os.path.join(base_dir,folder_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Carpeta creada: {output_dir}")
    else:
        print(f"Carpeta ya existenten: {output_dir}")

    output_ext = preferredcodec.lower()  # Convertir a minúsculas por consistencia
    output_path = os.path.join(output_dir,f"{output_filename}.{output_ext}")
    #output_path = os.path.join(output_dir, f"{output_filename}.%(ext)s")


    URLS=[link_url]
    progress = DownloadProgress()


    ydl_opts= {
        "format"        : "m4a/bestaudio/best",
        "postprocessors" : [{
                            "key"            : "FFmpegExtractAudio",
                            "preferredcodec" : "mp3",
                            #"preferredquality": "192",  # Ajusta la calidad según lo necesario

        }],
        "outtmpl":os.path.join(output_dir, f"{output_filename}.%(ext)s"),
        "progress_hooks": [progress.hook],  # Añadir la barra de progreso

    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)

    return output_path

def convertAUDIO_fragmento(audio_file_path, fragmento):
    try:
        audio = AudioSegment.from_mp3(audio_file_path)
    except:
        print("Error de conversion")
    #Duraciontotal de audio en milisegundos
    audio_duration_ms = len(audio)
    print(f"Duración total del audio: {audio_duration_ms / 1000} segundos")
    # Número de fragmentos
    num_parts = fragmento
    # Duración de cada fragmento
    fragment_duration_ms = audio_duration_ms // num_parts

    dirname   = os.path.dirname(audio_file_path)
    output_frag = os.path.join(dirname,"fragmentos")
    if not os.path.exists(output_frag):
        os.makedirs(output_frag)
        print(f"Carpeta creada: {output_frag}")
    else:
        print(f"Carpeta ya existenten: {output_frag}")

    # Dividir en fragmentos
    fragment_list=[]
    for i in range(num_parts):
        start_ms = i * fragment_duration_ms
        end_ms = (i + 1) * fragment_duration_ms if (i + 1) < num_parts else audio_duration_ms
        
        # Crear el fragmento
        fragment = audio[start_ms:end_ms]
        
        # Nombre del archivo para el fragmento
        fragment_name = f"{output_frag}/fragmento_{i + 1}.mp3"
        fragment.export(fragment_name, format="mp3")
        print(f"Fragmento {i + 1} guardado como {fragment_name}")
        fragment_list.append(fragment_name)
    return fragment_list
    
def audio_a_texto(audio_paths):
    # Cargar el modelo Whisper (PODEMOS  ELEGIR entre tiny, base, small, medium, large)
    model = whisper.load_model("small") ## small
    textos = []
    i=0
     # Inicializar tqdm para mostrar el progreso
    with tqdm(total=len(audio_paths), desc="Procesando audios", unit="archivo") as pbar:
        for audio_path in audio_paths:
            # Verificar que el archivo de audio existe
            if not os.path.exists(audio_path):
                print(f"El archivo {audio_path} no existe.")
                textos.append("[Archivo no encontrado]")
                pbar.update(1)
                continue
            
            try:
                print("working...")
                # Transcribir el archivo de audio usando Whisper
                result = model.transcribe(audio_path, language='en') # es: español , en:english
                
                # Verificar que la transcripción no sea None
                if result and "text" in result:
                    textos.append(result["text"])
                    #-----new--------------------
                    segments= result["segments"]
                    df_segments = pd.DataFrame(segments, columns=['id', 'start', 'end', 'text'])
                    df_segments.to_csv(f"segments_{i}",index=False)
                    #-------------------------------
                    print("Texto--->",i)
                    i=i+1
                else:
                    textos.append("[Transcripción fallida]")
            
            except Exception as e:
                print(f"Error al transcribir el archivo {audio_path}: {e}")
                textos.append(f"[Error: {e}]")
            
            # Actualizar la barra de progreso
            pbar.update(1)
    
    return textos

def juntar_textos(output_path,filename,textos):
    dirname   = os.path.dirname(output_path)
    output_transcrip= os.path.join(dirname,"transcripcion")

    if not os.path.exists(output_transcrip):
        os.makedirs(output_transcrip)
        print(f"Carpeta creada: {output_transcrip}")
    else:
        print(f"Carpeta ya existenten: {output_transcrip}")
    filename_path=f"{output_transcrip}/{filename}.txt"
    texto_completo = "\n".join(textos)
    with open(filename_path, "w", encoding="utf-8") as file:
        file.write(texto_completo)
    return filename_path


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
def procesar_archivo(file_path,filename):
    try:
        with open(file_path, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        
        print("Generando resumen...")
        resumen = agente_resumen(contenido)
        
        print("\nResumen en español:")
        print(resumen)
        dirname       = os.path.dirname(file_path)
        filename_path = f"{dirname}/{filename}_esp.txt"
        with open(filename_path, "w", encoding="utf-8") as file:
            file.write(resumen)

        
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

# Atributos
# Streamlit UI
st.title("Descargador y Procesador de Videos de YouTube")

link_url = st.text_input("Enlace de YouTube:")
preferredcodec = st.selectbox("Formato de audio", ["mp3", "m4a"])
base_dir = st.text_input("Directorio base:", "./downloads")
folder_name = st.text_input("Nombre de la carpeta:", "output")
output_filename = st.text_input("Nombre del archivo de salida:", "audio")
fragment_count = st.number_input("Número de fragmentos para dividir el audio:", min_value=1, step=1, value=5)

if st.button("Iniciar Proceso"):
    if link_url and base_dir and folder_name and output_filename:
        st.write("Iniciando descarga...")
        try:
            output_path = convertYOUTUBE_MP3(link_url, preferredcodec, base_dir, folder_name, output_filename)
            st.write(f"Audio descargado: {output_path}")

            st.write("Dividiendo el audio en fragmentos...")
            fragment_list = convertAUDIO_fragmento(output_path, fragment_count)
            st.write(f"Fragmentos creados: {len(fragment_list)}")

            st.write("Transcribiendo fragmentos de audio...")
            textos = audio_a_texto(fragment_list)

            st.write("Generando archivo de transcripción...")
            transcript_path = juntar_textos(output_path, output_filename, textos)
            st.write(f"Archivo de transcripción generado: {transcript_path}")

            st.success("¡Proceso completado exitosamente!")
        except Exception as e:
            st.error(f"Error durante el proceso: {e}")
    else:
        st.warning("Por favor, completa todos los campos antes de continuar.")

    """
    streamlit run app_final.py
    """