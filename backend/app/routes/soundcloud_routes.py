import os
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.soundcloud_service import download_soundcloud_track
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "app/downloads/")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Initialize router
soundcloud_router = APIRouter()

# Models for SoundCloud requests
class SoundCloudDownloadRequest(BaseModel):
    url: str


@soundcloud_router.post("/soundcloud/download")
async def soundcloud_download(request: SoundCloudDownloadRequest):
    """
    Downloads a SoundCloud track.
    """
    try:
        # Use the SoundCloud service to download the track
        data = download_soundcloud_track(request.url)
        return {
            "message": "Track downloaded successfully",
            "file_path": data["file_path"],
            "thumbnail": data["thumbnail"],  # Thumbnail URL
            "title": data["title"],  # Title of the track
        }
    except Exception as e:
        print(f"Error in soundcloud_download route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@soundcloud_router.get("/soundcloud/download/file")
async def serve_soundcloud_file(file_path: str, background_tasks: BackgroundTasks):
    """
    Serves a SoundCloud file for direct download.
    Deletes the file and its associated thumbnail after the user completes the download.
    :param file_path: Relative path to the file to download.
    :param background_tasks: BackgroundTasks for handling cleanup.
    """
    try:
        # Normalize the file path
        normalized_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(file_path))
        thumbnail_path = normalized_path.replace(".mp3", "_thumbnail.jpg")  # Derive thumbnail path

        # Validate that the audio file exists
        if not os.path.exists(normalized_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Schedule file deletion after serving
        background_tasks.add_task(delete_file, normalized_path)
        if os.path.exists(thumbnail_path):  # Only delete if the thumbnail exists
            background_tasks.add_task(delete_file, thumbnail_path)

        # Serve the audio file
        return FileResponse(
            path=normalized_path,
            media_type="audio/mpeg",
            filename=os.path.basename(normalized_path),  # Force the correct filename in the download
        )
    except Exception as e:
        print(f"Error in serve_soundcloud_file route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def delete_file(file_path: str):
    """
    Deletes the specified file.
    :param file_path: Path to the file to be deleted.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"Error deleting file {file_path}: {str(e)}")
