import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from scrapy import signals
import json
import logging

logger = logging.getLogger('scraping_tool_logger')

class WebsiteCrawl(CrawlSpider):
    name = 'websitecrawl'

    def __init__(self, row_id = None, allowed_domains = None, start_urls = None, urls_to_look = None, total = None, *args, **kwargs):
        logging.getLogger('scrapy.spidermiddlewares.httperror').setLevel(logging.WARNING)
        logging.getLogger('scrapy.core.scraper').setLevel(logging.WARNING)
        logging.getLogger('scrapy.middleware').setLevel(logging.WARNING)
        logging.getLogger('scrapy.statscollectors').setLevel(logging.WARNING)
        logging.getLogger('scrapy.extensions.telnet').setLevel(logging.WARNING)
        logging.getLogger('scrapy.core.engine').setLevel(logging.WARNING)
        logging.getLogger('scrapy.crawler').setLevel(logging.WARNING)

        self.row_id = row_id
        self.allowed_domains = allowed_domains  
        self.start_urls = start_urls
        self.urls_to_look = urls_to_look
        self.found_at = []
        self.total = total

        with open('article_links.json', 'rb') as json_file:
            self.data = json.load(json_file)

        super(WebsiteCrawl, self).__init__(*args, **kwargs)

    rules = (
        Rule(LinkExtractor(), callback='parse_url', follow=True),
    )

    def parse_url(self, response):
        hxs = scrapy.Selector(response)
        all_links = hxs.xpath('*//a/@href').extract()
        for link in all_links:
            for url_to_look in self.urls_to_look:
                if link == url_to_look:  
                    self.found_at.append(response.url)
                    raise CloseSpider('FOUND')

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(WebsiteCrawl, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        return spider

    def spider_opened(self, spider):
        logger.info('[' + str(self.row_id + 1) + '/' + str(self.total) + '] CRAWLING ' + ' '.join(self.start_urls) + ' AND LOOKING FOR [' + ', '.join(self.urls_to_look) + ']')
    
    def spider_closed(self, spider):
        for row in self.data:
            if row['ID'] == self.row_id:
                if len(self.found_at) > 0:
                    self.data[row['ID']]['Result'] = { 'Status': 'Found', 'Found_At': self.found_at }                    
                    logger.info('FOUND AT [' + ', '.join(self.found_at) + ']')
                    self.found_at = []
                else:
                    self.data[row['ID']]['Result'] = { 'Status': 'Not Found' }
                    logger.info('NOT FOUND')
                
        with open('article_links.json', 'wb') as write_urls:
            json.dump(self.data, write_urls)