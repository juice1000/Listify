from flask import Flask, render_template, request, flash, send_file, after_this_request
import spotify_get_song_names as spt
import youtube_downloader as yt
from config import Prod, Dev
from zipfile import ZipFile
import os
from os.path import basename
from io import BytesIO
import shutil

import os
app = Flask(__name__)
env_conf = Dev
#app.config.from_object(environment_configuration)


@app.route('/')
def index():
    path = 'static/music_files/'
    return render_template('index.html')


def zipping(data, dirName):

    # create a ZipFile object
    with ZipFile(data, 'w') as zipObj:
    # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(dirName):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath, basename(filePath))
        
        

@app.route('/download', methods=('GET', 'POST'))
def download():
    if request.method == 'POST':
        title = request.form['playlist']
        print(title)
        if not title:
            flash('Title is required!')
        yt.download_from_link(title)
    path = 'static/music_files/'
    data = BytesIO()
    zipping(data, path)
    data.seek(0)
    @after_this_request
    def remove_file(response):
        shutil.rmtree(path, ignore_errors=False, onerror=None)
        return response
    return send_file(data, mimetype='application/zip', as_attachment=True, download_name='music_playlist.zip')


if __name__ == "__main__":
    app.run(host=env_conf.DOMAIN)
