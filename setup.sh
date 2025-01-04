#!/bin/bash

# Instalar FFmpeg si no esta presente
if ! command -v ffmpeg &> /dev/null; then
    echo "FFmpeg no está instalado. Instalándolo ahora..."
    sudo apt update
    sudo apt install -y ffmpeg
else
    echo "FFmpeg ya está instalado."
fi

# Crear configuración para Streamlit
mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml