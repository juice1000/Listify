import requests
from bs4 import BeautifulSoup
import json
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep
import re



def extract_playlist_meta_information(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    track_metadata = soup.find_all('meta', {'name': 'music:song'})

    song_urls = []
    for element in track_metadata:
        element_url = element.attrs['content']
        song_urls.append((element_url))
    
    return song_urls


def extract_data_from_song_url(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # TODO: #1 this is quite unstable the way we do it, let's find a better solution!
    track_elements = soup.find_all('title')[0].contents[0].split(('- song and lyrics by'))
    song_name = track_elements[0].strip()
    artist_name = re.sub( '\|', '',re.sub( 'Spotify', '', track_elements[1])).strip()
    return (song_name, artist_name)


# using selenium and beautiful soup
def track_data_extractor(URL):
    options = ChromeOptions()
    options.headless = True

    # TODO: needs to be stored on webserver too when we're ready to deploy
    driver = Chrome(executable_path='/Users/julienlook/Documents/Coding/spotify_downloader/chromedriver', options=options)
    driver.get(url=URL)

    # extract information from html head
    # TODO: do this for all titles and put in array
    extracted_song_url = extract_playlist_meta_information(driver)
    driver.quit()
    tracks = []
    for song_url in extracted_song_url:
        # relaunch driver
        driver = Chrome(executable_path='/Users/julienlook/Documents/Coding/spotify_downloader/chromedriver', options=options)
        driver.get(url=song_url)

        track_info = extract_data_from_song_url(driver)

        # TODO: store this in another array (check array format we prepped for the youtube download)
        print(track_info)
        tracks.append(track_info)
        
        driver.quit()
    
    return tracks



# TODO: we need a function that checks if the input source is truly a playlist of just a song
# TODO: we could create a 2 stream product that can download songs or playlists

# TODO this needs to be left to the app input prompt
URL = "https://open.spotify.com/playlist/1QzMPmOyuxetr3Mbw4vBb8"
track_data_extractor(URL)
