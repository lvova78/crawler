from bs4 import BeautifulSoup

import requests

def parse():

	HEADERS = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
	}

	max_page = 43
	pages = []

	for x in range(1, max_page + 1):
		pages.append(requests.get('https://marketplace.xbox.com/en-US/Games/Xbox360Games?Page=' + str(x), headers = HEADERS))

	games = []

	for r in pages:
		soup = BeautifulSoup(r.content, 'html.parser')
		items = soup.findAll('li', class_ = 'grid-6')

		for item in items:
			games.append({
				'title': item.find('h2').get_text(strip = True),
				'rating': item.find('div', class_ = 'UserRatingStarStrip').get_text(strip = True)
			})

	for game in games:
	 	print(game['title'], game['rating'])

parse()