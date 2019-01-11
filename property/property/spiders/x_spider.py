import scrapy
from scrapy_splash import SplashRequest
from datetime import datetime


class AmericanRealtySpider(scrapy.Spider):
    name = 'american_realty'
    start_urls = ['http://amreal.com/property.htm']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        url = response.css('#buildout > iframe::attr(src)').extract_first()
        yield SplashRequest(url, callback=self.parse_buildout_iframe, args={'wait': 5})

    def dummy_fn_callback(self, url):
        print('xxxxxxx')
        print(response.url)
        print(response.body)
        return "123"

    def parse_buildout_iframe(self, response):
        properties_count = len(response.css('.row.map-listings.border-top.border-bottom.hidden-xs > .col-md-12 > div'))
        print(properties_count)

        for property_id in range(1, 2):
        # for property_id in range(0, properties_count - 1):

            script = """
                function main(splash)
                    splash:go("{url}")
                    splash:wait(5)
                    splash:runjs("document.querySelector('.map-listings .list-item').click()")

                    splash:wait(5)
                    return splash:html()
                end
            """.format(url=response.url, property_id=property_id)

        print(script)

        # yield SplashRequest(callback=self.dummy_fn_callback, endpoint='execute', args={'lua_source': script, 'wait': 3})
        yield SplashRequest(callback=self.parse_individual_property, endpoint='execute', args={'lua_source': script, 'wait': 3})

        # splash:runjs("document.querySelector('.row.border-bottom.hidden-xs.clickable.list-item').click()")
        #
        # script = """
        #     function main(splash)
        #         splash:runjs("window.location='https://www.google.com/ncr'")
        #         splash:wait(1)
        #         return splash:html()
        #     end
        # """
        # script0 = """
        #     function main(splash)
        #         splash:runjs("")
        #         splash:wait(1)
        #         return splash:evaljs("window.location")
        #     end
        # """
        # x = yield SplashRequest(callback=self.xx, endpoint='execute', args={'lua_source': script0})
        # print(x)
        # print(x.response.body)
        # yield SplashRequest(callback=self.xx, endpoint='execute', args={'lua_source': script})
        # print(x)
        # print(response.body)


        # splash:runjs("document.querySelector('.row.border-bottom.hidden-xs.clickable.list-item:nth-child({property_id})').click()")
        # local element = splash:select('.row.border-bottom.hidden-xs.clickable.list-item:nth-child({property_id})')
        # local element = splash:select_all('.map-listings .list-item')[{property_id}]
        # list_element_selector = '.row.border-bottom.hidden-xs.clickable.list-item'
        #
        # script = """
        #     function main(splash)
        #         assert(splash:go(splash.args.url))
        #         splash:wait(0.5)
        #         local element = splash:select('.row.border-bottom.hidden-xs.clickable.list-item')
        #         local bounds = element:bounds()
        #         element:mouse_click()
        #         return splash:html()
        #     end
        # """
        #
        # yield SplashRequest(url, self.parse_individual_property, endpoint='execute', args={'lua_source': script})

    def parse_individual_property(self, response):
        yield {
            'scraped_at': datetime.now(),
            'url': response.url,
        }
