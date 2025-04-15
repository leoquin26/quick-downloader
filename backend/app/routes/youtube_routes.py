import os
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.services.youtube_service import download_audio, download_video
from fastapi.responses import FileResponse

youtube_router = APIRouter()
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Obtener carpeta de descargas desde el entorno (fallback a /tmp/downloads para Vercel)
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "/tmp/downloads")

class AudioDownloadRequest(BaseModel):
    url: str
    quality: str


class VideoDownloadRequest(BaseModel):
    url: str

@youtube_router.post("/youtube/download/audio")
async def audio_download(request: AudioDownloadRequest):
    try:
        data = download_audio(request.url, request.quality)
        return {
            "message": "Audio downloaded successfully",
            "file_path": data["file_path"],
            "thumbnail": data["thumbnail"],
            "title": data["title"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@youtube_router.post("/youtube/download/video")
async def video_download(request: VideoDownloadRequest):
    try:
        data = download_video(request.url)
        return {
            "message": "Video downloaded successfully",
            "file_path": data["file_path"],
            "thumbnail": data["thumbnail"],
            "title": data["title"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@youtube_router.get("/youtube/download/file")
async def serve_file(file_path: str, background_tasks: BackgroundTasks):
    try:
        normalized_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(file_path))
        if not os.path.exists(normalized_path):
            raise HTTPException(status_code=404, detail="File not found")

        background_tasks.add_task(os.remove, normalized_path)

        return FileResponse(
            normalized_path,
            media_type="application/octet-stream",
            filename=os.path.basename(normalized_path),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
