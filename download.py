import requests
from bs4 import BeautifulSoup
#просто выкачиваем данные
url = 'https://www.zakon.kz/news'
r = requests.get(url)
with open('test.html', 'w') as output_file:
	output_file.write(r.text)

