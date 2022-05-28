## Project 1 - worldometers I

```
mkdir projects
cd projects
scrapy startproject worldometers

cd worldometers
scrapy genspider countries https://www.worldometers.info/world-population/population-by-country/
```

In `countries.py`, change `start_urls = ['http://www.worldometers.info/']` to `start_urls = ['https://www.worldometers.info/world-population/population-by-country/']`.


```
scrapy shell # shows some available Scrapy objects.
fetch('https://www.worldometers.info/world-population/population-by-country/')
r = scrapy.Request(url = 'https://www.worldometers.info/world-population/population-by-country/')
fetch(r)
response.body
view(response)
```

Note that Scrapy will return the raw HTML markup without JS, so we need to disable JS. 'Command + Shift + I' -> 'Command + Shift + P' -> disable JavaScript.

XPath expressions & CSS Selectors to get the title.

```
title = response.xpath('//h1')
title
title = response.xpath('//h1/text()')
title
title.get()
```

```
title_css = response.css('h1::text')
title_css
title_css.get()
```

XPath expressions & CSS Selectors to get all the countries.

```
countries = response.xpath('//td/a/text()').getall()
countries 
```

```
countries_css = response.css('td a ::text').getall()
countries_css
```

Display the response

```
yield {
    'title': title,
    'country': country
}
```

Now I modified the `countries.py` and run `scrapy crawl countries` to get country names.

## Project 1 - worldometers II

```
cd projects/worldometers
scrapy crawl countries
```

Two ways to get absolute link: `absolute_url = f"https://www.worldometers.info{link}"` or `absolute_url = response.urljoin(link)`, and followed by `yield scrapy.Request(url=absolute_url)` to request.
Can also simply do `yield response.follow(url=link)`, where `link` is relative link.


By `yield response.follow(url=link, callback=self.parse_country)`, scrapy sends a request to each country link, then the response will be sent to `parse_country()` method.

Use xpath `(//table[@class = 'table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr` to select the first specific table of that class.

## Building dataset

`scrapy crawl countries -o population_dataset.json`

'option + shift + F' to format the json file

`scrapy crawl countries -o population_dataset.csv`

`scrapy crawl countries -o population_dataset.xml`

## Debugger

Write a debugger `runner.py`. Assign a break point at a function in spider 'countries.py'. Back to 'runner.py'. Debug -> Start debugging -> python file.