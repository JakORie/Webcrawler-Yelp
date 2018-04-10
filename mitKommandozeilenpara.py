import requests
from bs4 import BeautifulSoup

#eingeben der beiden Parameter Name & Ort
searchname = raw_input("Welches Restaurant suchen Sie:\n")
searchplace = raw_input('In welcher Stadt suchen Sie?\n')

def find_object():
    url = 'https://www.yelp.com/search?find_desc=' + searchname + '&find_loc=' + searchplace
    source_code = requests.get(url, allow_redirects=False)
    plain_text = source_code.text.encode('ascii', 'replace')
    soup = BeautifulSoup(plain_text, 'html.parser')
    name = soup.find('a', {'class': 'biz-name'})
#Name des Restaurants wird ausgegeben
    print('Name des Restaurants: '+ name.string)
    link = soup.find('a', {'class': {'biz-name'}})
    href = 'https://www.yelp.com' + link.get('href')
#Es wird auf die naechste Seite gegangen
    get_single_item(href)


def get_single_item(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,'html.parser')
#Adresse wird ausgegeben
    adress = soup.find_all("address")[1].string
    print('Adresse: ' + adress)
#Sternebewertung wird ausgegeben
    stars = soup.find('div', {'class': 'biz-rating biz-rating-very-large clearfix'})
    stars1 = stars.find('img').get('alt')
    print(stars1)
#Anzahl an Bewertungen
    reviews = soup.find('span', {'class': 'review-count rating-qualifier'})
    print('Anzahl der Reviews: ' + reviews.string)
#Das Preissegment wird ausgegeben
    segment = soup.find('span', {'class': 'business-attribute price-range'})
    print('Preissegment: ' + segment.string)

    test = soup.find_all('div', {'class': 'review review--with-sidebar'})
    for bewertung in test:
        bewertung1 = bewertung.find('a', {'class': 'user-display-name js-analytics-click'})
        anzahlbew = bewertung.find('li', {'class': 'review-count responsive-small-display-inline-block'})
        anzahlbewert = anzahlbew.find('b')
        text = bewertung.find('p', {'lang': 'en'})
        bewstars = bewertung.find('div', {'class': 'biz-rating biz-rating-large clearfix'})
        bewstars1 = bewstars.find('img').get('alt')
        print('Name des Benutzers: ' + bewertung1.string)
        print('Rating des Benutzers: ' + bewstars1)
        print('abgegebene Bewertungen: ' + anzahlbewert.text)
        print('Review: ' + text.text)

find_object()
