import os
from dotenv import load_dotenv
from app import create_app
import uvicorn
from fastapi.staticfiles import StaticFiles

# Cargar variables de entorno desde .env
load_dotenv()

app = create_app()

# Obtener la ruta de descarga desde el entorno (por defecto: /tmp/downloads)
downloads_dir = os.getenv("DOWNLOAD_FOLDER", "/tmp/downloads")

# Asegúrate de que la carpeta de descargas exista
os.makedirs(downloads_dir, exist_ok=True)

# Monta la carpeta como un directorio estático
app.mount("/downloads", StaticFiles(directory=downloads_dir), name="downloads")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
