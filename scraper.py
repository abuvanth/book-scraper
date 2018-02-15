import urlparse
import scrapy

from scrapy.http import Request

class wbpublibnet(scrapy.Spider):
    name = "wbpublibnet"

    allowed_domains = ["dspace.wbpublibnet.gov.in:8080"]
    start_urls = ["dspace.wbpublibnet.gov.in:8080/jspui/"]

    def parse(self, response):
        for href in response.css('div.carousel-inner div div a::attr(href)').extract():
            yield Request(
                url=response.urljoin(href),
                callback=self.parse_article
            )

    def parse_article(self, response):
        for href in response.css('table.panel-body tr td a[href$=".pdf"]::attr(href)').extract():
            yield Request(
                url=response.urljoin(href),
                callback=self.save_pdf
            )

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
