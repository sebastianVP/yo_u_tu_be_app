import os
from pydub import AudioSegment

# Función para aumentar el volumen de todos los archivos MP3 en una carpeta
def aumentar_volumen_directorio(directorio, incremento_db=10):
    # Recorrer todos los archivos en el directorio
    for archivo in os.listdir(directorio):
        if archivo.endswith(".mp3"):
            ruta_archivo = os.path.join(directorio, archivo)
            
            # Cargar el archivo MP3
            audio = AudioSegment.from_mp3(ruta_archivo)
            
            # Aumentar el volumen
            audio_aumentado = audio + incremento_db
            
            # Sobrescribir el archivo con el volumen aumentado
            audio_aumentado.export(ruta_archivo, format="mp3")
            
            print(f"Volumen aumentado para: {archivo}")


# Ejemplo de uso
directorio = "/home/soporte/Documents/YOUTUBE_APP/yo_u_tu_be_app/fragmentos"
#directorio = r"C:\Users\soporte\Downloads\sesion9\audios"
aumentar_volumen_directorio(directorio, incremento_db=16)