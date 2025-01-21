import os
from fastapi import APIRouter, HTTPException
from app.services.tiktok_service import download_tiktok_video
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Initialize router
tiktok_router = APIRouter()
DOWNLOAD_FOLDER = "app/downloads/"  # TikTok-specific download folder


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
async def serve_tiktok_file(file_path: str):
    """
    Serves a TikTok file for direct download.
    :param file_path: Relative path to the file to download.
    """
    try:
        # Normalize the file path to ensure it points to the TikTok download directory
        normalized_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(file_path))

        # Check if the file exists
        if not os.path.exists(normalized_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Return the file for download
        return FileResponse(
            normalized_path,
            media_type="video/mp4",  # Adjust media type if needed
            filename=os.path.basename(normalized_path),  # Force the filename in the download
        )
    except Exception as e:
        print(f"Error in serve_tiktok_file route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
