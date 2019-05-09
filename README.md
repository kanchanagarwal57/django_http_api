# Django HTTP API

## Requirements

* Python3 using Django
* MySQL

```
$pip install -r requirements.txt

```
## Usage

1) Load sample_data.csv to MySQL database.
2) Create a config.ini file with following credentials:

```
[DJANGO]
SECRET_KEY='<secret_key>'

[MYSQL]
DB_HOST=localhost
DB_PORT=3306
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_TABLE=<table_name>
```
3) Initiate the django server
```
$python manage.py runserver
```

## Objectives
Expose the sample dataset through a HTTP API endpoint, which is capable of filtering, grouping and sorting. Dataset represents performance metrics (impressions, clicks, installs, spend, revenue) for a given date, advertising channel, country and operating system. It is expected to be stored and processed in a relational database of your choice.

Sample dataset: sample_data.csv

Client of this API would be able to:
1) filter by time range (date_from / date_to is enough), channels, countries, operating systems
2) group by one or more columns: date, channel, country, operating system
2) sort by any column in ascending or descending order

Client can use filtering, grouping, sorting at the same time.

Common API use cases:
1) Show the number of impressions and clicks that occurred till the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order. Hint:
```
=> select channel, country, sum(impressions) as impressions, sum(clicks) as clicks from sampledataset where date <= '2017-06-01' group by channel, country order by clicks desc;
     channel      | country | impressions | clicks
------------------+---------+-------------+--------
 adcolony         | US      |      532608 |  13089
 apple_search_ads | US      |      369993 |  11457
 vungle           | GB      |      266470 |   9430
 vungle           | US      |      266976 |   7937
 ...
```

This can be achieved by the following url:
http://127.0.0.1:8000/api/?date_to=2017-06-01&group_by=channel&group_by=country&sum_on=impressions&sum_on=clicks&sort_by=clicks&order_type=DESC

2) Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.

This can be achieved by the following url:
http://127.0.0.1:8000/api/?date_from=2017-05-01&date_to=2017-05-31&os=iOS&group_by=date&sum_on=installs&sort_by=date&order_type=ASC

3) Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.

This can be achieved by the following url:
http://127.0.0.1:8000/api/?date_from=2017-06-01&date_to=2017-06-01&country=US&group_by=os&sum_on=revenue&sort_by=revenue&order_type=DESC

4) CPI (cost per install) metric added, i.e., cpi = spend / installs.
Use case: CPI values for Canada (CA) broken down by channel ordered by CPI in descending order.

This can be achieved by the following url:
http://127.0.0.1:8000/api/?country=CA&group_by=channel&sort_by=CPI&order_type=DESC

