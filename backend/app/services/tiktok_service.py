import os
import yt_dlp
import subprocess
import re
from fastapi import HTTPException

# Directory for saving downloaded files
DOWNLOAD_FOLDER = "app/downloads/"
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
        ydl_opts = {"quiet": True}
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
    Downloads a TikTok video and converts it to MP4 format with H.264 and AAC encoding.

    :param url: TikTok video URL.
    :return: Dictionary containing download details, including file path and thumbnail.
    """
    try:
        # Retrieve video info
        video_info = get_video_info(url)
        sanitized_title = sanitize_filename(video_info['title'])

        # Temporary file and final output paths
        temp_output_file = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}_temp.webm")
        final_output_file_base = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}.mp4")
        final_output_file = get_unique_filename(final_output_file_base)

        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": temp_output_file,
        }

        # Download video using yt-dlp
        print(f"Downloading TikTok video from URL: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Re-encode video to H.264 and AAC
        print("Reencoding video to H.264 and AAC...")
        subprocess.run(
            [
                "ffmpeg",
                "-i", temp_output_file,
                "-c:v", "libx264",  # Video codec
                "-c:a", "aac",  # Audio codec
                "-strict", "experimental",  # Enable AAC support
                "-b:a", "192k",  # Audio bitrate
                final_output_file,
                "-y",  # Overwrite if file exists
            ],
            check=True,
        )

        # Remove temporary file
        if os.path.exists(temp_output_file):
            os.remove(temp_output_file)

        # Verify if the final MP4 file exists
        if not os.path.exists(final_output_file):
            raise Exception("Failed to reencode video to MP4 format.")

        print(f"TikTok video downloaded and saved to: {final_output_file}")

        return {
            "message": "Video downloaded successfully",
            "file_path": final_output_file,
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
