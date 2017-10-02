# NC Legislature Bill Scrapy

Use this Scrapy to obtain bill data from the [NC Legislature website](http://www.ncleg.net).

The scrapy extracts each bill's data into an object. Use [scrapy](https://github.com/scrapy/scrapy) command to out put a JSON list of bill objects.

## Technology Stack
* Python 3
* PostgreSQL
 * _[Scrapy](https://github.com/scrapy/scrapy)_: Web Scraping Library
 * _[psycopg2](http://initd.org/psycopg/)_: Postgres Connector

## Prerequisites
1. Python 3
1. Environment variables stored for:
  * AWS Access Key (`S3_ACCESS_KEY`)
  * AWS Secret Key (`S3_SECRET_KEY`)
  * AWS S3 Bucket (`S3_BUCKET_NAME`)
1. psycopg2 intalled
  * `pip install psycopg2`
1. tinys3 installed 
  * `pip install tinys3`

## Running the Scraper
1. Requires python3
1. Install Scrapy, pip for example: `pip install scrapy`
1. Navigate into repo
1. Tell Scrapy to crawl "bills" `scrapy crawl bills -o <filename>.<ext>` (<filename>.<ext> is a JSON file that will be created at runtime and will contain the extracted data.)


