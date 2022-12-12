import requests
from bs4 import BeautifulSoup
import json
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from time import sleep
import re


def get_number_of_tracks(soup):
    try:
        meta_song_count = soup.find('meta', {'name': 'music:song_count'})
        song_count = int(meta_song_count.attrs["content"])
        return song_count
    except TypeError:
        print('Could not find valid number of tracks')


def is_first_and_last_element_visible(soup, song_count):
    first_element_locator = '#main .JUa6JJNj7R_Y3i4P8YUX > div:nth-child(2) > div:nth-child(1)'
    first_element = soup.select(first_element_locator)
    last_element_locator = '#main .JUa6JJNj7R_Y3i4P8YUX > div:nth-child(2) > div:nth-child({})'.format(song_count)
    last_element = soup.select(last_element_locator)
    if len(last_element) == 0:
        return False
    if len(first_element) == 0: 
        return Exception('First Element lost on scrolling')
    return True


def scroll(actions):
    # TODO: make scrolling range dependent on screen size
    for i in range(20):
        actions.key_down(Keys.ARROW_DOWN)
    actions.perform()
    ('\nscrolled down once')
    return


def extract_song_data(soup, song_count):
    track_extracts = soup.find_all('div', {"class": "iCQtmPqY0QvkumAOuCjr"})
    
    tracks = []
    for track_extract in track_extracts:
        song_name = track_extract.find('div',"Type__TypeElement-sc-goli3j-0 kHHFyx t_yrXoUO3qGsJS4Y6iXX standalone-ellipsis-one-line").contents[0]
        artist_name = track_extract.find('span',"Type__TypeElement-sc-goli3j-0 dvSMET rq2VQ5mb9SDAFWbBIUIn standalone-ellipsis-one-line").contents[0].contents[0]
        tracks.append((song_name, artist_name))


    return tracks

# using selenium and beautiful soup
def track_data_extractor(URL):
    options = ChromeOptions()
    options.headless = False

    # TODO: needs to be stored on webserver too when we're ready to deploy
    driver = Chrome(executable_path='/Users/julienlook/Documents/Coding/spotify_downloader/chromedriver', options=options)
    driver.get(url=URL)
    #driver.maximize_window()
    actions = ActionChains(driver)

    # load soup
    # TODO find a better way to wait for HTML parser to load
    sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    song_count = get_number_of_tracks(soup)

    # click on main panel once to enable scrolling
    locator = 'contentSpacing'
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME,locator))).click()

    # check if last track is visible by HTML 
    while not is_first_and_last_element_visible(soup, song_count):
        scroll(actions)
        # reinitialize soup
        # TODO: get a proper sleep time to see if elements really loaded
        sleep(9)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    print('left loop')

    extract_song_data(soup, song_count)
    
    driver.quit()



# TODO: we need a function that checks if the input source is truly a playlist of just a song
# TODO: we could create a 2 stream product that can download songs or playlists

# TODO this needs to be left to the app input prompt
URL = "https://open.spotify.com/playlist/1QzMPmOyuxetr3Mbw4vBb8"
track_data_extractor(URL)
