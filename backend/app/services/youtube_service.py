import os
import yt_dlp
from fastapi import HTTPException

# Folder where downloaded files will be stored
DOWNLOAD_FOLDER = "app/downloads/"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """
    Cleans and normalizes a filename to avoid problematic characters.
    :param filename: Original filename.
    :return: Cleaned filename.
    """
    return "".join(c if c.isalnum() or c in " .-_()" else "_" for c in filename)


def get_video_info(url: str) -> dict:
    """
    Retrieves basic video information, including the thumbnail and title.
    """
    try:
        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", "Unknown Title"),  # Default title value
                "thumbnail": info.get("thumbnail", "https://via.placeholder.com/640x360?text=No+Thumbnail"),
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving video info: {str(e)}")


def download_audio(url: str, quality: str) -> dict:
    """
    Downloads the audio of a YouTube video in MP3 format with the desired quality.
    Returns information about the downloaded file, including thumbnail and title.
    """
    try:
        # Validate audio quality
        bitrate_map = {"320kbps": "320", "256kbps": "256", "128kbps": "128"}
        if quality not in bitrate_map:
            raise ValueError("Invalid quality. Choose from 320kbps, 256kbps, or 128kbps.")

        # Retrieve video information
        video_info = get_video_info(url)
        sanitized_title = sanitize_filename(video_info["title"])

        # yt-dlp configuration
        output_file = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}_{quality}.mp3")
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": bitrate_map[quality],
                }
            ],
            "outtmpl": output_file,  # Ensure correct file extension
            "quiet": True,  # Suppress unnecessary output
        }

        # Download audio using yt-dlp
        print(f"Downloading audio from URL: {url} with quality: {quality}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"Audio downloaded and saved to: {output_file}")
        return {
            "message": "Audio downloaded successfully",
            "file_path": os.path.basename(output_file),  # Only the filename
            "thumbnail": video_info["thumbnail"],  # Video thumbnail
            "title": video_info["title"],  # Original video title
        }
    except Exception as e:
        print(f"Error in download_audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading audio: {str(e)}")


def download_video(url: str) -> dict:
    """
    Downloads a YouTube video in MP4 format.
    Returns information about the downloaded file, including thumbnail and title.
    """
    try:
        # Retrieve video information
        video_info = get_video_info(url)
        sanitized_title = sanitize_filename(video_info["title"])

        # yt-dlp configuration
        output_file = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}.mp4")
        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",  # Directly get MP4 format if available
            "outtmpl": output_file,  # Ensure correct output file path
            "merge_output_format": "mp4",  # Force final output format
            "quiet": True,  # Suppress unnecessary output
        }

        # Download video using yt-dlp
        print(f"Downloading video from URL: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"Video downloaded and saved to: {output_file}")
        return {
            "message": "Video downloaded successfully",
            "file_path": os.path.basename(output_file),  # Only the filename
            "thumbnail": video_info["thumbnail"],
            "title": video_info["title"],
        }
    except Exception as e:
        print(f"Error in download_video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading video: {str(e)}")


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
