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


## Basic steps to web-scrapping

Start a project

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

Note that Scrapy cannot interpret JavaScript. Scrapy will return the raw HTML markup without JS, so we need to disable JS. 'Command + Shift + I' -> 'Command + Shift + P' -> disable JavaScript.

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

## Splash

JS requires engine to be executed. Chrome has V8 engine. Firefox has Spider Monkey. Safari has Apple Web kit (same engine used by Splash). Microsoft Edge has Shakra. For scrapping those websites on which we really need JavaScript, we can use Splash or Selenium.

To download Splash, we first download Docker and run

```
docker pull scrapinghub/splash
```

To start Splash at the first time, we run

```
docker run -it -p 8050:8050 scrapinghub/splash 
```

Then, open 'http://0.0.0.0:8050' on browser to start Splash.

To start the Splash next time, we can use docker desktop, go dashboard, and click on start button of the specific app.

To render the target website: https://duckduckgo.com, on http://0.0.0.0:8050 do

```
function main(splash, args)
  url = args.url
  assert(splash:go(url))
  assert(spalsh:wait(1))
  return {
      splash:png(),
      splash:html()
  }
end
```

We can use `select()` or `select_all()` to select elements. When searching results, sometimes we need to wait a little bit more seconds to render the webpage.


We can click the button by either

```
btn = assert(splash:select("#search_button_homepage"))
btn:mouse_click()
```
or

```
input_box:send_keys("<Enter>")
```

The full code is 

```
function main(splash, args)

  url = args.url
  assert(splash:go(url))
  assert(splash:wait(1))
  
  input_box = assert(splash:select("#search_form_input_homepage"))
  input_box:focus()
  input_box:send_text("my user agent")
  assert(splash:wait(0.5))
  
  --[[
  btn = assert(splash:select("#search_button_homepage"))
  btn:mouse_click()
  --]]
  input_box:send_keys("my user agent")
  assert(splash:wait(5))

  return {
      splash:png(),
      splash:html()
  }
end
```

To overwrite request headers (set user agent) we can do

```
splash:set_user_agent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")
```
or 

```
header = {
    ['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
}
splash:set_custom_headers(headers)
```
or 

```
splash:on_request(function(request)
    request:set_head('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36')
end)
```

## Selenium

```
pip install scrapy_selenium
```

## Store data in MongoDB

```
pip install pymongo dnspython
```
Modify `pipelines.py`, and `settings.py` (change to MongodbPipeline).

Create an account on MongoDB cloud. Create a new cluster. Config databased access and network access (0.0.0.0/0). 

Connect to the cluster. Connect -> connect to your application -> config the language -> copy the application code and paste in 'pipelines.py' -> replace <password> with the actual password.

Run `scrapy crawl best_moviews` and check the collection on MongoDB. The data are store in it.


## Store data in SQLite3

Note that sqlite3 is already included in python standard library so we don't need to install it.

Modify `pipelines.py` and `settings.py` (change to SQLlitePipeline).

Run `scrapy crawl best_moviews` then we get a `imdb.db` file.

Install SQLits extension in vscode. Right clide and open the `imdb.db`.
