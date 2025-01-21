from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.youtube_routes import youtube_router
from app.routes.tiktok_routes import tiktok_router  # Import the TikTok router
from app.routes.instagram_routes import instagram_router 
def create_app() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI.
    """
    app = FastAPI(title="Video Downloader API", version="1.0")

    # Configuración de CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # Permite el frontend en desarrollo
        allow_credentials=True,
        allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc.)
        allow_headers=["*"],  # Permite todas las cabeceras
    )

    # Registrar rutas
    app.include_router(youtube_router)
    app.include_router(tiktok_router)
    app.include_router(instagram_router)

    @app.get("/")
    def home():
        return {"message": "Video Downloader API is running"}

    @app.get("/health", tags=["Health"])
    def health_check():
        """
        Ruta para verificar que el servicio está funcionando correctamente.
        """
        return {"status": "ok", "message": "Service is up and running"}

    return app
