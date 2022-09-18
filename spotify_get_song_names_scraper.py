import requests
from bs4 import BeautifulSoup
from selenium import webdriver

URL = "https://open.spotify.com/playlist/1QzMPmOyuxetr3Mbw4vBb8"
#page = requests.get(URL)
#soup = BeautifulSoup(page.content, "html.parser")
driver = webdriver.Chrome('/Users/julienlook/Documents/Coding/spotify_downloader/chromedriver')
driver.get(URL)

soup = BeautifulSoup(driver.page_source, 'html.parser')

results = soup.find(id="main")
#print(results.prettify())
job_elements = results.find_all("div", class_="Root__top-container")

print(job_elements)