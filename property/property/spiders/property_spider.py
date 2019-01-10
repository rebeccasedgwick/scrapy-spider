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
            'property_name': response.css('.header-text h1::text').extract_first(),
            'address': response.css('.text-muted::text').extract(),
            'price': response.css('tr:nth-child(1) > td:nth-child(2)::text').extract_first(),
            'property-type': response.css('tr:nth-child(2) > td:nth-child(2)::text').extract_first(),
            'size': response.css('tr:nth-child(3) > td:nth-child(2)::text').extract_first(),
            'description': response.css('.js-description-content::text').extract_first(),
            'highlghts': {
                'highlight_1': response.css('ul > div > div:nth-child(1) > li:nth-child(1)::text').extract_first(),
                'highlight_2': response.css('ul > div > div:nth-child(1) > li:nth-child(2)::text').extract_first(),
                'highlight_3': response.css('ul > div > div:nth-child(2) > li:nth-child(1)::text').extract_first(),
                },
            'location': response.css('.js-location-content::text').extract_first(),
            'contacts': [
                {
                    'name': response.css('div:nth-child(1) > table > tbody > tr > td.js-broker-details > strong > a::text').extract_first(),
                    'job_title': response.css('div:nth-child(1) > table > tbody > tr > td.js-broker-details > div:nth-child(2) > small::text').extract_first(),
                    'email': response.css('div:nth-child(1) > table > tbody > tr > td.js-broker-details > div.js-broker-contact-info > a::text').extract_first(),
                    'phone_main': response.css('div:nth-child(1) > table > tbody > tr > td.js-broker-details > div.js-broker-contact-info > div:nth-child(2) > a::text').extract_first(),
                    'phone_office': response.css('div:nth-child(1) > table > tbody > tr > td.js-broker-details > div.js-broker-contact-info > div:nth-child(3) > a::text').extract_first(),
                    'fax': response.css('div:nth-child(1) > table > tbody > tr > td.js-broker-details > div.js-broker-contact-info > div:nth-child(4)::text').extract_first(),
                },
                {
                    'name': response.css('div:nth-child(2) > table > tbody > tr > td.js-broker-details > strong > a::text').extract_first(),
                    'job_title': response.css('div:nth-child(2) > table > tbody > tr > td.js-broker-details > div:nth-child(2) > small::text').extract_first(),
                    'email': response.css('div:nth-child(2) > table > tbody > tr > td.js-broker-details > div.js-broker-contact-info > a::text').extract_first(),
                    'phone_main': response.css('div:nth-child(2) > table > tbody > tr > td.js-broker-details > div.js-broker-contact-info > div:nth-child(2) > a::text').extract_first(),
                    'phone_office': response.css('div:nth-child(2) > table > tbody > tr > td.js-broker-details > div.js-broker-contact-info > div:nth-child(3) > a::text').extract_first(),
                    'fax': response.css('div:nth-child(2) > table > tbody > tr > td.js-broker-details > div.js-broker-contact-info > div:nth-child(4)::text').extract_first(),
                },
                {
                    'name': response.css('div:nth-child(3) > table > tbody > tr > td.js-broker-details > strong > a::text').extract_first(),
                    'job_title': response.css('div:nth-child(3) > table > tbody > tr > td.js-broker-details > div:nth-child(2) > small::text').extract_first(),
                    'email': response.css('div:nth-child(3) > table > tbody > tr > td.js-broker-details > div.js-broker-contact-info > a::text').extract_first(),
                    'phone_main': response.css('div:nth-child(3) > table > tbody > tr > td.js-broker-details > div.js-broker-contact-info > div:nth-child(2) > a::text').extract_first(),
                    'phone_office': response.css('div:nth-child(3) > table > tbody > tr > td.js-broker-details > div.js-broker-contact-info > div:nth-child(3) > a::text').extract_first(),
                    'fax': response.css('div:nth-child(3) > table > tbody > tr > td.js-broker-details > div.js-broker-contact-info > div:nth-child(4)::text').extract_first(),
                }
            ]
        }

    def parse(self, response):
        url = response.css("#buildout iframe::attr(src)").extract_first()

        yield(SplashRequest(url, callback=self.parse_buildout_iframe))
