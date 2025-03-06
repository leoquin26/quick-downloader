FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg libnss3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Crea la carpeta downloads si no existe (para evitar errores al montar)
RUN mkdir -p app/downloads

EXPOSE 5000

CMD ["uvicorn", "app.__init__:create_app", "--host", "0.0.0.0", "--port", "5000"]