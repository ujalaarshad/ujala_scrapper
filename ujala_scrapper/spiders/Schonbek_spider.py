import scrapy
from scrapy import Request


class Quotesschonbekspider(scrapy.Spider):
    name = 'quotes_schonbekspider'
    allowed_domains = ['www.schonbek.com']
    start_urls = ['https://www.schonbek.com/schonbek-families']

    def parse(self, response):
        for url in response.css('[data-menu="menu-908"] a::attr(href)').getall()[1:]:
            yield Request(url=url, callback=self.parse_listing)

    def parse_listing(self, response):
        url_all = response.urljoin('?&product_list_limit=all')
        yield Request(url=url_all, callback=self.parse_listing)

    def parse_listing(self, response):
        for url_product in response.css('.product-item-info a::attr(href)').getall():
            yield Request(url=url_product, callback=self.parse_product)

    def parse_product(self, response):
        yield {
            'core-sku': response.css('.prod-name::text').get(),
            'page-title': response.css('.base::text').get().strip(),
            'specsheet': response.css('.download-btn a::attr(href)').get()
        }






