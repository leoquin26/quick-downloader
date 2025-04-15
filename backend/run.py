# run.py
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from app import create_app

# ⚠️ IMPORTANTE: Cargar antes del getenv
load_dotenv()

# ✅ Lee la ruta del .env o usa /tmp como fallback en Vercel
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "/tmp/downloads")

# ✅ Evita rutas de solo lectura
if not DOWNLOAD_FOLDER.startswith("/var/task"):
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

app = create_app()
app.mount("/downloads", StaticFiles(directory=DOWNLOAD_FOLDER), name="downloads")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
