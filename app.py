from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import spotify_get_song_names as spt

import os
app = Flask(__name__)
environment_configuration = os.environ['CONFIGURATION_SETUP']
app.config.from_object(environment_configuration)

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        title = request.form['playlist']
        if not title:
            flash('Title is required!')
        song_titles = spt.retrieve_playlist_songs(title, False)
        #print(song_titles)
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)
