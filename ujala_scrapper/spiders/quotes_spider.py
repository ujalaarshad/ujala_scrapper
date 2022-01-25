import scrapy
from scrapy import Request


class QuotesSpider(scrapy.Spider):
    name = 'quotes_spider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response):
        for quote_s in response.css('.tag-item')[:4]:
            url = quote_s.css('.tag-item > .tag::attr(href)').get()
            yield Request(url=response.urljoin(url), callback=self.parse_menu)

    def parse_menu(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        url = response.css('.next > a::attr(href)').get()
        yield Request(url=response.urljoin(url), callback=self.parse_menu)
