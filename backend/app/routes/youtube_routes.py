import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.youtube_service import download_audio, download_video
from fastapi.responses import FileResponse

youtube_router = APIRouter()
DOWNLOAD_FOLDER = "app/downloads/"

# Models for requests
class AudioDownloadRequest(BaseModel):
    url: str
    quality: str  # Allowed qualities: 320kbps, 256kbps, 128kbps

class VideoDownloadRequest(BaseModel):
    url: str


@youtube_router.post("/youtube/download/audio")
async def audio_download(request: AudioDownloadRequest):
    """
    Downloads audio in MP3 format with the specified quality.
    """
    try:
        data = download_audio(request.url, request.quality)
        return {
            "message": "Audio downloaded successfully",
            "file_path": data["file_path"],
            "thumbnail": data["thumbnail"],  # Thumbnail included in the response
            "title": data["title"],  # Video title
        }
    except Exception as e:
        print(f"Error in audio_download route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@youtube_router.post("/youtube/download/video")
async def video_download(request: VideoDownloadRequest):
    """
    Downloads video in MP4 format.
    """
    try:
        data = download_video(request.url)
        return {
            "message": "Video downloaded successfully",
            "file_path": data["file_path"],
            "thumbnail": data["thumbnail"],  # Thumbnail included in the response
            "title": data["title"],  # Video title
        }
    except Exception as e:
        print(f"Error in video_download route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@youtube_router.get("/youtube/download/file")
async def serve_file(file_path: str):
    """
    Serves a file for direct download.
    :param file_path: Relative path to the file to download.
    """
    try:
        # Normalize the file path based on DOWNLOAD_FOLDER
        normalized_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(file_path))

        # Validate that the file exists
        if not os.path.exists(normalized_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Return the file with appropriate headers
        return FileResponse(
            normalized_path,
            media_type="application/octet-stream",
            filename=os.path.basename(normalized_path)  # Forces the correct filename in the download
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
