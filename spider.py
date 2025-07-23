import scrapy
from scrapy.crawler import CrawlerProcess

class HelloSpider(scrapy.Spider):
    name = "hello"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]
    custom_settings = {
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'result.csv',
        'FEED_EXPORT_ENCODING' : 'utf-8',
    }

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                "text" : quote.css('span.text::text').get(),
                "author" : quote.css('small.author::text').get(),
                "tags": quote.css('div.tags a.tag::text').getall(),
                }

        yield from response.follow_all(css='ul.pager a', callback=self.parse)


process = CrawlerProcess()
process.crawl(HelloSpider)
process.start()
