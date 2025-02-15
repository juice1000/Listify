# from dotenv import dotenv_values
import os

import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyClientCredentials

# Load env variables
# config = dotenv_values(os.getcwd() + "/legacy_scripts/" + ".env")

# Search for name
# TODO: needs to be refactored if we want to make an app out of this
scope = "user-library-read"
username = "Julien Look"

CLIENT_ID = "54372e1b817d4af19982352a52541a48"
CLIENT_SECRET = "ef3cdce4889e4a55aff19bebbdaa5c24"


# deprecated
def authorization():
    token = util.prompt_for_user_token(
        username, scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:9090/", show_dialog=True
    )
    auth = f"Authorization: Bearer {token}"

    return auth


def authorization2():
    return SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )


def retrieve_playlist_songs(playlist_id, debug):

    # client credentials authorization flow requires only client_id and client_secret
    auth = authorization2()
    sp = spotipy.Spotify(auth_manager=auth)
    # the fields specify the data selection of the query, works somewhat like graphQL
    dictionary = sp.playlist(playlist_id, fields="tracks(items(track(name,album(artists(name)))))")

    song_titles = []
    tracks = dictionary.get("tracks", {}).get("items", [])

    # we only append the first track to our song list if we're in debug mode
    if debug:
        track_name = tracks[0].get("track", {}).get("name")
        artists = tracks[0].get("track", {}).get("album", {}).get("artists", {})
        first_artist_name = artists[0].get("name", {})
        song_titles.append(f"{track_name}  by  {first_artist_name}")
    else:
        for item in tracks:
            track_name = item.get("track", {}).get("name")
            artists = item.get("track", {}).get("album", {}).get("artists", {})
            first_artist_name = artists[0].get("name", {})
            song_titles.append(f"{track_name}  by  {first_artist_name}")
    return song_titles
