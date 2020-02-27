import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http.request import Request
from scrapy.exceptions import CloseSpider
import csv

class WebsiteCrawl(CrawlSpider):
    name = 'websitecrawl'
    #allowed_domains = []
    #start_urls = []
    #url_to_look = ''
    csv_fields = ['Article_Link', 'Website_Link', 'Status']

    def __init__(self, allowed_domains = None, start_urls = None, url_to_look = None, *args, **kwargs):
        self.allowed_domains = allowed_domains  
        self.start_urls = start_urls
        self.url_to_look = url_to_look
        super(WebsiteCrawl, self).__init__(*args, **kwargs)

    rules = (
        Rule(LinkExtractor(), callback='parse_url', follow=True),
    )

    # def start_requests(self):
    #     with open('article_links.csv', 'rb') as urls:
    #         article_links_reader = csv.DictReader(urls, self.csv_fields)
    #         for row in article_links_reader:
    #             if row['Article_Link'] and row['Website_Link']:
    #                 yield Request(row['Website_Link'], self.parse, 'GET', None, None, meta={'article_link': row['Article_Link'], 'website_link': row['Website_Link']})

    def parse_url(self, response):
        hxs = scrapy.Selector(response)
        all_links = hxs.xpath('*//a/@href').extract()
        for link in all_links:
            if link == self.url_to_look:  
                file = open('output.txt', 'a+')
                file.write('FOUND - ' + self.url_to_look + ' - ' + response.url + '\n')
                file.close()
                #print('FOUND - ' + response.url)
                raise CloseSpider('FOUND')
