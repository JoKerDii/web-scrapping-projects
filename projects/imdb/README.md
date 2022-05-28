
## Project 3 - IMDB crawl spider

Create project and spider

```
scrapy startproject imdb
scrapy genspider -t crawl best_movies imdb.com
```

Note that there is a `rules` tuple, which must contain at least one Rule object. It is used to tell the CrawlSpider what are the links we want to follow. LinkExrtactor is used to specify the links that you want to extract or not to extract. We can do with xpath or css (Notice that we do not use `//a[@class='active']/@href`, because the LinkExtractor object will automatically search for the href attribute.)

```
rules = (
    Rule(LinkExtractor(restrict_xpaths=("//a[@class='active']"), callback = 'parse_item', follow = True))
)
```


link: https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc

Open developer tool, command + F to search `//h3[@class = 'lister-item-header']/a` and get 50 results.

Run the following to get all the movies and links.

```
scrapy crawl best_movies
```

If there are unexpected space around the string, we can do the following to remove space

```
response.xpath("normalize-space((//time)[1]/text())").get()
```

If we want to concatenate getall() results, we can do the following

```
"".join(response.xpath("//div[@class='sc-94726ce4-3 eSKKHi']/ul/li[3]/text()").extract())
```

To scrape all movies, we need to get other pages' links first.

Spoofing often allows access to a site's content where the site's web server is configured to block browsers that do not send referer headers. To spoof request headers, google search my user agent and got 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'.