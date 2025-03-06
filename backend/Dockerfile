FROM python:3.10-slim

# Instala dependencias para Python y Node.js
RUN apt-get update && apt-get install -y \
    ffmpeg libnss3 \
    nodejs npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Clona y configura el proveedor HTTP Server
RUN git clone --single-branch --branch 0.7.4 https://github.com/Brainicism/bgutil-ytdlp-pot-provider.git /app/bgutil-provider
WORKDIR /app/bgutil-provider/server
RUN yarn install --frozen-lockfile && npx tsc

# Copia el resto del código del backend
WORKDIR /app
COPY . .

# Crea la carpeta downloads
RUN mkdir -p app/downloads

EXPOSE 5000
EXPOSE 4416

# Inicia el proveedor y el backend
CMD ["sh", "-c", "node /app/bgutil-provider/server/build/main.js & uvicorn app.__init__:app --host 0.0.0.0 --port 5000"]