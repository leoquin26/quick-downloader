import os
import yt_dlp
from fastapi import HTTPException
from app.utils.file_utils import sanitize_filename, get_unique_filename

from dotenv import load_dotenv

# Cargar variables de entorno si estás en local
load_dotenv()

# Obtener carpeta de descargas desde el entorno (fallback a /tmp/downloads para Vercel)
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "/tmp/downloads")

def download_facebook_video(url: str) -> dict:
    """
    Downloads a Facebook video in MP4 format.

    :param url: Facebook video URL.
    :return: Dictionary containing download details, including file path and thumbnail.
    """
    try:
        # Extract video information
        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            sanitized_title = sanitize_filename(info.get("title", "Unknown Title"))
            thumbnail = info.get("thumbnail", "https://via.placeholder.com/640x360?text=No+Thumbnail")

        # Output file path
        output_file = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}.mp4")
        output_file = get_unique_filename(output_file)

        ydl_opts.update({
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "outtmpl": output_file,
            "merge_output_format": "mp4",
        })

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if not os.path.exists(output_file):
            raise Exception("Failed to download the video in MP4 format.")

        return {
            "message": "Video downloaded successfully",
            "file_path": os.path.basename(output_file),
            "thumbnail": thumbnail,
            "title": sanitized_title,
        }
    except Exception as e:
        print(f"Error in download_facebook_video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading Facebook video: {str(e)}")
