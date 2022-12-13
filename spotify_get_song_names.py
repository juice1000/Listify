from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep


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
        tracks.append(f"{song_name}  by  {artist_name}")

    return tracks


# using selenium and beautiful soup
def track_data_extractor(URL):
    browser = 'chrome'
    if browser == 'chrome': 
        options = ChromeOptions()
        options.headless = False
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser == 'firefox':
        options = FirefoxOptions()
        options.headless = True
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        print(Exception("current browser not supported"))
    

    driver.get(url=URL)
    actions = ActionChains(driver)

    # load soup
    # TODO find a better way to wait for HTML parser to load
    sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    song_count = get_number_of_tracks(soup)

    # undo cookies window
    try:
        locator = 'onetrust-accept-btn-handler'
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID,locator))).click()
        locator = 'Button-sc-y0gtbx-0.hNxTPt.CVqkR3tIgVsGD4SvvXS4'
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME,locator))).click()
        print('disabled all buttons')
    except:
        print('some buttons were not available')

    # click on main panel once to enable scrolling
    locator = 'Root__main-view'
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME,locator))).click()

    # check if last track is visible by HTML 
    while not is_first_and_last_element_visible(soup, song_count):
        scroll(actions)
        # reinitialize soup
        # TODO: get a proper sleep time to see if elements really loaded
        sleep(9)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    

    tracks = extract_song_data(soup, song_count)
    driver.quit()
    return tracks



# TODO: we need a function that checks if the input source is truly a playlist of just a song
# TODO: we could create a 2 stream product that can download songs or playlists

# TODO: decide browser based on what we really use

URL = 'https://open.spotify.com/playlist/1QzMPmOyuxetr3Mbw4vBb8'
track_data_extractor(URL)
