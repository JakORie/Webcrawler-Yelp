# Webcrawler-Yelp
Webcrawler to extract data from Yelp

# Tables must be created before program can be ran
use yelp;

CREATE TABLE YELP_ADDRESS 
(Restaurant_id BIGINT(20) NOT NULL auto_increment, 
comp_name VARCHAR(30), 
street VARCHAR(30), 
postalcode VARCHAR(10), 
city VARCHAR(20), 
PRIMARY KEY(Restaurant_id));

CREATE TABLE YELP_REVIEWS
 (Review_id BIGINT(20) NOT NULL auto_increment, 
 Restaurant_id BIGINT(20),
 review VARCHAR(8000), 
 rating VARCHAR(10), 
 PRIMARY KEY(Review_id),
 FOREIGN KEY (Restaurant_id) REFERENCES YELP_ADDRESS(Restaurant_id));
