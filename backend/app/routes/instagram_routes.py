from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from fastapi.responses import FileResponse
from app.services.instagram_service import download_instagram_video
import os
from dotenv import load_dotenv

instagram_router = APIRouter()

# Load environment variables
load_dotenv()
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "/tmp/downloads")


@instagram_router.post("/instagram/download")
async def instagram_download(request: Request):
    """
    Downloads an Instagram video.
    """
    try:
        data = await request.json()
        url = data.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="Instagram URL is required.")
        result = download_instagram_video(url)
        return {
            "message": result["message"],
            "file_path": result["file_path"],
            "thumbnail": f"instagram/thumbnail/{result['thumbnail']}" if result.get("thumbnail") else None,
            "title": result.get("title"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading Instagram video: {str(e)}")


@instagram_router.get("/instagram/download/file")
async def serve_instagram_file(file_path: str, background_tasks: BackgroundTasks):
    """
    Serves an Instagram file for direct download.
    Deletes the video and its associated thumbnail after the user completes the download.
    """
    try:
        # Build the absolute path for the file and associated thumbnail
        absolute_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(file_path))
        thumbnail_path = absolute_path.replace(".mp4", "_thumbnail.jpg")

        # Validate that the file exists
        if not os.path.exists(absolute_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Schedule deletion of the file and its thumbnail after serving
        background_tasks.add_task(delete_file, absolute_path)
        if os.path.exists(thumbnail_path):  # Only schedule if the thumbnail exists
            background_tasks.add_task(delete_file, thumbnail_path)

        # Serve the file
        return FileResponse(
            path=absolute_path,
            media_type="video/mp4",
            filename=os.path.basename(absolute_path)  # Force the correct filename in the download
        )
    except Exception as e:
        print(f"Error in serve_instagram_file route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def delete_file(file_path: str):
    """
    Deletes the specified file.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"Error deleting file {file_path}: {str(e)}")


@instagram_router.get("/instagram/thumbnail/{filename}")
async def serve_instagram_thumbnail(filename: str):
    """
    Serves a downloaded Instagram thumbnail.
    """
    try:
        # Absolute path based on the download directory
        absolute_path = os.path.join(DOWNLOAD_FOLDER, filename)

        # Verify if the file exists
        if not os.path.exists(absolute_path):
            raise HTTPException(status_code=404, detail="Thumbnail not found")

        # Return the thumbnail
        return FileResponse(
            absolute_path,
            media_type="image/jpeg",
            filename=os.path.basename(absolute_path)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving thumbnail: {str(e)}")
