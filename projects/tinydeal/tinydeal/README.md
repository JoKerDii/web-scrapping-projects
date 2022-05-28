

##  Project 2 TinyDeal

target: https://web.archive.org/web/20190225123327/https://www.tinydeal.com.hk/specials.html

```
scrapy startproject tinydeal 
scrapy genspider special_offers web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html
```

After modifying parse function in special_offers.py, run

```
scrapy crawl special_offers -o dataset.json
```

'option + shift + F' to format the json file. 

Note that we have unicode characters, which is an encoding issue. Scrapy by default does not use the UTF 8 encoding for JSON files. We can easily fix this by adding `FEED_EXPORT_ENCODING = 'utf-8'` in settings.py.

To get info from multiple pages, everytime we check whether there is a next page, if yes extract the url of the next page.


To check available scrapy objects, run

```
scrapy shell "https://web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html"
```

The following two commands are the same to output request headers:
```
request.headers
response.request.headers
```

To see the request header sent by the browser we can user developer tools - Network. Note that different browser has different user-agent.

If we want to override multiple request headers, there are two approaches: First, by using DEFAULT_REQUEST_HEADERS:

```
DEFAULT_REQUEST_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
}
```

Second, by defining a start-requests() function and deleting `start_urls` variable.

```
def start_requests(self):
    yield scrapy.Request(url = 'https://www.tinydeal.com.hk/specials.html', callback=self.parse, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
    })
```
