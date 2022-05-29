import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys


class ExampleSpider(scrapy.Spider):
    name = 'example'
    
    def start_requests(self):
        yield SeleniumRequest(
            url="https://duckduckgo.com",
            wait_time = 3,
            screenshot = True,
            callback = self.parse
        )
        
    def parse(self, response):
        # img = response.meta['screenshot']
        # with open('screenshot.png', 'wb') as f:
        #     f.write(img)
        
        driver = response.meta['driver']
        search_input = driver.find_element_by_xpath("//input[@id='search_form_inut_homepage]")
        search_input.send_keys('hello world')
        
        # driver.save_screenshot('after_filling_input.pnd')
        
        search_input.send_keys(Keys.ENTER)
        
        # driver.save_screenshot('enter.pnd')
        
        html = driver.page_source
        
        response_obj = Selector(text=html)
        
        links = response.xpath("//span[@class='result__extras__url']/a")
        for link in links:
            yield {
                'URL': link.xpath(".//@href").get()
            }
        
