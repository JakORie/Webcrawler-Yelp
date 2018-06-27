CREATE database yelp;

CREATE TABLE YELP_ADDRESS 
(Restaurant_id BIGINT(20) NOT NULL auto_increment, 
comp_name VARCHAR(30), 
street VARCHAR(30), 
postalcode VARCHAR(10), 
city VARCHAR(20), 
PRIMARY KEY(Restaurant_id), 
rating VARCHAR(20), 
segment VARCHAR(20), 
reviews varchar(60));


CREATE TABLE YELP_REVIEWS 
(Review_id BIGINT(20) NOT NULL auto_increment, 
Restaurant_id BIGINT(20), 
review VARCHAR(8000), 
rating VARCHAR(10), 
PRIMARY KEY(Review_id), 
FOREIGN KEY (Restaurant_id) REFERENCES YELP_ADDRESS(Restaurant_id));


CREATE TABLE YELP_PIC 
(pic_id BIGINT(20) NOT NULL auto_increment, 
Review_id BIGINT(20), 
pic_url VARCHAR(150), 
PRIMARY KEY(pic_id), 
FOREIGN KEY (Review_id) REFERENCES YELP_REVIEWS(Review_id));


CREATE TABLE YELP_USER
(user_id BIGINT(20) NOT NULL auto_increment, 
Review_id BIGINT(20), 
name VARCHAR(30), 
reviews VARCHAR(20), 
PRIMARY KEY(user_id), 
FOREIGN KEY (Review_id) REFERENCES YELP_REVIEWS(Review_id));
