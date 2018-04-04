from bs4 import BeautifulSoup
import requests
import pymysql.cursors

# Yelp connection
html = requests.get('https://www.yelp.com/search?find_desc=burger&find_loc=München%2C+Bavaria%2C+Germany&ns=1').text
soup = BeautifulSoup(html, 'html.parser')

#finds all Companynames on the searchpage at yelp
companyList = soup.find_all("a", {"class": "biz-name"})


#creates a connection to the mysql-server
connection = pymysql.connect(host='localhost',
                             user='root',
                             db='sys',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


try:
    with connection.cursor() as cursor:
        for company in companyList:
            name = company.text.strip()
            sql = "INSERT INTO `RestaurantsYelp` (`CompName`) VALUES (%s)"
            cursor.execute(sql, (name))
    connection.commit()
finally:
    connection.close()