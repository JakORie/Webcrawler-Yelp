import requests
from bs4 import BeautifulSoup

#Inputparameter -> Insert Searchtext in console
searchText = input('Suchtext eingeben:')

#Manipulate URL with inputparameter
url = "https://www.yelp.com/search?find_desc="+searchText+"&find_loc=M%C3%BCnchen%2C+Bayern&ns=1"
r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")

# print all title of the business presented in search page.
# Limits the result of find_all to 1
# links = soup.find_all("a", {"class": "biz-name"}, limit=1)
# for link in links:
#     print(link.string)

# find() is equivalent to find_all(limit=1)
# links = soup.find("a", {"class": "biz-name"})
# print(links.string)

#Gibt die Bewertung aus z.B.€€
links = soup.find("span", {"class": "business-attribute price-range"})
print(links.string.string)
