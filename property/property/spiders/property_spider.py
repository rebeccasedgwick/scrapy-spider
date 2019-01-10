import scrapy
from scrapy_splash import SplashRequest
from datetime import datetime


class SVNIndividualPageSpider(scrapy.Spider):
    name = 'svn'
    start_urls = ['https://svn.com/find-properties/?propertyId=wagenburgwest']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        iframe_url = response.css('#buildout iframe::attr(src)').extract_first()
        orig_url = response.url
        yield SplashRequest(url=iframe_url, callback=self.parse_buildout_iframe, meta={'orig_url': orig_url})

    def parse_buildout_iframe(self, response):
        contacts_data = []
        items = ["1", "2", "3"]
        for i in items:
            scope = f'div:nth-child({i}) > table > tbody > tr > td.js-broker-details'
            contacts_data.append(
                {
                    'name': response.css(f'{scope} > strong > a::text').extract_first(),
                    'job_title': response.css(f'{scope} > div:nth-child(2) > small::text').extract_first(),
                    'email': response.css(f'{scope} > div.js-broker-contact-info > a::text').extract_first(),
                    'phone_main': response.css(f'{scope} > div.js-broker-contact-info > div:nth-child(2) > a::text').extract_first(),
                    'phone_office': response.css(f'{scope} > div.js-broker-contact-info > div:nth-child(3) > a::text').extract_first(),
                    'fax': response.css(f'{scope} > div.js-broker-contact-info > div:nth-child(4)::text').extract_first(),
                },
            )

        yield {
            'url': response.meta['orig_url'],
            'scraped_at': datetime.now(),
            'property_name': response.css('.header-text h1::text').extract_first(),
            'address': response.css('.text-muted::text').extract(),
            'price': response.css('tr:nth-child(1) > td:nth-child(2)::text').extract_first(),
            'property-type': response.css('tr:nth-child(2) > td:nth-child(2)::text').extract_first(),
            'size': response.css('tr:nth-child(3) > td:nth-child(2)::text').extract_first(),
            'description': response.css('.js-description-content::text').extract_first(),
            'highlghts': [
                response.css('ul > div > div:nth-child(1) > li:nth-child(1)::text').extract_first(),
                response.css('ul > div > div:nth-child(1) > li:nth-child(2)::text').extract_first(),
                response.css('ul > div > div:nth-child(2) > li:nth-child(1)::text').extract_first(),
                ],
            'location': response.css('.js-location-content::text').extract_first(),
            'contacts': contacts_data
        }
