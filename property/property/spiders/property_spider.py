import scrapy
from scrapy_splash import SplashRequest


class SVNIndividualPageSpider(scrapy.Spider):
    name = "svn"

    start_urls = [
        "https://svn.com/find-properties/?propertyId=wagenburgwest",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse_buildout_iframe(self, response):
        yield {
            'name': response.css('.header-text h1::text').extract_first(),
            'address': response.css('.text-muted::text').extract(),
        }

    def parse(self, response):
        url = response.css("#buildout iframe::attr(src)").extract_first()

        yield(SplashRequest(url, callback=self.parse_buildout_iframe))
