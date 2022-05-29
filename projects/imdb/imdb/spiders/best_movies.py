import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    # start_urls = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc',
                             headers={
            'User-Agent' : self.user_agent
        })
        
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class = 'lister-item-header']/a"), callback='parse_item', follow=True, process_request = 'set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[1]"))
    )
    
    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request
        

    def parse_item(self, response):
        print(response.url)
        yield {
            'title' : response.xpath("//div[@class='sc-94726ce4-1 iNShGo']/h1/text()").get(),
            'year' : response.xpath("//div[@class='sc-94726ce4-3 eSKKHi']/ul/li[1]/span/text()").get(),
            'duration' : "".join(response.xpath("//div[@class='sc-94726ce4-3 eSKKHi']/ul/li[3]/text()").extract()),
            'genre' : response.xpath("//div[@class='ipc-chip-list sc-16ede01-5 ggbGKe']/a/ul/li/text()").get(),
            'rating' : response.xpath("//div[@class = 'sc-7ab21ed2-2 kYEdvH']/span/text()").get(),
            'movie_url' : response.url
        }
