import os
import re
import subprocess
from pathlib import Path

import _deprecated_spotify_get_song_names as spt
import yt_dlp
from pytube import Search, YouTube


def progress_hook(d):
    if d["status"] == "finished":
        print(f"✅ Download complete: {d['filename']}")


def search_youtube(song_title: str, max_results: int = 5, max_length: int = 750):
    """Search for a song on YouTube and return video URLs."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "default_search": "ytsearch",
        "extract_flat": True,  # Don't download, just get video info
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_query = f"ytsearch{max_results}:{song_title}"
        info = ydl.extract_info(search_query, download=False)

        valid_tracks = []
        if "entries" in info and len(info["entries"]) > 0:
            for entry in info["entries"]:
                duration = entry.get("duration", 0)  # Get duration in seconds
                if duration <= max_length:
                    valid_tracks.append(entry["url"])

        return valid_tracks


def download_audio(video_url: str, target_file_type: str, parent_dir: str):
    """Download highest quality audio from YouTube."""
    ydl_opts = {
        "format": "bestaudio/best",  # Get the best available audio format
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # Convert to audio
                "preferredcodec": target_file_type,  # Ensure MP3 output
                "preferredquality": "320",  # Set bitrate
            }
        ],
        "outtmpl": f"{parent_dir}/%(title)s",  # Save as song title
        "quiet": True,  # Suppress most output
        "noprogress": True,  # Hide progress bar
        "progress_hooks": [progress_hook],  # Minimal updates
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

        return True


def download_from_link(playlist_link, debug=False):

    # TODO: print out chosen playlist name
    if playlist_link == "":
        playlist_link = "https://open.spotify.com/playlist/3ULk7XI8p5pQ0zv0dVbTzs?si=149f094ef0854170"
        # debug = True

    # Parse playlist id from link
    playlist_id = re.findall(r"playlist/(.*)\?", playlist_link)[0]

    # target_file_type = input('Specify file type [default is .wav]: \n')
    # if target_file_type != '.wav' or target_file_type != '.mp3':
    #    print('No valid input found, music files will be converted to .wav\n')
    #    target_file_type = '.wav'
    target_file_type = "wav"

    home = str(Path.home())
    music_directory = home + "/Music/"
    music_subdirectory = input(
        "Specify directory [press enter if you want to create a directory in music folder]: \n"
    )
    if music_subdirectory == "":
        music_subdirectory = "spotify_downloaded_playlist/downtempo"

    parent_dir = music_directory + music_subdirectory

    print("will save in ", parent_dir)
    # parent_dir = 'static/music_files'

    song_titles = spt.retrieve_playlist_songs(playlist_id, debug=debug)

    for song in song_titles:
        print(song)
        video_urls = search_youtube(song, max_results=5)

        if video_urls:
            for url in video_urls:
                try:
                    # Download audio
                    print(f"Downloading: {url}")
                    download_audio(url, target_file_type, parent_dir)
                    print("Download complete! 🎧")
                    break
                except Exception as e:
                    print(e)


download_from_link("")
