import whisper
import os
import pandas as pd

def audio_a_texto(audio_paths):
    # Cargar el modelo Whisper (puedes elegir entre tiny, base, small, medium, large)
    model = whisper.load_model("small") ## small
    textos = []
    i=0
    for audio_path in audio_paths:
        # Verificar que el archivo de audio existe
        if not os.path.exists(audio_path):
            print(f"El archivo {audio_path} no existe.")
            textos.append("[Archivo no encontrado]")
            continue
        
        try:
            print("working...")
            # Transcribir el archivo de audio usando Whisper
            result = model.transcribe(audio_path, language='es')
            
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
    
    return textos

def juntar_textos(textos):
    texto_completo = "\n".join(textos)
    with open("transcripcion_completa.txt", "w", encoding="utf-8") as file:
        file.write(texto_completo)

directorio="/home/soporte/Documents/YOUTUBE_APP/yo_u_tu_be_app/fragmentos"

audio_paths=sorted(os.listdir(directorio))
print(audio_paths)
file_path_list=[]
for audio_file in audio_paths:
    audio_file_path = os.path.join(directorio, audio_file)
    file_path_list.append(audio_file_path)
textos = audio_a_texto(file_path_list)
# Juntar y guardar los textos
juntar_textos(textos)