import os
from fastapi import HTTPException
from fastapi.responses import FileResponse

def serve_file(file_path: str, base_folder: str, media_type: str = "video/mp4"):
    """
    Serves a file for direct download.

    :param file_path: Relative path to the file.
    :param base_folder: Base directory where files are stored.
    :param media_type: Media type of the file (default is video/mp4).
    :return: FileResponse object for serving the file.
    """
    try:
        # Normalize the file path
        normalized_path = os.path.join(base_folder, os.path.basename(file_path))

        # Check if the file exists
        if not os.path.exists(normalized_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Serve the file
        return FileResponse(
            normalized_path,
            media_type=media_type,
            filename=os.path.basename(normalized_path),  # Forces the filename for download
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving file: {str(e)}")