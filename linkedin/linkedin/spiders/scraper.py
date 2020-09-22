import scrapy
from scrapy.crawler import CrawlerProcess

class TestScrape(scrapy.Spider):
    
    name = "test_spider"

    def start_requests ( self ): #tells which sites to scrape and where to send info to be parsed. Needs to be called start_requests
        urls = ['https://www.linkedin.com/company/jubaili-bros/']
        for url in urls:
            yield scrapy.Request( url = url, callback = self.parse )

    def parse( self, response ):
        filename = 'test.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)