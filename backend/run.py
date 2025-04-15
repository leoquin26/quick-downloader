# run.py
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from app import create_app

# Carga las variables de entorno
load_dotenv()

# Directorio para archivos de descarga
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "/tmp/downloads")

# Solo crear si es un path válido de escritura
if not DOWNLOAD_FOLDER.startswith("/var/task"):
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Instancia global requerida por Vercel
app = create_app()
app.mount("/downloads", StaticFiles(directory=DOWNLOAD_FOLDER), name="downloads")
