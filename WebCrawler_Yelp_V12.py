import requests
from bs4 import BeautifulSoup
import pymysql.cursors

#creates a connection to the mysql-server
#ggf host, user, db, etc. mit userinput abfragen
connection = pymysql.connect(host='localhost',
                              user='root',
                              db='YELP',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()
cursor.execute("USE YELP")

#Daten in YELP_ADDRESS einfügen
def store_address(compname, street, postalcode, city, rating, segment, reviews):
    cursor.execute("INSERT INTO `YELP_ADDRESS` (`comp_name`, `street`, `postalcode`, `city`, `rating`, `segment`, `reviews`) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                   (compname, street, postalcode, city, rating, segment, reviews))
    cursor.connection.commit()

#in YELP_Review einfügen
def store_review(text1,bewstars1):
    lastentry = cursor.execute("SELECT Restaurant_id from YELP_ADDRESS ORDER BY Restaurant_id DESC")
    cursor.execute("INSERT INTO `YELP_REVIEWS` (`Restaurant_id`,`review`, `rating`) VALUES (%s,%s,%s)",
                   (lastentry, text1, bewstars1))
    cursor.connection.commit()

#in YELP_PIC einfügen
def store_pic(pic):
    lastidreview = cursor.execute("SELECT Review_id from YELP_REVIEWS ORDER BY Review_id DESC")
    cursor.execute("INSERT INTO `YELP_PIC` (`Review_id`,`pic_url`) VALUES (%s,%s)", (lastidreview, pic))
    cursor.connection.commit()

#in YELP_USER einfügen
def store_user(name, reviews):
    lastidreview = cursor.execute("SELECT Review_id from YELP_REVIEWS ORDER BY Review_id DESC")
    cursor.execute("INSERT INTO `YELP_USER` (`Review_id`,`name`, `reviews`) VALUES (%s,%s,%s)", (lastidreview, name, reviews))
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


# Die verlinkte Seite wird geladen
def get_single_item(item_url):
    # html in soup laden
    source_code = requests.get(item_url).text
    soup = BeautifulSoup(source_code, 'html.parser')

    # Name und Adresse aufgesplittet in PLZ, Ort & Straße
    name = soup.find('a', {'class': 'biz-name'})
    street = soup.find("span", {"itemprop": "streetAddress"})
    postalCode = soup.find("span", {"itemprop": "postalCode"})
    city = soup.find("span", {"itemprop": "addressLocality"})
    print('Name des Restaurants: ' + name.string)
    print('Street: ' + street.text)
    print('Postalcode: ' + postalCode.text)
    print('City: ' + city.text)

    # Sternebewertung wird ausgegeben
    stars = soup.find('div', {'class': 'biz-rating biz-rating-very-large clearfix biz-rating-DE'}).find('img').get('alt')
    print('Anzahl der Sterne: ' + stars)

    # Anzahl der Reviews der Objektes
    reviews = soup.find('span', {'class': 'review-count rating-qualifier'})

    # Das Preissegment wird ausgegeben
    segment = soup.find('span', {'class': 'business-attribute price-range'})

    # Fängt den Fehler auf, dass kein Preissegment verfügbar ist.
    try:
        print('Preissegment: ' + segment.string)
    except AttributeError:
        print("Das Preissegment wurde nicht definiert.")

    # uncomment when SQL is working
    try:
        store_address(name.text.strip(), street.text.strip(), postalCode.text.strip(), city.text.strip(), stars.strip(),
                  segment.text.strip(), reviews.text.strip())
    except:
        pass
    #Link zu den einzelnen Bewertungen -> neue Methode
    loop_bewertungen(soup)

    # Bewertungen werden ausgegeben
def loop_bewertungen(soup):

    loop_bew = soup.find_all('div', {'class': 'review review--with-sidebar'})
    for bewertung in loop_bew:
        #Username des Bewerters
        username = bewertung.find('a', {'class': 'user-display-name js-analytics-click'})
        #Anzahl der Bewertungen
        anzahlbew = bewertung.find('li', {'class': 'review-count responsive-small-display-inline-block'})
        #Text der Bewertung
        text = bewertung.find('p', {'lang': 'de'})
        bewstars = bewertung.find('div', {'class': 'biz-rating biz-rating-large clearfix'}).find('img').get('alt')
        ##SQL-Befehl: Bewertung & Rating wird in die DB eingefügt
        store_review(text.text.strip(), bewstars)
        #store_user(username, anzahlbewert)
        store_user(username.text.strip(), anzahlbew.text.strip())
        pic = bewertung.find_all('a', {'class': {'biz-shim js-lightbox-media-link js-analytics-click'}})

        try:
            print('Name des Benutzers: ' + username.string)
        except AttributeError:
            username = bewertung.find('span', {'class': 'ghost-user ghost-qype-user'})
            print('Name des Benutzers: ' + username.text)

        for pics in pic:
            pic = 'https://www.yelp.com' + pics.get('href')
            try:
                store_pic(pic.strip())
            except:
                pass


    # Falls eine zweite Seite gibt, wird auf die zweite Seite gesprungen und die Kommentare werden ausgegeben.
    if soup.find("span",{"class": "pagination-label responsive-hidden-small pagination-links_anchor"}):
        link = soup.find("a",{"class": "u-decoration-none next pagination-links_anchor"})
        href = link.get("href")
        source_code = requests.get(href)
        plain_text = source_code.text
        new_soup = BeautifulSoup(plain_text, 'html.parser')
        loop_bewertungen(new_soup)

find_object()