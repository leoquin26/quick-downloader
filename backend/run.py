from app import create_app
import uvicorn
from fastapi.staticfiles import StaticFiles
import os

app = create_app()

# Asegúrate de que la carpeta de descargas exista
# os.makedirs("app/downloads", exist_ok=True)

# Monta la carpeta `downloads` como un directorio estático
# app.mount("/downloads", StaticFiles(directory="app/downloads"), name="downloads")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=5000)
