from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from app.services.instagram_service import download_instagram_video
import os

instagram_router = APIRouter()
DOWNLOAD_FOLDER = "app/downloads/"  # Download directory

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
            "thumbnail": f"/instagram/thumbnail/{result['thumbnail']}" if result.get("thumbnail") else None,
            "title": result.get("title"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading Instagram video: {str(e)}")

@instagram_router.get("/instagram/download/file")
async def serve_instagram_file(file_path: str):
    """
    Serves an Instagram file for direct download.
    :param file_path: Relative path to the file to download.
    """
    try:
        # Build the absolute path from the provided relative path
        absolute_path = os.path.join(DOWNLOAD_FOLDER, file_path)

        # Validate that the file exists
        if not os.path.exists(absolute_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Return the file for download
        return FileResponse(
            absolute_path,
            media_type="video/mp4",
            filename=os.path.basename(absolute_path),  # Force the correct filename in the download
        )
    except Exception as e:
        print(f"Error in serve_instagram_file route: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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
