import os
import re
from pathlib import Path

import libs.spotify_get_song_names as spt
import yt_dlp


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


def download_audio(video_url: str, target_file_type: str, target_folder: str):
    """Download highest quality audio from YouTube."""
    ydl_opts = {
        "format": "bestaudio/best",  # Get the best available audio format
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # Convert to audio
                "preferredcodec": target_file_type,
                "preferredquality": "320",  # Set bitrate
            }
        ],
        "outtmpl": f"{target_folder}/%(title)s",  # Save as song title
        "quiet": True,  # Suppress most output
        "noprogress": True,  # Hide progress bar
        "progress_hooks": [progress_hook],  # Minimal updates
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

        return True


def download_from_link(playlist_link, debug=False):
    """Download songs from a YouTube playlist link."""
    if playlist_link == "" or playlist_link is None:
        raise ValueError("Playlist link cannot be empty")
        # debug = True

    print(f"Downloading from playlist: {playlist_link}")
    # Parse playlist id from link
    playlist_id = re.findall(r"playlist/(.*)\?", playlist_link)[0]

    # target_file_type = input('Specify file type [default is .wav]: \n')
    # if target_file_type != '.wav' or target_file_type != '.mp3':
    #    print('No valid input found, music files will be converted to .wav\n')
    #    target_file_type = '.wav'
    target_file_type = "wav"

    home = str(Path.home())
    music_directory = home + "/Music/"
    # music_subdirectory = input("Specify directory [press enter if you want to create a directory in music folder]: \n")
    if music_subdirectory == "":
        music_subdirectory = "spotify_downloaded_playlist/afro_jena"

    parent_dir = music_directory + music_subdirectory
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    print("will save in ", parent_dir)
    # parent_dir = 'static/music_files'

    song_titles = spt.retrieve_playlist_songs(playlist_id, debug=debug)
    # song_titles = song_titles[72:]  # We'll truncate because it failed there
    for song in song_titles:
        print(song)
        truncated_name = song.split(" by")[0].strip()
        if is_song_saved(truncated_name, parent_dir, target_file_type):
            print(f"⏩ Already downloaded\n")
            continue
        video_urls = search_youtube(song, max_results=5)
        # video_urls = ["https://www.youtube.com/watch?v=P6YV76CnsKM"]

        if video_urls:
            for url in video_urls:
                try:
                    # Download audio
                    print(f"Downloading: {url}")
                    download_audio(url, target_file_type, parent_dir)
                    print("Download complete! 🎧\n")
                    break
                except Exception as e:
                    print(e)


def is_song_saved(truncated_name: str, parent_dir: str, target_file_type: str):
    """Check if a song (truncated before 'by') is already saved in the target directory."""
    # Search for files starting with truncated_name and ending with target_file_type
    for file in os.listdir(parent_dir):
        if truncated_name in file:
            return True
    return False


def download_songs_from_playlist(
    playlist_id: str, target_folder: str, target_file_type: str = "wav", debug: bool = False
):
    """Download songs from a Spotify playlist using just the playlist ID."""
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    print(f"Will save in {target_folder}")

    try:
        song_titles = spt.retrieve_playlist_songs(playlist_id, debug=debug)

        for song in song_titles:
            print(song)
            truncated_name = song.split(" by")[0].strip()
            if is_song_saved(truncated_name, target_folder, target_file_type):
                print(f"⏩ Already downloaded\n")
                continue

            video_urls = search_youtube(song, max_results=5)

            if video_urls:
                for url in video_urls:
                    try:
                        print(f"Downloading: {url}")
                        download_audio(url, target_file_type, target_folder)
                        print("Download complete! 🎧\n")
                        break
                    except Exception as e:
                        print(e)
        return True
    except Exception as e:
        print(f"Error downloading playlist: {e}")
        return False


if __name__ == "__main__":
    # Call with an empty string to use the default playlist link
    download_from_link("https://open.spotify.com/playlist/3jpyYM6tKCg3xmYvI8qTeU?si=ddeab91e74474cce")
