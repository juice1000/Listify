import requests
from bs4 import BeautifulSoup
import json
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep

# experimenting with soup
def print_scripts(URL):
    #for script in soup("script"):
    #    script.extract()
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, features='lxml')
    res = soup.find_all('script')
    json_object = json.loads(res.contents[0])
    print(json_object)
#job_elements = results.find_all("div", class_="body-drag-top")
#print(job_elements)

# experimenting with selenium
def selenium_setup(URL):
    options = ChromeOptions()
    options.headless = True
    driver = Chrome(executable_path='/Users/julienlook/Documents/Coding/spotify_downloader/chromedriver', options=options)
    driver.get(url=URL)
    sleep(10)
    
    
    element = driver.find_element(By.CLASS_NAME, 'os-resize-observer-host observed')
    driver.quit()

# experimenting with selenium
def selenium_soup(URL):
    options = ChromeOptions()
    options.headless = True
    driver = Chrome(executable_path='/Users/julienlook/Documents/Coding/spotify_downloader/chromedriver', options=options)
    driver.get(url=URL)
    sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    element = soup.find('div', {"class": "t_yrXoUO3qGsJS4Y6iXX"})
    print(element.contents)
    driver.quit()

URL = "https://open.spotify.com/playlist/1QzMPmOyuxetr3Mbw4vBb8"
#URL = 'https://quotes.toscrape.com/'
selenium_soup(URL)


