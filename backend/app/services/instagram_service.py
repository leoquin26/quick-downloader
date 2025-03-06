import os
import yt_dlp
import requests
from fastapi import HTTPException
from dotenv import load_dotenv
import re

load_dotenv()
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "app/downloads/")
# os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
# import tempfile
# DOWNLOAD_FOLDER = tempfile.gettempdir()

def sanitize_filename(filename: str) -> str:
    """
    Cleans and normalizes a filename to avoid problematic characters.

    :param filename: Original filename.
    :return: Cleaned filename.
    """
    return re.sub(r'[<>:"/\\|?*]', "", filename).strip()


def download_image(url: str, save_path: str):
    """
    Downloads an image from a URL and saves it to a local file.

    :param url: URL of the image.
    :param save_path: Local file path to save the image.
    """
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return save_path
        else:
            raise Exception(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error downloading image: {str(e)}")


def get_video_info(url: str) -> dict:
    """
    Retrieves basic video information, including the title and thumbnail.

    :param url: URL of the Instagram video.
    :return: Dictionary containing title and thumbnail URL.
    """
    try:
        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", "Unknown Title"),
                "thumbnail": info.get("thumbnail"),
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving video info: {str(e)}")


def download_instagram_video(url: str) -> dict:
    """
    Downloads an Instagram video in MP4 format, along with its thumbnail.

    :param url: URL of the Instagram video.
    :return: Dictionary with details of the downloaded video and thumbnail.
    """
    try:
        # Retrieve video info
        video_info = get_video_info(url)
        sanitized_title = sanitize_filename(video_info["title"])

        # Output file paths
        output_file = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}.mp4")
        output_file = get_unique_filename(output_file)

        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "outtmpl": output_file,
            "merge_output_format": "mp4",
            "quiet": True,
        }

        # Download video using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Verify that the video file exists
        if not os.path.exists(output_file):
            raise HTTPException(status_code=500, detail="Failed to download the video.")

        # Download the thumbnail if available
        thumbnail_url = video_info.get("thumbnail")
        thumbnail_path = None
        if thumbnail_url:
            thumbnail_name = f"{sanitized_title}_thumbnail.jpg"
            thumbnail_path = os.path.join(DOWNLOAD_FOLDER, thumbnail_name)
            download_image(thumbnail_url, thumbnail_path)

        return {
            "message": "Video downloaded successfully",
            "file_path": os.path.basename(output_file),
            "thumbnail": os.path.basename(thumbnail_path) if thumbnail_path else None,
            "title": video_info["title"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading Instagram video: {str(e)}")


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
