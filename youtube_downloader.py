
import re
from pytube import Search, YouTube
from pytube.cli import on_progress
import subprocess
import os
import spotify_get_song_names as spt

song_titles = spt.retrieve_playlist_songs()

target_file_type = '.wav'
parent_dir = '/Users/julienlook/Music/PioneerDJ/new_tracks'

for song in song_titles:
    s = Search(song)
    downloadable_ids = re.findall(r'videoId=(.{11})', str(s.results))
    for id in downloadable_ids:
        try: 
            yt = YouTube('http://youtube.com/watch?v=' + id, on_progress_callback=on_progress)
            stream = yt.streams.get_audio_only()
            stream.download(parent_dir)
            print('success!!')

            default_filename = stream.default_filename
            filename = stream.default_filename[:len(default_filename)-4] +target_file_type
            subprocess.run([
            'ffmpeg',
            '-i', os.path.join(parent_dir, default_filename),
            os.path.join(parent_dir, filename)])
            break
        except Exception as e:
            print(e)