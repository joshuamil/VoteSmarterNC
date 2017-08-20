# NC Legislature Bill scrapy

Use this scrapy to obtain bill data from the [NC Legislature website](http://www.ncleg.net).

The scrapy extracts each bill's data into an object. Use [scrapy](https://github.com/scrapy/scrapy) command to out put a JSON list of bill objects.

## How to run

1. Requires python3
1. Install scrapy, pip for example: `pip install scrapy`
1. Navigate into repo
1. Tell scrapy to crawl "bills" `scrapy crawl bills -o <filename>.<ext>`
