from pydub import AudioSegment
import os

# Cargar el archivo de audio
audio = AudioSegment.from_mp3("AUDIO.mp3")

# Duración total del audio en milisegundos
audio_duration_ms = len(audio)
print(f"Duración total del audio: {audio_duration_ms / 1000} segundos")

# Número de fragmentos
num_parts = 5

# Duración de cada fragmento
fragment_duration_ms = audio_duration_ms // num_parts
# Crear una carpeta llamada "fragmentos" si no existe
output_folder = "fragmentos"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Carpeta '{output_folder}' creada.")

# Dividir en fragmentos
for i in range(num_parts):
    start_ms = i * fragment_duration_ms
    end_ms = (i + 1) * fragment_duration_ms if (i + 1) < num_parts else audio_duration_ms
    
    # Crear el fragmento
    fragment = audio[start_ms:end_ms]
    
    # Nombre del archivo para el fragmento
    fragment_name = f"{output_folder}/fragmento_{i + 1}.mp3"
    fragment.export(fragment_name, format="mp3")
    print(f"Fragmento {i + 1} guardado como {fragment_name}")