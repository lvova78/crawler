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
            link = 'https://marketplace.xbox.com' + item.find('a').get('href')
            response = requests.get(link,headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            rating_str = soup.find('div', class_='UserRatingStarStrip').get_text(strip=True)
            # publishing = soup.find('ul', {"id": "ProductPublishing"}).get_text(strip=True)
            game = dict(
                title=soup.find('h1').get_text(strip=True),
                rating=float(rating_str.split(' ')[0]),
                # release_date=publishing(),
                link=link
            )

            if soup.find('span', class_='ProductPrice'):
                game['price']=soup.find('span', class_='ProductPrice').get_text(strip=True)

            games.append(game)

            print("Parsed game:", game)
        
        page_number += 1

if __name__ == '__main__':
    crawl()
