import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

class CoinSpider(scrapy.Spider):
    name = 'coin_selenium'
    allowed_domains = ['web.archive.org']
    start_urls = ['https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/']
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        s = Service('./chromedriver')
        driver = webdriver.Chrome(service=s, options=options)
        driver.set_window_size(1920, 1080)
        driver.get("https://duckduckgo.com")
        
        rur_tab = driver.find_elements_by_class_name("filterPanelItem___2z5Gb")
        rur_tab[4].click()
        
        self.html = driver.page_source
        driver.close()
        
    def parse(self, response):
        resp = Selector(text = self.html)
        for currency in resp.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield {
                'currency pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24h)': currency.xpath(".//div[2]/span/text()").get()
            }
