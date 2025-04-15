import os
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.twitter_service import download_twitter_video
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Initialize router
twitter_router = APIRouter()
load_dotenv()
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "/tmp/downloads")

class TwitterDownloadRequest(BaseModel):
    url: str


@twitter_router.post("/twitter/download")
async def twitter_download(request: TwitterDownloadRequest):
    """
    Downloads a Twitter video.
    """
    try:
        # Use the Twitter service to download the video
        data = download_twitter_video(request.url)
        return {
            "message": "Video downloaded successfully",
            "file_path": data["file_path"],
            "thumbnail": data["thumbnail"],
            "title": data["title"],
        }
    except Exception as e:
        print(f"Error in twitter_download route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@twitter_router.get("/twitter/download/file")
async def serve_twitter_file(file_path: str, background_tasks: BackgroundTasks):
    """
    Serves a Twitter file for direct download.
    Deletes the file after the user completes the download.
    """
    try:
        normalized_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(file_path))
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
        print(f"Error in serve_twitter_file route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
