import requests
from bs4 import BeautifulSoup
import pymysql.cursors


# Verbindung zum MySQL-Server wird hergestellt - ggf. kann host, user, db, etc separat mit userinput eingegeben werden
connection = pymysql.connect(host='localhost',
                              user='root',
                              db='YELP',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
cursor.execute("USE YELP")

# Methode um Daten in YELP_ADDRESS einzufügen
def store_address(compname, street, postalcode, city, rating, segment, reviews):
    cursor.execute("INSERT INTO `YELP_ADDRESS` (`comp_name`, `street`, `postalcode`, "
                   "`city`, `rating`, `segment`, `reviews`) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                   (compname, street, postalcode, city, rating, segment, reviews))
    cursor.connection.commit()

# Methode um Daten in YELP_REVIEWS einzufügen
def store_review(text1,bewstars1):
    lastentry = cursor.execute("SELECT Restaurant_id from YELP_ADDRESS ORDER BY Restaurant_id DESC")
    cursor.execute("INSERT INTO `YELP_REVIEWS` (`Restaurant_id`,`review`, `rating`) VALUES (%s,%s,%s)",
                   (lastentry, text1, bewstars1))
    cursor.connection.commit()

# Methode um Daten in YELP_PIC einzufügen
def store_pic(pic):
    lastidreview = cursor.execute("SELECT Review_id from YELP_REVIEWS ORDER BY Review_id DESC")
    cursor.execute("INSERT INTO `YELP_PIC` (`Review_id`,`pic_url`) VALUES (%s,%s)", (lastidreview, pic))
    cursor.connection.commit()

# Methode um Daten in YELP_USER einzufügen
def store_user(name, reviews):
    lastidreview = cursor.execute("SELECT Review_id from YELP_REVIEWS ORDER BY Review_id DESC")
    cursor.execute("INSERT INTO `YELP_USER` (`Review_id`,`name`, `reviews`) VALUES (%s,%s,%s)",
                   (lastidreview, name, reviews))
    cursor.connection.commit()


# Name und Ort in der Kommandozeile abfragen
searchname = input("Welches Restaurant suchen Sie:\n")
searchplace = input('In welcher Stadt suchen Sie?\n')

# Methode um die Suchseite zu laden
def find_object():
    # html manipulieren und in soup laden
    url = 'https://www.yelp.de/search?find_desc=' + searchname + '&find_loc=' + searchplace
    source_code = requests.get(url, allow_redirects=False).text
    soup = BeautifulSoup(source_code, 'html.parser')

    # Verlinkung auf die Seite des gesuchten Objekts
    link = soup.find('a', {'class': 'biz-name'})
    href = 'https://www.yelp.de' + link.get('href')

    # Methode um die Seite des Objektes zu laden
    get_single_item(href)


# Die Seite des Objekts wird geladen
def get_single_item(item_url):
    # html in soup laden
    source_code = requests.get(item_url).text
    soup = BeautifulSoup(source_code, 'html.parser')

    # Name und Adresse aufgesplittet in PLZ, Ort & Straße
    name = soup.find('a', {'class': 'biz-name'})
    street = soup.find("span", {"itemprop": "streetAddress"})
    postalCode = soup.find("span", {"itemprop": "postalCode"})
    city = soup.find("span", {"itemprop": "addressLocality"})

    # Sternebewertung des Objekts
    stars = soup.find('div',
                      {'class': 'biz-rating biz-rating-very-large clearfix biz-rating-DE'}).find('img').get('alt')

    # Anzahl der Reviews des Objekts
    reviews = soup.find('span', {'class': 'review-count rating-qualifier'})

    # Preissegment des Objekts
    segment = soup.find('span', {'class': 'business-attribute price-range'})

    # Aufrufen der Methode um die gelesenen Daten in die Tabelle YELP_ADDRESS einzufügen
    try:
        store_address(name.text.strip(), street.text.strip(), postalCode.text.strip(), city.text.strip(), stars.strip(),
                  segment.text.strip(), reviews.text.strip())
    except:
        pass
    # Link zu den einzelnen Bewertungen -> neue Methode
    loop_bewertungen(soup)


    # Bewertungen werden ausgegeben
def loop_bewertungen(soup):

    loop_bew = soup.find_all('div', {'class': 'review review--with-sidebar'})

    # for-Schleife für jede einzelne Bewertung
    for bewertung in loop_bew:

        # Anzahl der Bewertungen
        anzahlbew = bewertung.find('li', {'class': 'review-count responsive-small-display-inline-block'})

        # Text der Bewertung
        text = bewertung.find('p', {'lang': 'de'})

        # Anzahl der bewerteten Sterne des Bewerters
        bewstars = bewertung.find('div', {'class': 'biz-rating biz-rating-large clearfix'}).find('img').get('alt')

        # Aufrufen der Methode um die gelesenen Daten in die Tabelle YELP_REVIEWS einzufügen
        store_review(text.text.strip(), bewstars)

        # Username des Bewerters
        try:
            username = str(bewertung.find('a', {'class': 'user-display-name js-analytics-click'}).string)
        except AttributeError:
           try:
               username = str(bewertung.find('span', {'class': 'ghost-user ghost-qype-user'}).text)
           except AttributeError:
               try:
                   username = str(bewertung.find('span', {'class': 'ghost-user ghost-rk-user'}).text)
               except AttributeError:
                   username = 'kein Yelp-User'


        # Aufrufen der Methode um die gelesenen Daten in die Tabelle YELP_USER einzufügen
        store_user(username.strip(), anzahlbew.text.strip())

        # for-Schleife für jedes einzelne Bild innerhalb einer Bewertung
        pic = bewertung.find_all('a', {'class': {'biz-shim js-lightbox-media-link js-analytics-click'}})
        for pics in pic:
            pic = 'https://www.yelp.com' + pics.get('href')
            try:
                # Aufrufen der Methode um die Bild-URL in die Tabelle YELP_PIC einzufügen, falls vorhanden
                store_pic(pic.strip())
            except:
                pass


    # Falls eine weitere Seite mit Bewertungen gibt, wird die nächste Seite aufgerufen
    if soup.find("span",{"class": "pagination-label responsive-hidden-small pagination-links_anchor"}):
        link = soup.find("a",{"class": "u-decoration-none next pagination-links_anchor"})
        href = link.get("href")
        source_code = requests.get(href)
        plain_text = source_code.text
        new_soup = BeautifulSoup(plain_text, 'html.parser')

        # Aufrufen der Methode um die einzelnen Bewertungen aufzurufen
        loop_bewertungen(new_soup)

# Aufrufen der Methode um die Daten aus dem HTML-Dokument zu scrappen und in den MySQL-Server zu übertragen
try:
    find_object()
    print('Objektdaten wurden erfolgreich in die Datenbank gespeichert')
except:
    print('Objketdaten wurden nicht in die Datenbank gespeichert')
