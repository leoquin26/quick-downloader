import os
import yt_dlp
import requests
from fastapi import HTTPException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# DOWNLOAD_FOLDER = os.getenv("DOWNLOAD_FOLDER", "app/downloads/")
# os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
import tempfile
DOWNLOAD_FOLDER = tempfile.gettempdir()

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes the filename by removing or replacing problematic characters.
    :param filename: Original filename.
    :return: Sanitized filename.
    """
    return "".join(c if c.isalnum() or c in " .-_()" else "_" for c in filename)

def get_track_info(url: str) -> dict:
    """
    Retrieves basic track information from SoundCloud, including the title and thumbnail.
    :param url: URL of the SoundCloud track.
    :return: Dictionary containing title and thumbnail URL.
    """
    try:
        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", "Unknown Title"),
                "thumbnail": info.get("thumbnail", None),
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving track info: {str(e)}")

def download_thumbnail(thumbnail_url: str, title: str) -> str:
    """
    Downloads the thumbnail image from the provided URL.
    :param thumbnail_url: URL of the thumbnail image.
    :param title: Title of the track (used for naming the thumbnail).
    :return: Path to the saved thumbnail image.
    """
    try:
        if not thumbnail_url:
            raise Exception("No thumbnail URL provided.")

        # Create a sanitized filename for the thumbnail
        sanitized_title = sanitize_filename(title)
        thumbnail_path = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}_thumbnail.jpg")

        # Download the thumbnail
        response = requests.get(thumbnail_url, stream=True)
        if response.status_code == 200:
            with open(thumbnail_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Thumbnail downloaded and saved to: {thumbnail_path}")
            return thumbnail_path
        else:
            raise Exception(f"Failed to download thumbnail. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading thumbnail: {str(e)}")
        return None

def download_soundcloud_track(url: str) -> dict:
    """
    Downloads a track from SoundCloud in MP3 format, along with its thumbnail.
    :param url: SoundCloud track URL.
    :return: Dictionary containing download details, including file path and thumbnail.
    """
    try:
        # Retrieve track information
        track_info = get_track_info(url)
        sanitized_title = sanitize_filename(track_info["title"])

        # Output file path (without extension, yt-dlp will add it automatically)
        output_file = os.path.join(DOWNLOAD_FOLDER, sanitized_title)

        # yt-dlp configuration
        ydl_opts = {
            "format": "*_mp3/bestaudio",  # Dynamically select best available MP3 or audio format
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",  # Set desired quality
                }
            ],
            "outtmpl": f"{output_file}.%(ext)s",  # Use placeholder for extension
            "quiet": True,  # Suppress unnecessary output
        }

        # Download the track using yt-dlp
        print(f"Downloading SoundCloud track from URL: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # The final output file path (yt-dlp will add ".mp3" automatically)
        final_output_file = f"{output_file}.mp3"

        # Validate that the file exists
        if not os.path.isfile(final_output_file):
            print(f"File validation failed: {final_output_file}")
            raise HTTPException(status_code=500, detail="Failed to download the track.")

        # Download the thumbnail if available
        thumbnail_path = None
        if track_info["thumbnail"]:
            thumbnail_path = download_thumbnail(track_info["thumbnail"], track_info["title"])

        print(f"SoundCloud track downloaded and saved to: {final_output_file}")
        return {
            "message": "Track downloaded successfully",
            "file_path": os.path.basename(final_output_file),
            "thumbnail": f"/downloads/{os.path.basename(thumbnail_path)}",  # Ruta accesible públicamente
            "title": track_info["title"],
        }
    except yt_dlp.utils.DownloadError as e:
        print(f"Error in download_soundcloud_track: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to download the track. The requested format may not be available. "
                "Try checking available formats or using another URL."
            ),
        )
    except Exception as e:
        print(f"Error in download_soundcloud_track: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading SoundCloud track: {str(e)}")

def list_available_formats(url: str):
    """
    Lists all available formats for a SoundCloud track.
    :param url: SoundCloud track URL.
    :return: List of available formats.
    """
    try:
        ydl_opts = {"quiet": False, "listformats": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing formats: {str(e)}")
