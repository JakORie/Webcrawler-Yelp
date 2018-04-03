from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.yelp.com/search?find_desc=burger&find_loc=München%2C+Bavaria%2C+Germany&ns=1').text
soup = BeautifulSoup(source,'html.parser')




#saemtliche Tags der Webseite werden in Links gespeichert
links = soup.find_all("a")


#Methode um den Quelltext in strukturierter Form auszugeben
#print(soup.prettify())








#returns a list of all genres
# genre = soup.find_all("span", {"class": "category-str-list"})
# for item in genre:
#     print(item.get_text())


#retunrs a list of all the restaurant names
#die text bzw. get_text() methode gibt nur den text aus und entfernt saemtliche tags
#companyName = soup.find_all("a", {"class": "biz-name"})
#for item in companyName:
#    print(item.text)


# gibt saemtliche Adressen der Restaurants aus
# ToDo weitere Aufteilung nach PLZ, Straße, etc
#adress = soup.find_all("address")
#for item in adress:
#   print(item.text)


#gibt eine einzelne Adresse aus, bzw. die erste
#single_address = soup.find_all("address")[1].text
#print(single_address)


adress = soup.find_all("address")
#for item in adress:
   #print(item.text)


phone = soup.find_all("span", {"class": "biz-phone"})
for item in phone:
    print(item.text)
#print(phone)
