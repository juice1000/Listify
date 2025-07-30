import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from libs.youtube_downloader_local_use import download_songs_from_playlist
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DownloadResponse(BaseModel):
    message: str
    playlist_id: str
    download_path: str


@app.get("/download")
async def download_playlist(playlist_id: str, target_folder: str):
    """Download songs from a Spotify playlist using playlist ID."""
    try:
        # Set up download directory
        home = str(Path.home())
        # parent_dir = os.path.join(home, "Music", "spotify_downloaded_playlist", playlist_id)

        # Call the download function
        success = download_songs_from_playlist(playlist_id=playlist_id, target_folder=target_folder)

        if success:
            return DownloadResponse(
                message="Playlist download completed successfully", playlist_id=playlist_id, download_path=target_folder
            )
        else:
            raise HTTPException(status_code=500, detail="Download failed")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading playlist: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
