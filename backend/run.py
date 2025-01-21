from app import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":
    # Ejecuta el servidor ASGI usando Uvicorn directamente desde Python
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="debug")
