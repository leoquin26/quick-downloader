import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.youtube_routes import youtube_router
from app.routes.tiktok_routes import tiktok_router
from app.routes.instagram_routes import instagram_router 
from app.routes.soundcloud_routes import soundcloud_router
from app.routes.rating_routes import rating_router
from app.routes.cookies_routes import cookies_router
from app.routes.twitter_routes import twitter_router
from app.routes.facebook_routes import facebook_router

def create_app() -> FastAPI:
    """
    Crea y configura la aplicación FastAPI.
    """
    app = FastAPI(title="Video Downloader API", version="1.0")

    # Config CORS
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost", "http://localhost:3000,https://quick-downloader-frontend.vercel.app", "https://youtubedownloader-frontend-restless-star-9831.fly.dev").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes registered
    app.include_router(youtube_router)
    app.include_router(tiktok_router)
    app.include_router(instagram_router)
    app.include_router(soundcloud_router)
    app.include_router(facebook_router)
    app.include_router(twitter_router, prefix="/api", tags=["Twitter"])
    app.include_router(rating_router, prefix="/api", tags=["Ratings"])
    app.include_router(cookies_router, prefix="/api", tags=["Cookies"])

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