import requests
from bs4 import BeautifulSoup

# eingeben der beiden Parameter Name & Ort
searchname = input("Welches Restaurant suchen Sie:\n")
searchplace = input('In welcher Stadt suchen Sie?\n')

# Die Suchseite wird geladen
def find_object():
    # html in soup laden
    url = 'https://www.yelp.com/search?find_desc=' + searchname + '&find_loc=' + searchplace
    source_code = requests.get(url, allow_redirects=False)
    plain_text = source_code.text.encode('ascii', 'replace')
    soup = BeautifulSoup(plain_text, 'html.parser')

    # Name des Restaurants wird ausgegeben
    name = soup.find('a', {'class': 'biz-name'})
    print('Name des Restaurants: ' + name.string)

    # Verlinkung vervollständigen
    link = soup.find('a', {'class': 'biz-name'})
    href = 'https://www.yelp.com' + link.get('href')

    # Es wird auf die naechste Seite gegangen
    get_single_item(href)


# Die verlinkte Seite wurde geladen
def get_single_item(item_url):
    # html in soup laden
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    # Adresse wird ausgegeben
    adress = soup.find_all("address")[1].string[9:]
    print('Adresse: ' + adress)

    # Sternebewertung wird ausgegeben
    stars = soup.find('div', {'class': 'biz-rating biz-rating-very-large clearfix'})
    stars1 = stars.find('img').get('alt')
    print(stars1)

    # Anzahl der Reviews
    reviews = soup.find('span', {'class': 'review-count rating-qualifier'}).string[13:]
    print('Anzahl der Reviews: ' + reviews)

    # Das Preissegment wird ausgegeben
    segment = soup.find('span', {'class': 'business-attribute price-range'})
    print('Preissegment: ' + segment.string)

    loop_bewertungen(soup)

    # Bewertungen werden ausgegeben
def loop_bewertungen(soup):
    loop_bew = soup.find_all('div', {'class': 'review review--with-sidebar'})
    for bewertung in loop_bew:
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

    # Falls eine zweite Seite gibt, wird auf die zweite Seite gesprungen und die Kommentare werden ausgegeben.
    if soup.find("span",{"class": "pagination-label responsive-hidden-small pagination-links_anchor"}):
        link = soup.find("a",{"class": "u-decoration-none next pagination-links_anchor"})
        href = link.get("href")
        source_code = requests.get(href)
        plain_text = source_code.text
        new_soup = BeautifulSoup(plain_text, 'html.parser')
        loop_bewertungen(new_soup)

find_object()
