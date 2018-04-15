CREATE DATABASE yelp;
USE yelp;

CREATE TABLE YELP_RESTAURANT
(Restaurant_id BIGINT(20) NOT NULL auto_increment, 
name VARCHAR(30), 
rating VARCHAR(20),
reviews VARCHAR(20),
segment VARCHAR(20),
street VARCHAR(30), 
postalcode VARCHAR(10), 
city VARCHAR(20),
PRIMARY KEY (Restaurant_id));

CREATE TABLE YELP_USER
(User_id BIGINT(20) NOT NULL auto_increment,
name VARCHAR(30),
reviews VARCHAR(20),
PRIMARY KEY (User_id));

CREATE TABLE YELP_REVIEWS 
(Review_id BIGINT(20) NOT NULL auto_increment,
Restaurant_id BIGINT(20),
User_id BIGINT(20),
rating VARCHAR(10),
review VARCHAR(1000), 
PRIMARY KEY (Review_id),
FOREIGN KEY (Restaurant_id) REFERENCES YELP_RESTAURANT(Restaurant_id));

CREATE TABLE YELP_PIC 
(pic_id BIGINT(20) NOT NULL auto_increment,
Review_id BIGINT(20),
pic_url VARCHAR(150),
PRIMARY KEY (pic_id),
FOREIGN KEY (Review_id) REFERENCES YELP_REVIEWS(Review_id));
