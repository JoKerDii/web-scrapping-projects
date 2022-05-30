## Project Login

Target website: https://openlibrary.org/account/login

Go to login page and open developer tool -> Network -> clear all requests and click on login button -> open the first request 'Login', have a look at the form data

```
scrapy startproject book_login
cd book_login
scrapy genspider openlibrary_login openlibrary.org/account/login
```

After modifying openlibrary_login.py, run

```
scrapy crawl openlibrary_login
```

Note that if the form requires JavaScript, we cannot use the `FormRequest` class. Instead, we have to use `SplashFormRequest`, which has the same methods as in the `FormRequest` and takes the same arguments. Also, we need to add Splash to the settings.py, and need Splash to run on the background.


Example:

```
# Splash should be running on the background
 
import scrapy
from scrapy_splash import SplashRequest, SplashFormRequest
 
class QuotesLoginSpider(scrapy.Spider):
    name = 'quotes_login'
    allowed_domains = ['quotes.toscrape.com']
    
    script = '''
        function main(splash, args)
          assert(splash:go(args.url))
          assert(splash:wait(0.5))
          return splash:html()
        end
    '''
    
    def start_requests(self):
        yield SplashRequest(
            url='https://quotes.toscrape.com/login',
            endpoint='execute',
            args = {
                'lua_source': self.script
            },
            callback=self.parse
        )
 
    def parse(self, response):
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        yield SplashFormRequest.from_response(
            response,
            formxpath='//form',
            formdata={
                'csrf_token': csrf_token,
                'username': 'admin',
                'password': 'admin'
            },
            callback=self.after_login
        )
    
    def after_login(self, response):
        if response.xpath("//a[@href='/logout']/text()").get():
            print('logged in')


```