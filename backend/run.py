import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from app import create_app

load_dotenv()

app = create_app()

DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "/tmp/downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)  # Solo aquí

app.mount("/downloads", StaticFiles(directory=DOWNLOAD_FOLDER), name="downloads")
