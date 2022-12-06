import requests
import pandas as pd

url = "https://www.investing.com/earnings-calendar/"

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

r = requests.get(url, headers=header)
print(r.status_code, '\n\n')
#print(r.text, '\n\n')
print(r.cookies)