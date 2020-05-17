import requests

from bs4 import BeautifulSoup


def crawl():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }

    games = []

    page_number = 1
    while True:
        page_url = f'https://marketplace.xbox.com/en-US/Games/Xbox360Games?Page={page_number}'

        print(f"Loading page #{page_number}: {page_url}")
        response = requests.get(page_url,headers=headers)
        print("Done")

        soup = BeautifulSoup(response.content, 'html.parser')

        if soup.find_all("div", {"class": "NoGamesFound"}):
            # if we reached the end, there is a div with class 'NoGamesFound',
            # so we stop crawling
            print("No data on page, finishing execution.")
            break

        for item in soup.findAll('li', class_='grid-6'):
            rating_str = item.find('div', class_='UserRatingStarStrip').get_text(strip=True)
            game = dict(
                title=item.find('h2').get_text(strip=True),
                rating=float(rating_str.split(' ')[0])
            )
            games.append(game)
            print("Parsed game:", game)

        page_number += 1


if __name__ == '__main__':
    crawl()
