# Scrapping Notes and Logs

## Using Scrapy

`scrapy bench`: Run quick benchmark test.
`scrapy fetch <URL>`: Fetch a URL using the Scrapy downloader.
`scrapy genspider`: Generate new spider using pre-defined templates.

## CSS Selectors

[CSS playground](https://try.jsoup.org/)

Use `#` to query tags with id. Use `.` to query tags with class. Use `.A.B` to query double classes `class="A B"`.
Use square bracket to query tags with attributes, e.g. use `[data-identifier=7]` or `li[data-identifier=7]` to query `<li data-identifier="7">` tag.
Select tags with specific attributes: `a[href^='https']` for `<a href="https://www.google.com">Google</a>`, `a[href$='fr']` for `<a href="https://www.google.fr">Google France</a>`.
Select nested tags: `div.intro p, span#location` for `<p>` and `<span>` in `<div class = "intro">`.
Select nested tags: `div.intro > p` for all tages within `<div class="intro">`.
Select a particular tag immediately after a tag: `div.intro + p` for a specific `<p>` immediately after `<div class="intro">`.
Select the specific number of tag: `li:nth-child(1)` to get the first `<li>`, `li:nth-child(3)` to get the third `<li>`, `li:nth-child(odd)` to get the odd number of `<li>`.

## XPath Selectors

[XPath playground](https://scrapinghub.github.io/xpath-playground/).


Select all `<p>` within the `<div class="intro">` and `<div class="outro">`: `//div[@class="intro" or @class="outro"]/p`. Select text only: `//div[@class="intro" or @class="outro"]/p/text()`.
Select specific `<a>` with href starting with 'https': `//a[start-with(@href,"https")]`.
Select specific `<a>` with href ending with 'fr': `//a[end-with(@href,"fr")]`.
Select specific `<a>` with href containing 'google': `//a[contains(@href,"google")]`.
Select specific `<a>` with text containing 'google': `//a[contains(text(),"France")]`. (note that this is case sensitive)
Select the first `<li>` in `<ul>`: `//ul[@id="items"]/li[1]`. Select the first and the fourth `<li>` in `<ul>`: `//ul[@id="items"]/li[position() = 1 or position() = 4]`. If the fourth one is the last: `//ul[@id="items"]/li[position() = 1 or last() = 4]`.


Select the immediate parent tag `<div>` of `<p id="unique">`: `//p[@id='unique']/parent::div`.
Select the any immediate parent tag of `<p id="unique">`: `//p[@id='unique']/parent::node()`.
Select all parent tags of `<p id="unique">`(p is excluded): `//p[@id='unique']/ancestor::node()`.
Select all parent tags of `<p id="unique">`(p is included): `//p[@id='unique']/ancestor-or-self::node()`.
Select tag `<h1>` that precedes `<p id="unique">` (not parents): `//p[@id='unique']/preceding::h1`.
Select all tags that precede `<p id="unique">` (not parents): `//p[@id='unique']/preceding::node()`.
Select all tags that are siblings of `<p id="unique">`: `//p[@id='unique']/preceding-sibling::node()`.


Select the immediate child tag `<p>` of `<div class="intro">`: `//div[@class='intro']/child::p`.
Select the any immediate child tag of `<div class="intro">`: `//div[@class='unique']/child::node()`.
Select all tags listed after `<div class="intro">`: `//div[@class='unique']/following::node()`.
Select all tags listed after `<div class="intro">` and share the same parent `<body>`: `//div[@class='unique']/following-sibling::node()`.
Selected all children tags inside `<div class="intro">`: `//div[@class='unique']/descendant::node()`.


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

Note that Scrapy will return the raw HTML markup without JS, so we need to disable JS. `Command + Shift + I` -> `Command + Shift + P` -> disable JavaScript.

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

Now I modified the `countries.py` and run `scrapy crawl countries` to get country names.

## Project 1 - worldometers II

```
cd projects/worldometers
scrapy crawl countries
```

Two ways to get absolute link: `absolute_url = f"https://www.worldometers.info{link}"` or `absolute_url = response.urljoin(link)`, and followed by `yield scrapy.Request(url=absolute_url)` to request.
Can also simply do `yield scrapy.follow(url=link)`, where `link` is relative link.
