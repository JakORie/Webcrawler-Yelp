# Webcrawler-Yelp
Webcrawler to extract data from Yelp

# Tables must be created before program can be ran
CREATE TABLE YELP_REVIEWS (id BIGINT(20) NOT NULL auto_increment, review VARCHAR(1000),
rating VARCHAR(10), PRIMARY KEY(id));

CREATE TABLE YELP_ADDRESS (id BIGINT(20) NOT NULL auto_increment, comp_name VARCHAR(30),
street VARCHAR(30), postalcode VARCHAR(10), city VARCHAR(20),  PRIMARY KEY(id));
