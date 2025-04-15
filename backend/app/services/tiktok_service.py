import os
import yt_dlp
import re
from fastapi import HTTPException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "/tmp/downloads")

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "", filename).strip()

def get_video_info(url: str) -> dict:
    try:
        ydl_opts = {
            "quiet": False,
            "verbose": True,
            "print_traffic": True,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "no_check_certificate": True,
            # Cookiefile removed
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
    try:
        video_info = get_video_info(url)
        sanitized_title = sanitize_filename(video_info["title"])
        output_file = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}.mp4")
        output_file = get_unique_filename(output_file)

        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "outtmpl": output_file,
            "merge_output_format": "mp4",
            "quiet": False,
            "verbose": True,
            "print_traffic": True,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "no_check_certificate": True,
            # Cookiefile removed
        }

        print(f"Downloading TikTok video from URL: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

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
    if not os.path.exists(filepath):
        return filepath

    base, ext = os.path.splitext(filepath)
    counter = 1
    unique_filepath = f"{base} ({counter}){ext}"
    while os.path.exists(unique_filepath):
        counter += 1
        unique_filepath = f"{base} ({counter}){ext}"
    return unique_filepath
