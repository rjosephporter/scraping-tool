import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class WebsiteCrawl(CrawlSpider):
    name = 'websitecrawl'
    allowed_domains = ['holic-inc.jp']
    start_urls = ['https://holic-inc.jp/bodyandmake/']
    url_to_look = 'https://plus-japan.sakura.ne.jp/area/holic.html'
    counter = 1

    rules = (
        Rule(LinkExtractor(), callback='parse_url', follow=True),
    )

    def parse_url(self, response):
        hxs = scrapy.Selector(response)
        all_links = hxs.xpath('*//a/@href').extract()
        print(response.url)
        for link in all_links:
            if link == self.url_to_look:                
                print('FOUND - ' + link)
                raise CloseSpider('Found!')
