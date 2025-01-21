from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.youtube_routes import youtube_router
from app.routes.tiktok_routes import tiktok_router
from app.routes.instagram_routes import instagram_router 
def create_app() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI.
    """
    app = FastAPI(title="Video Downloader API", version="1.0")

    # Config CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes registered
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
