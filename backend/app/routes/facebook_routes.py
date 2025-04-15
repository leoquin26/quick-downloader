import os
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.facebook_service import download_facebook_video
from dotenv import load_dotenv

# Initialize router
facebook_router = APIRouter()

# Load environment variables
load_dotenv()
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "/tmp/downloads")

# Models for Facebook requests
class FacebookDownloadRequest(BaseModel):
    url: str


@facebook_router.post("/facebook/download")
async def facebook_download(request: FacebookDownloadRequest):
    """
    Downloads a Facebook video.
    """
    try:
        # Use the Facebook service to download the video
        data = download_facebook_video(request.url)
        return {
            "message": "Video downloaded successfully",
            "file_path": data["file_path"],
            "thumbnail": data["thumbnail"],  # Thumbnail URL
            "title": data["title"],  # Title of the video
        }
    except Exception as e:
        print(f"Error in facebook_download route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@facebook_router.get("/facebook/download/file")
async def serve_facebook_file(file_path: str, background_tasks: BackgroundTasks):
    """
    Serves a Facebook file for direct download.
    Deletes the file after the user completes the download.
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
            media_type="video/mp4",
            filename=os.path.basename(normalized_path),
        )
    except Exception as e:
        print(f"Error in serve_facebook_file route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
