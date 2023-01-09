
import re
from pytube import Search, YouTube
from pytube.cli import on_progress
import subprocess
import os

def download_from_link(song_title, filetype):

    # TODO: handle wrong or empty playlist string

    parent_dir = os.path.join(os.getcwd(), 'static', 'music_files')
    print(parent_dir)
    print(song_title)
    s = Search(song_title)
    downloadable_ids = re.findall(r'videoId=(.{11})', str(s.results))
    filename = ''
    for id in downloadable_ids:
        try: 
            yt = YouTube('http://youtube.com/watch?v=' + id, on_progress_callback=on_progress)
            stream = yt.streams.get_audio_only()
            stream.download(parent_dir)
            print('success!!')

            # Give new filename the specified file convention
            default_filename = stream.default_filename
            filename = default_filename[:len(default_filename)-4] + filetype

            # Transform file with ffmpeg
            subprocess.run([
            'ffmpeg', '-loglevel', 'warning',
            '-i', os.path.join(parent_dir, default_filename),
            os.path.join(parent_dir, filename)])

            # Remove .mov file and keep .wav format
            os.remove(os.path.join(parent_dir, default_filename))

            # After successful run we're done
            break
        except Exception as e:
            print(e)

    return filename
