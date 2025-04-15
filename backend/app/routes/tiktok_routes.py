import os
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.tiktok_service import download_tiktok_video
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Initialize router
tiktok_router = APIRouter()

# Load environment variables
load_dotenv()
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "app/downloads/")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
# import tempfile
# DOWNLOAD_FOLDER = tempfile.gettempdir()

# Models for TikTok requests
class TikTokDownloadRequest(BaseModel):
    url: str


@tiktok_router.post("/tiktok/download")
async def tiktok_download(request: TikTokDownloadRequest):
    """
    Downloads a TikTok video.
    """
    try:
        # Use the TikTok service to download the video
        data = download_tiktok_video(request.url)
        return {
            "message": "Video downloaded successfully",
            "file_path": data["file_path"],
            "thumbnail": data["thumbnail"],  # Thumbnail URL
            "title": data["title"],  # Title of the video
        }
    except Exception as e:
        print(f"Error in tiktok_download route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@tiktok_router.get("/tiktok/download/file")
async def serve_tiktok_file(file_path: str, background_tasks: BackgroundTasks):
    """
    Serves a TikTok file for direct download.
    Deletes the file after the user completes the download.
    :param file_path: Relative path to the file to download.
    :param background_tasks: BackgroundTasks for handling cleanup.
    """
    try:
        # Normalize the file path
        normalized_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(file_path))

        # Validate that the file exists
        if not os.path.exists(normalized_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Schedule file deletion after the response is completed
        background_tasks.add_task(os.remove, normalized_path)

        # Serve the file
        return FileResponse(
            path=normalized_path,
            media_type="video/mp4",  # Adjust media type if needed
            filename=os.path.basename(normalized_path),  # Force the filename in the download
        )
    except Exception as e:
        print(f"Error in serve_tiktok_file route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
