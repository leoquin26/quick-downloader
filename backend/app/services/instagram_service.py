import os
import yt_dlp
import requests
from fastapi import HTTPException

DOWNLOAD_FOLDER = "app/downloads/"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

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

def download_instagram_video(url: str) -> dict:
    """
    Downloads an Instagram video and its thumbnail, and saves both files locally.
    :param url: URL of the Instagram video.
    :return: Dictionary with details of the downloaded video and thumbnail.
    """
    try:
        ydl_opts = {
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
            "format": "best",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            
            if not os.path.exists(file_path):
                raise HTTPException(status_code=500, detail="Failed to download the video.")

            # Download the thumbnail
            thumbnail_url = info.get("thumbnail", None)
            thumbnail_path = None
            if thumbnail_url:
                thumbnail_name = f"{info['title']}_thumbnail.jpg"
                thumbnail_path = os.path.join(DOWNLOAD_FOLDER, thumbnail_name)
                download_image(thumbnail_url, thumbnail_path)

            return {
                "message": "Video downloaded successfully",
                "file_path": os.path.basename(file_path),  # Only the filename
                "thumbnail": os.path.basename(thumbnail_path) if thumbnail_path else None,
                "title": info.get("title", "Unknown Title"),
            }
    except Exception as e:
        print(f"Error in download_instagram_video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading Instagram video: {str(e)}")
