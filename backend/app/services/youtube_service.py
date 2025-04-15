import os
import yt_dlp
from fastapi import HTTPException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Folder where downloaded files will be stored
DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "/tmp/downloads")
COOKIES_FILE = os.path.join(os.path.dirname(__file__), "cookies.txt")

print(f"Cookies file path: {COOKIES_FILE}")

def sanitize_filename(filename: str) -> str:
    return "".join(c if c.isalnum() or c in " .-_()" else "_" for c in filename)

def get_video_info(url: str) -> dict:
    try:
        ydl_opts = {
            "quiet": True,
            # Usa el archivo cookies.txt para autenticación
            "cookies": COOKIES_FILE
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", "Unknown Title"),
                "thumbnail": info.get("thumbnail", "https://via.placeholder.com/640x360?text=No+Thumbnail"),
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving video info: {str(e)}")

def download_audio(url: str, quality: str) -> dict:
    try:
        bitrate_map = {"320kbps": "320", "256kbps": "256", "128kbps": "128"}
        if quality not in bitrate_map:
            raise ValueError("Invalid quality. Choose from 320kbps, 256kbps, or 128kbps.")

        video_info = get_video_info(url)
        sanitized_title = sanitize_filename(video_info["title"])
        output_file_base = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}_{quality}")

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": bitrate_map[quality],
                }
            ],
            "outtmpl": output_file_base,
            "quiet": False,  # Desactiva quiet para ver los logs de yt-dlp
            "verbose": True,  # Activa verbose para depuración
            # Usa el archivo cookies.txt para autenticación
            "cookies": COOKIES_FILE
        }

        print(f"Downloading audio from URL: {url} with quality: {quality}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        final_output_file = f"{output_file_base}.mp3"
        if not os.path.exists(final_output_file):
            raise HTTPException(status_code=500, detail=f"File not found: {final_output_file}")

        print(f"Audio downloaded successfully: {final_output_file}")
        return {
            "message": "Audio downloaded successfully",
            "file_path": os.path.basename(final_output_file),
            "thumbnail": video_info["thumbnail"],
            "title": video_info["title"],
        }
    except Exception as e:
        print(f"Error in download_audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading audio: {str(e)}")

def download_video(url: str) -> dict:
    try:
        video_info = get_video_info(url)
        sanitized_title = sanitize_filename(video_info["title"])
        output_file = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}.mp4")
        
        ydl_opts = {
            "format": "best[ext=mp4]/best",
            "outtmpl": output_file,
            "merge_output_format": "mp4",
            "quiet": False,
            "verbose": True,
            # Usa el archivo cookies.txt para autenticación
            "cookies": COOKIES_FILE
        }

        print(f"Downloading video from URL: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if not os.path.exists(output_file):
            raise HTTPException(status_code=500, detail=f"File not found: {output_file}")

        return {
            "message": "Video downloaded successfully",
            "file_path": os.path.basename(output_file),
            "thumbnail": video_info["thumbnail"],
            "title": video_info["title"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading video: {str(e)}")

def get_unique_filename(filepath: str) -> str:
    base, ext = os.path.splitext(filepath)
    counter = 1
    while os.path.exists(filepath):
        filepath = f"{base} ({counter}){ext}"
        counter += 1
    return filepath