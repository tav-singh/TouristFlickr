/*DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (   id INTEGER PRIMARY KEY AUTOINCREMENT,   username TEXT UNIQUE NOT NULL,   password TEXT NOT NULL );
CREATE TABLE post (   id INTEGER PRIMARY KEY AUTOINCREMENT,   author_id INTEGER NOT NULL,   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,   title TEXT NOT NULL,   body TEXT NOT NULL,   FOREIGN KEY (author_id) REFERENCES user (id) );
*/
/*

insert into living_expense(city, country, year_2016, cost_living_index_2016, groceries_index_2016, restaurant_price_index_2016
 year_2017, cost_living_index_2017, groceries_index_2017, restaurant_price_index_2017, year_2018, cost_living_index_2018,
 groceries_index_2018, restaurant_price_index_2018) values('New York', 'United States', 2016, 1140.68, )
CREATE TABLE living_expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city VARCHAR(30),
    country VARCHAR(30),
    cost_living_index DECIMAL (10,2),
    groceries_index DECIMAL (10,2),
    restaurant_price_index DECIMAL (10,2),
    year INTEGER
);



select l3.city, l3.country, l3.year as year_2016, l3.cost_living_index as cost_living_index_2016, l3.groceries_index as
groceries_index_2016, l3.restaurant_price_index as restaurant_price_index_2016,
l1.year_2017, l1.cost_living_index_2017, l1.groceries_index_2017, l1.restaurant_price_index_2017,
l1.year_2018, l1.cost_living_index_2018, l1.groceries_index_2018, l1.restaurant_price_index_2018,
from (select l.city, l.country, l.year as year_2017, l.cost_living_index as cost_living_index_2017,
l.groceries_index as groceries_index_2017, l.restaurant_price_index as restaurant_price_index_2017, l2.year as year2018,
l2.cost_living_index as cost_living_index_2018, l2.groceries_index as groceries_index_2018, l2.restaurant_price_index as
 restaurant_price_index_2018, from living_expense l inner join living_expense l2
on l.city = l2.city where l.year != l2.year order by l.city) as l1
inner join living_expense l3 on l3.city = l1.city where l1.year_2017 != l3.year and l1.year_2018 != l3.year
group by l1.city order by l1.city limit 10;


select l3.city, l3.country, l3.year as year_2016, l3.cost_living_index as cost_living_index_2016, l3.groceries_index as groceries_index_2016, l3.restaurant_price_index as restaurant_price_index_2016, l1.year_2017, l1.cost_living_index_2017, l1.groceries_index_2017, l1.restaurant_price_index_2017, l1.year_2018, l1.cost_living_index_2018, l1.groceries_index_2018, l1.restaurant_price_index_2018 from (select l.city, l.country, l.year as year_2017, l.cost_living_index as cost_living_index_2017, l.groceries_index as groceries_index_2017, l.restaurant_price_index as restaurant_price_index_2017, l2.year as year2018, l2.cost_living_index as cost_living_index_2018, l2.groceries_index as groceries_index_2018, l2.restaurant_price_index as restaurant_price_index_2018, from living_expense l inner join living_expense l2 on l.city = l2.city where l.year != l2.year order by l.city) as l1 inner join living_expense l3 on l3.city = l1.city where l1.year_2017 != l3.year and l1.year_2018 != l3.year group by l1.city order by l1.city limit 10;
create table costs_combined (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city VARCHAR(30),
    country VARCHAR(30),
    year_2016 INTEGER,
    cost_living_index_2016 DECIMAL (10,2),
    groceries_index_2016 DECIMAL (10,2),
    restaurant_price_index_2016 DECIMAL (10,2),
    year_2017 INTEGER,
    cost_living_index_2017 DECIMAL (10,2),
    groceries_index_2017 DECIMAL (10,2),
    restaurant_price_index_2017 DECIMAL (10,2),
    year_2018 INTEGER,
    cost_living_index_2018 DECIMAL (10,2),
    groceries_index_2018 DECIMAL (10,2),
    restaurant_price_index_2018 DECIMAL (10,2)
)
*/
/*insert into costs_combined (city, country, year_2016, cost_living_index_2016, groceries_index_2016, restaurant_price_index_2016, year_2017, cost_living_index_2017, groceries_index_2017, restaurant_price_index_2017, year_2018, cost_living_index_2018, groceries_index_2018, restaurant_price_index_2018) select * from (select l3.city, l3.country, l3.year as year_2016, l3.cost_living_index as cost_living_index_2016, l3.groceries_index as groceries_index_2016, l3.restaurant_price_index as restaurant_price_index_2016, l1.year_2017, l1.cost_living_index_2017, l1.groceries_index_2017, l1.restaurant_price_index_2017, l1.year_2018, l1.cost_living_index_2018, l1.groceries_index_2018, l1.restaurant_price_index_2018 from (select l.city, l.country, l.year as year_2017, l.cost_living_index as cost_living_index_2017, l.groceries_index as groceries_index_2017, l.restaurant_price_index as restaurant_price_index_2017, l2.year as year_2018, l2.cost_living_index as cost_living_index_2018, l2.groceries_index as groceries_index_2018, l2.restaurant_price_index as restaurant_price_index_2018 from living_expense l inner join living_expense l2 on l.city = l2.city where l.year != l2.year order by l.city) as l1 inner join living_expense l3 on l3.city = l1.city where l1.year_2017 != l3.year and l1.year_2018 != l3.year group by l1.city order by l1.city limit 10);
select * from living_expense l join living_expense l2 where l.city = l2.city  and l.year != l2.year order by l.city

CREATE TABLE safety (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country VARCHAR(30),
    safety_index DECIMAL (8,4)
);
*/

CREATE TABLE photos_nus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    comments INTEGER,
    views INTEGER,
    popularity INTEGER,
    latitude DECIMAL (10, 6) ,
    longitude DECIMAL (10, 6),
    city VARCHAR(30),
    country VARCHAR(30),
    url TEXT,
    cdn_url TEXT,
    class_tag TEXT
);

CREATE TABLE traffic (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city VARCHAR(30),
    country VARCHAR(30),
    traffic_index DECIMAL (10,2),
    time_index DECIMAL (10,2),
    inefficiency_index DECIMAL (10,2),
    year INTEGER
);

CREATE TABLE pollution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city VARCHAR(30),
    country VARCHAR(30),
    pollution_index DECIMAL (10,2),
    year INTEGER
);

CREATE TABLE crime (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city VARCHAR(30),
    country VARCHAR(30),
    crime_index DECIMAL (10, 2),
    safety_index DECIMAL(10, 2),
    year INTEGER
);

CREATE TABLE cost (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city VARCHAR(30),
    country VARCHAR(30),
    cost_living_index DECIMAL (10,2),
    groceries_index DECIMAL (10,2),
    restaurant_price_index DECIMAL (10,2),
    year INTEGER
);

/*
ALTER TABLE living_expense drop column cost;
ALTER TABLE living_expense add cost_index DECIMAL (10,2);
ALTER TABLE living_expense add groceries_index DECIMAL (10,2);
ALTER TABLE living_expense add pp_index DECIMAL (10,2);*/

/* VIEWS and sql

select count(*) from (select city, country, latitude, longitude, sum(popularity) as popularity, group_concat(url) as url,
group_concat(cdn_url) as cdn_url, group_concat(class_tag) as class_tag from
(select * from photos_nus where class_tag like '%beach%') group by city, country) as p inner join
(select city, country, group_concat(groceries_index) as groceries_index, group_concat(restaurant_price_index) as
restaurant_price_index, group_concat(cost_living_index) as cost_living_index, group_concat(year) as year from cost
group by city, country) c on p.city = c.city where p.country = c.country order by p.popularity desc limit 2


select * from (select city, country, latitude, longitude, sum(popularity) as popularity, group_concat(url) as url,
group_concat(cdn_url) as cdn_url, group_concat(class_tag) as class_tag from
(select * from photos_nus where class_tag like '%beach%') group by city, country) as p inner join
[cost_view] c on p.city = c.city where p.country = c.country order by p.popularity desc limit 2

select city, country, latitude, longitude, sum(popularity) as popularity, group_concat(url) as url, group_concat(cdn_url) as cdn_url, group_concat(class_tag) as class_tag from photos_nus group by city, country as p inner join cost on p.city = cost.city, p.country = cost.country order by p.popularity desc limit 2

create view [crime_view] as
select city, country, group_concat(crime_index) as crime_index, group_concat(safety_index) as safety_index, group_concat(year)
as year from crime group by city, country


select city, country, latitude, longitude, sum(popularity) as popularity, group_concat(url) as url, group_concat(cdn_url) as cdn_url, group_concat(class_tag) as class_tag from (select * from photos_nus where class_tag like '%beach%') group by city, country

*/