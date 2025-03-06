import os
import yt_dlp
from fastapi import HTTPException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "app/downloads/")
# os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
# import tempfile
# DOWNLOAD_FOLDER = tempfile.gettempdir()

def sanitize_filename(filename: str) -> str:
    """
    Cleans and normalizes a filename to avoid problematic characters.
    """
    return "".join(c if c.isalnum() or c in " .-_()" else "_" for c in filename)

def get_twitter_video_info(url: str) -> dict:
    """
    Retrieves basic video information, including the title and thumbnail.
    """
    try:
        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", "Unknown Title"),
                "thumbnail": info.get("thumbnail", "https://via.placeholder.com/640x360?text=No+Thumbnail"),
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving video info: {str(e)}")

def download_twitter_video(url: str) -> dict:
    """
    Downloads a Twitter video in MP4 format.
    """
    try:
        # Get video information
        video_info = get_twitter_video_info(url)
        sanitized_title = sanitize_filename(video_info["title"])
        output_file = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}.mp4")

        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "outtmpl": output_file,
            "merge_output_format": "mp4",
            "quiet": True,
        }

        print(f"Downloading Twitter video from URL: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Validate the final file exists
        if not os.path.exists(output_file):
            raise Exception("Failed to download the Twitter video.")

        return {
            "message": "Video downloaded successfully",
            "file_path": os.path.basename(output_file),
            "thumbnail": video_info["thumbnail"],
            "title": video_info["title"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading Twitter video: {str(e)}")
