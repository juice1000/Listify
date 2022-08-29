
import re
from pytube import Search, YouTube
from pytube.cli import on_progress
import subprocess
import os
import spotify_get_song_names as spt
from pathlib import Path


playlist_link = input("Copy & Paste your playlist link into the command line [skip if you want to debug]: \n") 
debug = False

# TODO: print out chose playlist name
if playlist_link == '':
    playlist_link = 'https://open.spotify.com/playlist/1QzMPmOyuxetr3Mbw4vBb8?si=3e9a494834c44ee9'
    debug = True

# Parse playlist id from link
playlist_id = re.findall(r'playlist/(.*)\?', playlist_link)[0]

target_file_type = input('Specify file type [default is .wav]: \n')
home = str(Path.home())
music_directory = home + '/Music/' 
music_subdirectory =  input('Specify directory [press enter if you want to create a directory in music folder]: \n')

if music_subdirectory == '':
    music_subdirectory = 'spotify_downloaded_playlist'

if target_file_type == '':
    target_file_type = '.wav'

parent_dir = music_directory + music_subdirectory

song_titles = spt.retrieve_playlist_songs(playlist_id, debug = debug)

for song in song_titles:
    s = Search(song)
    downloadable_ids = re.findall(r'videoId=(.{11})', str(s.results))
    for id in downloadable_ids:
        try: 
            yt = YouTube('http://youtube.com/watch?v=' + id, on_progress_callback=on_progress)
            stream = yt.streams.get_audio_only()
            stream.download(parent_dir)
            print('success!!')

            # Give new filename the specified file convention
            default_filename = stream.default_filename
            filename = default_filename[:len(default_filename)-4] + target_file_type

            # Transform file with ffmpeg
            subprocess.run([
            'ffmpeg',
            '-i', os.path.join(parent_dir, default_filename),
            os.path.join(parent_dir, filename)])

            # Remove .mov file and keep .wav format
            os.remove(parent_dir + '/' + default_filename)
            # After successful run we're done
            break
        except Exception as e:
            print(e)