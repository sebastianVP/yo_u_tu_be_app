**YOUTUBE-SCRIPT-APP**
---


Este repositorio contiene el script para descargar videos de youtube. En el S.O. Ubuntu 22.04
Primera prueba:
- Utilizando la libreria pytube: Despues de varios intentos, optamos por utilizar otra libreria porque genera errores
- La libreria utilizada es yt-dlp
- Tenemos tambien que instalar el paquete ffmpeg
- Solo descargamos el audio formato mp3 y m4a.
- Link de info : https://github.com/yt-dlp/yt-dlp#readme
- Instalamos tambien la libreria moviepy
- pip install moviepy SpeechRecognition pydub
- Reconocimiento de voz(pip install git+https://github.com/openai/whisper.git)
Comandos necesarios:

- sudo apt install ffmpeg
- pip install yt-dlp

**OBJETIVO**
---

Implementar un agente para descargar videos, resumir su contenido y traducirlo,  esto debe dar como resultado una aplicación o herramienta basada en inteligencia artificial que automatice las siguientes tareas:

Funcionalidades del Agente

1. Descargar videos:

* Utilizar bibliotecas o servicios para descargar videos de plataformas como YouTube o Vimeo.
* Soportar distintos formatos y resoluciones.

2. Transcribir el contenido:

* Extraer el audio del video.
* Utilizar APIs de reconocimiento de voz como Whisper de OpenAI o Google Speech-to-Text para transcribir el audio.

4. Generar resúmenes:

* Procesar la transcripción usando modelos de procesamiento de lenguaje natural (NLP) como BERT, GPT o T5 para generar resúmenes.

5. Traducir el contenido:

* Usar servicios como Google Translate API o DeepL API para traducir la transcripción o el resumen a otros idiomas.

**Ejemplo de Flujo del Agente**
--- 

1. Input del usuario:

* URL del video.
* Idioma de salida para la traducción.
* Nivel de detalle del resumen (breve o detallado).

2. Procesamiento:

* Descargar el video.
* Extraer el audio y generar la transcripción.
* Generar el resumen del contenido.
* Traducir el resumen al idioma seleccionado.

3. Output:

* Texto transcrito y traducido.
* Resumen del video en el idioma elegido.

**PUESTA EN PRODUCCION**

* Crear los archivos:
    * Procfile
    * setup.sh
    * requirements.txt


**EJECUCION**
--- 

* streamlit run app_transcripcion.py

![EJECUCION1](/IMAGENES/3_FINAL.PNG)
![EJECUCION2](/IMAGENES/4_FINAL.PNG)


