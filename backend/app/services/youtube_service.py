import os
import yt_dlp
import subprocess
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

    :param url: YouTube video URL.
    :param quality: Desired audio quality (320kbps, 256kbps, 128kbps).
    :return: Dictionary with file path, thumbnail, and title.
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
            "outtmpl": f"{output_file_base}.%(ext)s",  # Ensure correct file extension
        }

        # Download audio using yt-dlp
        print(f"Downloading audio from URL: {url} with quality: {quality}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Final file path
        final_file = f"{output_file_base}.mp3"
        print(f"Audio downloaded and saved to: {final_file}")
        return {
            "message": "Audio downloaded successfully",
            "file_path": os.path.basename(final_file),  # Only the filename
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

    :param url: YouTube video URL.
    :return: Dictionary with file path, thumbnail, and title.
    """
    try:
        # Retrieve video information
        video_info = get_video_info(url)
        sanitized_title = sanitize_filename(video_info["title"])

        # yt-dlp configuration
        temp_output_file = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}_temp.webm")
        final_output_file_base = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}.mp4")
        final_output_file = get_unique_filename(final_output_file_base)  # Generate a unique filename

        ydl_opts = {
            "format": "bestvideo+bestaudio/best",  # Select the best video and audio quality
            "outtmpl": temp_output_file,  # Temporary file with .webm extension
        }

        # Download video using yt-dlp
        print(f"Downloading video from URL: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Reencode video and audio to H.264 and AAC respectively
        print(f"Reencoding video to H.264 and AAC...")
        subprocess.run(
            [
                "ffmpeg",
                "-i", temp_output_file,
                "-c:v", "libx264",  # Reencode video to H.264
                "-c:a", "aac",  # Reencode audio to AAC
                "-strict", "experimental",  # Support for AAC
                "-b:a", "192k",  # Audio bitrate
                final_output_file,  # Final MP4 file
                "-y",  # Force overwrite in case of errors
            ],
            check=True
        )

        # Remove the temporary file
        if os.path.exists(temp_output_file):
            os.remove(temp_output_file)

        # Validate that the final MP4 file exists
        if not os.path.exists(final_output_file):
            raise Exception("Failed to reencode video to MP4 format.")

        print(f"Video downloaded and saved to: {final_output_file}")

        return {
            "message": "Video downloaded successfully",
            "file_path": os.path.basename(final_output_file),  # Only the filename
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
