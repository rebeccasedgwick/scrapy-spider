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
        items = ['1', '2', '3']
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


class AmRealIndividualPageSpider(scrapy.Spider):
    name = 'amreal'
    start_urls = ['http://www.amreal.com/property.htm?propertyId=419174-sale']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        iframe_url = response.css('#buildout iframe::attr(src)').extract_first()
        orig_url = response.url
        yield SplashRequest(url=iframe_url, callback=self.parse_buildout_iframe, meta={'orig_url': orig_url})

    def parse_buildout_iframe(self, response):
        description_text = []
        items = ['2', '3', '4', '5', '6', '7', '9']
        for i in items:
            scope = f'.col-md-9.pr-3-lg > div:nth-child(3) > p:nth-child({i})'
            description_text.append(response.css(f'{scope}::text').extract_first())

        yield {
            'url': response.meta['orig_url'],
            'scraped_at': datetime.now(),
            'property_name': response.css('.plugin-header-title::text').extract_first(),
            'address': response.css('.plugin-header-address::text').extract_first(),
            'price': response.css('tr:nth-child(1) > td::text').extract_first(),
            'property-type': response.css('tr:nth-child(2) > td::text').extract_first(),
            'size': response.css('div:nth-child(2) > table > tbody > tr > td::text').extract_first(),
            'description': description_text,
            'latitude': response.css('.map-container.w-100::attr(data-latitude)').extract_first(),
            'longitude': response.css('.map-container.w-100::attr(data-longitude)').extract_first(),
            'contacts': [
               {
                 'name': response.css('div:nth-child(1) > strong::text').extract_first(),
                 'telephone': response.css('.broker-phone > a.text-dark::text').extract_first(),
                 'email': response.css('.text-dark.text-truncate.d-block::text').extract_first(),
               }
             ],
        }
