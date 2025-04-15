FROM python:3.10-slim

# Instala dependencias del sistema y herramientas necesarias
RUN apt-get update && apt-get install -y \
    ffmpeg libnss3 \
    && rm -rf /var/lib/apt/lists/* \
    && ffmpeg -version  # Verifica que ffmpeg se haya instalado correctamente

WORKDIR /app

# Instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install -U --pre "yt-dlp[default]"

# Copia el resto del código del backend
COPY . .

# Crea la carpeta downloads
RUN mkdir -p app/downloads

# Copia y da permisos al script de inicio
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 5000

# Inicia con el script
CMD ["./start.sh"]