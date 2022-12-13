from flask import Flask, render_template, request, url_for, flash, redirect, send_file
from werkzeug.exceptions import abort
import spotify_get_song_names as spt
import youtube_downloader as yt
from config import Dev
from zipfile import ZipFile
import os
from os.path import basename
from io import BytesIO

import os
app = Flask(__name__)
#environment_configuration = os.environ['CONFIGURATION_SETUP']
environment_configuration = Dev
app.config.from_object(environment_configuration)


@app.route('/')
def index():

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
    return send_file(data, mimetype='application/zip', as_attachment=True, download_name='music_playlist.zip')


if __name__ == "__main__":
    app.run(debug=True)
