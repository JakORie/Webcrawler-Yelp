import requests
from bs4 import BeautifulSoup


def trade_spider(max_pages):
    page = 0
    while page <= max_pages:
        url = 'https://www.yelp.com/search?find_loc=Hamburg&start=' + str(page) + '0'
        source_code = requests.get(url, allow_redirects=False)
        plain_text = source_code.text.encode('ascii', 'replace')
        soup = BeautifulSoup(plain_text, 'html.parser')
        for link in soup.findAll('a', {'class': 'biz-name'}):
            href = 'https://www.yelp.com' + link.get('href')
            title = link.string
            print('Name des Restaurants:                    ' + href)
            print('Link:                                    ' + title)
            get_single_item_data(href)
        page += 1


def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,'html.parser')
    # if you want to gather photos from that user
    for item_name in soup.findAll('span', {'class': 'biz-phone'}):
        print(item_name.string)



trade_spider(1)

