import os
import yt_dlp
import re
from fastapi import HTTPException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "app/downloads/")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes the filename by removing or replacing problematic characters.

    :param filename: Original filename.
    :return: Sanitized filename.
    """
    return re.sub(r'[<>:"/\\|?*]', "", filename).strip()

def get_video_info(url: str) -> dict:
    """
    Retrieves basic video information, including the title and thumbnail.

    :param url: URL of the TikTok video.
    :return: Dictionary containing title and thumbnail URL.
    """
    try:
        ydl_opts = {
            "quiet": False,  # Desactivamos quiet para ver más logs
            "verbose": True,  # Habilitamos modo verbose para depuración
            "print_traffic": True,  # Mostramos el tráfico HTTP
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "no_check_certificate": True,
            "cookiefile": os.path.join(os.path.dirname(__file__), "cookies.txt"),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", "Unknown Title"),
                "thumbnail": info.get("thumbnail", "https://via.placeholder.com/640x360?text=No+Thumbnail"),
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving video info: {str(e)}")

def download_tiktok_video(url: str) -> dict:
    """
    Downloads a TikTok video in MP4 format.

    :param url: TikTok video URL.
    :return: Dictionary containing download details, including file path and thumbnail.
    """
    try:
        # Retrieve video info
        video_info = get_video_info(url)
        sanitized_title = sanitize_filename(video_info["title"])

        # Output file path
        output_file = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}.mp4")
        output_file = get_unique_filename(output_file)  # Ensure unique filename

        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "outtmpl": output_file,
            "merge_output_format": "mp4",
            "quiet": False,
            "verbose": True,
            "print_traffic": True,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "no_check_certificate": True,
            "cookiefile": os.path.join(os.path.dirname(__file__), "cookies.txt"),
        }

        # Download video using yt-dlp
        print(f"Downloading TikTok video from URL: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Validate that the final MP4 file exists
        if not os.path.exists(output_file):
            raise Exception("Failed to download the video in MP4 format.")

        print(f"TikTok video downloaded and saved to: {output_file}")

        return {
            "message": "Video downloaded successfully",
            "file_path": os.path.basename(output_file),
            "thumbnail": video_info["thumbnail"],
            "title": video_info["title"],
        }
    except Exception as e:
        print(f"Error in download_tiktok_video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading TikTok video: {str(e)}")

def get_unique_filename(filepath: str) -> str:
    """
    Generates a unique filename if a file with the same name already exists.

    :param filepath: Base file path.
    :return: Unique file path.
    """
    if not os.path.exists(filepath):
        return filepath

    base, ext = os.path.splitext(filepath)
    counter = 1
    unique_filepath = f"{base} ({counter}){ext}"
    while os.path.exists(unique_filepath):
        counter += 1
        unique_filepath = f"{base} ({counter}){ext}"
    return unique_filepath