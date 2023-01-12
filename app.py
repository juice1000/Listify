from flask import Flask, render_template, request, flash, send_file, url_for, jsonify, redirect
import spotify_get_song_names as spt
import youtube_downloader as yt
from config import Prod, Dev
from zipfile import ZipFile
import os
from os.path import basename
from io import BytesIO
import shutil
import time
import spotify_get_song_names as spt
from celery import Celery
import os
import boto3

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Prod)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

local_download_directory = os.path.join(os.getcwd(), 'static', 'music_files')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/playlist_check', methods=('GET', 'POST'))
def playlist_check():
    if request.method == 'POST':
        playlist_id = request.json["playlist_id"]
        print(playlist_id)
        if not playlist_id:
            flash('Playlist Link is required!')
        
        playlist_too_long = spt.playlist_too_long(playlist_id)
        return jsonify({'response': playlist_too_long})


@app.route('/download', methods=('GET', 'POST'))
def download():
    if request.method == 'POST':
        playlist_id = request.json["playlist_id"]
        filetype = request.json["filetype"]
        print(playlist_id)
        if not playlist_id:
            flash('Playlist Link is required!')
        
        # First third of progress bar would be song title retrieval, second third would be download, last would be zipping
        task = background_process.apply_async(args=(playlist_id, filetype))
        result = jsonify({}), 202, {'Location': url_for('progress', task_id=task.id)}
        return result


def zipping(data, dirName):
    # create a ZipFile object
    with ZipFile(data, 'w') as zipObj:
    # Iterate over all the files in directory
        print('existing in zipping ', os.path.exists(dirName))
        
        for folderName, subfolders, filenames in os.walk(dirName):
            for filename in filenames:
                #create complete filepath of file in directory

                filePath = os.path.join(folderName, filename)
                print('filepath to write: ', filePath)
                # Add file to zip
                zipObj.write(filePath, basename(filePath))


@app.route('/send_zip_file', methods=('GET', 'POST'))
def send_zip_file():
    path = local_download_directory
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path)
    # initialize active storage
    s3 = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    # download files into local directory
    for key in s3.list_objects(Bucket=AWS_BUCKET_NAME)['Contents']:
        key_filename = key["Key"].split("public/", 1)[1]
        download_filename = os.path.join(path, key_filename)
        s3.download_file(Bucket=AWS_BUCKET_NAME, Key=key['Key'], Filename=download_filename)
        s3.delete_object(Bucket=AWS_BUCKET_NAME, Key=key['Key'])
        print('downloaded song: ', key_filename)
    
    data = BytesIO()
    print('zipping')
    data.seek(0)
    return send_file(data, mimetype='application/zip', as_attachment=True, download_name='music_playlist.zip')


@celery.task(bind=True)
def background_process(self, playlist_link, filetype):
    path = local_download_directory
    shutil.rmtree(path, ignore_errors=True)
    process = 0
    song_titles = spt.track_data_extractor(playlist_link)
    process = 30
    single_song_percent = int(70 / len(song_titles))
    self.update_state(state='PROGRESS', meta={'current': process, 'total': 100, 'status': 'downloading songs'})

    # initialize active storage
    s3 = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    for song in song_titles:
        filename = yt.download_from_link(song, filetype)
        self.update_state(state='PROGRESS', meta={'current': process, 'total': 100, 'status': 'downloading songs'})
        filepath = os.path.join(path, filename)
        if os.path.exists(filepath):
            # upload to active storage here
            key = 'public/' + filename
            s3.upload_file(Filename=filepath, Bucket=AWS_BUCKET_NAME, Key=key)

        process += single_song_percent
        self.update_state(state='PROGRESS', meta={'current': process, 'total': 100, 'status': 'downloading songs'})

    shutil.rmtree(path, ignore_errors=True)
    self.update_state(state='SUCCESS', meta={'current': 100, 'total': 100, 'status': 'Finished downloads! Zipping now...','result': 42})
    time.sleep(2)
    return {'current': 100, 'total': 100, 'status': 'Finished downloads! Zipping now...',
            'result': 42}


@app.route('/progress/<task_id>', methods=('GET', 'POST'))
def progress(task_id):
    task = background_process.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Scanning through playlist...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    json_response = jsonify(response)
    return json_response


if __name__ == "__main__":
    app.run(host=app.config.get("DOMAIN"))
