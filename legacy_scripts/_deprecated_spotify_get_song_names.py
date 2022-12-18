import spotipy
from spotipy import util
import subprocess
import json

# Search for name
# TODO: needs to be refactored if we want to make an app out of this
scope = 'user-library-read'
username = 'Julien Look'


def authorization():
    token = util.prompt_for_user_token(username,
    scope,
    client_id='your spotify developer client id',
    client_secret='your spotify developer client secret',
    redirect_uri='http://localhost:9090')
    auth = f"Authorization: Bearer {token}"
    return auth


def retrieve_playlist_songs(playlist_id, debug):
    auth = authorization()

    song_limit = ''
    if debug:
        song_limit = '&limit=1'
        
    json_file = subprocess.check_output(["curl", "-X", "GET", f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?fields=items(track(name%2C%20album(artists(name)))){song_limit}", "-H", auth, '--silent'])

    song_titles = []

    if str(json_file) != "b''" and str(json_file).find("Error") == -1 and str(json_file).find("error") == -1:

        dictionary = json.loads(json_file)
        for item in dictionary.values():
            for value in item:
                track_name = value.get('track', {}).get('name', {})
                artists = value.get('track', {}).get('album', {}).get('artists', {})
                artist_name = artists[0].get('name', {})

                song_titles.append(f"{track_name}  by  {artist_name}")

    
    return song_titles
