from SpotifyScraper.scraper import Scraper, Request
request = Request().request()
scraper = Scraper(session=request)
from urllib.parse import unquote


playlist_information = scraper.get_playlist_url_info(url=unquote('https://open.spotify.com/playlist/37i9dQZF1DX74DnfGTwugU'))


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