import requests
from bs4 import BeautifulSoup
import pymysql.cursors

#uncomment when SQL is working
#creates a connection to the mysql-server
#ggf host, user, db, etc. mit userinput abfragen
connection = pymysql.connect(host='localhost',
                              user='root',
                              db='yelp2',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()
cursor.execute("USE yelp2")

#inserts data to SQL-TABLE YELP_REVIEW
def store_yelp_reviews(bewstars1, text1):
    cursor.execute("INSERT INTO `YELP_REVIEWS` (`rating`, `review`) VALUES (%s,%s)",
                   (bewstars1,text1))
    cursor.connection.commit()
#inserts data to SQL-TABLE YELP_Restaurant
def store_yelp_restaurant(name, stars1, reviews, segment, street, postalCode, city):
    cursor.execute("INSERT INTO `YELP_RESTAURANT` (`name`, `rating`, `reviews`, `segment`, `segment`, `street`, `postalcode`, `city`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                   (name, stars1, reviews, segment, street, postalCode, city))
    cursor.connection.commit()





# eingeben der beiden Parameter Name & Ort
searchname = input("Welches Restaurant suchen Sie:\n")
searchplace = input('In welcher Stadt suchen Sie?\n')

# Die Suchseite wird geladen
def find_object():
    # html in soup laden
    url = 'https://www.yelp.de/search?find_desc=' + searchname + '&find_loc=' + searchplace
    source_code = requests.get(url, allow_redirects=False).text
    soup = BeautifulSoup(source_code, 'html.parser')

    # Verlinkung vervollständigen
    link = soup.find('a', {'class': 'biz-name'})
    href = 'https://www.yelp.de' + link.get('href')

    # Es wird auf die naechste Seite gegangen
    get_single_item(href)


# Die verlinkte Seite wurde geladen
def get_single_item(item_url):
    # html in soup laden
    source_code = requests.get(item_url).text
    soup = BeautifulSoup(source_code, 'html.parser')

    # Name und Adresse wird ausgegeben
    name = soup.find('a', {'class': 'biz-name'})
    street = soup.find("span", {"itemprop": "streetAddress"})
    postalCode = soup.find("span", {"itemprop": "postalCode"})
    city = soup.find("span", {"itemprop": "addressLocality"})
    print('Name des Restaurants: ' + name.string)
    print('Street: ' + street.text)
    print('Postalcode: ' + postalCode.text)
    print('City: ' + city.text)

    # Sternebewertung wird ausgegeben
    stars = soup.find('div', {'class': 'biz-rating biz-rating-very-large clearfix biz-rating-DE'})
    stars1 = stars.find('img').get('alt')
    print('Anzahl der Sterne: ' + stars1)

    # Anzahl der Reviews
    reviews = soup.find('span', {'class': 'review-count rating-qualifier'}).string[13:]
    print('Anzahl der Reviews: ' + reviews)

    # Das Preissegment wird ausgegeben
    segment = soup.find('span', {'class': 'business-attribute price-range'})

    # Fängt den Fehler auf, dass kein Preissegment verfügbar ist.
    try:
        print('Preissegment: ' + segment.string)
    except AttributeError:
        print("Das Preissegment wurde nicht definiert.")

    # uncomment when SQL is working
    store_yelp_restaurant(name.text.strip(), stars1.text.strip(), reviews.text.strip(), segment.text.strip(), street.text.strip(), postalCode.text.strip(), city.text.strip())

    loop_bewertungen(soup)

    # Bewertungen werden ausgegeben
def loop_bewertungen(soup):

    loop_bew = soup.find_all('div', {'class': 'review review--with-sidebar'})
    for bewertung in loop_bew:
        bewertung1 = bewertung.find('a', {'class': 'user-display-name js-analytics-click'})
        anzahlbew = bewertung.find('li', {'class': 'review-count responsive-small-display-inline-block'})
        anzahlbewert = anzahlbew.find('b')
        text = bewertung.find('p', {'lang': 'de'})
        text1 = text.text.strip()
        bewstars = bewertung.find('div', {'class': 'biz-rating biz-rating-large clearfix'})
        bewstars1 = bewstars.find('img').get('alt')
        bewstars1 = bewstars1[:3]
        ##uncomment when SQL is setup
        store_yelp_reviews(bewstars1, text1)
        pic = bewertung.find_all('a', {'class': {'biz-shim js-lightbox-media-link js-analytics-click'}})
        try:
            print('Name des Benutzers: ' + bewertung1.string)
        except AttributeError:
            bewertung1 = bewertung.find('span', {'class': 'ghost-user ghost-qype-user'})
            print('Name des Benutzers: ' + bewertung1.text)
        print('Rating des Benutzers: ' + bewstars1)
        print('abgegebene Bewertungen: ' + anzahlbewert.text)
        print('Review: ' + text.text)
        for pics in pic:
            print('Bild: ' + 'https://www.yelp.com' + pics.get('href'))


    # Falls eine zweite Seite gibt, wird auf die zweite Seite gesprungen und die Kommentare werden ausgegeben.
    if soup.find("span",{"class": "pagination-label responsive-hidden-small pagination-links_anchor"}):
        link = soup.find("a",{"class": "u-decoration-none next pagination-links_anchor"})
        href = link.get("href")
        source_code = requests.get(href)
        plain_text = source_code.text
        new_soup = BeautifulSoup(plain_text, 'html.parser')
        loop_bewertungen(new_soup)

find_object()
