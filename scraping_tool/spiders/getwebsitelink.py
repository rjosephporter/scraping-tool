import scrapy
from scrapy.http.request import Request
from scrapy import signals
import csv
from tempfile import NamedTemporaryFile
import shutil

class GetWebsiteLink(scrapy.Spider):
    name = 'getwebsitelink'
    tempfile = NamedTemporaryFile(mode = 'w', delete = False)
    csv_fields = ['Article_Link', 'Website_Link', 'Status']
    links_array = []

    def start_requests(self):
        with open('article_links.csv', 'rb') as urls:
            article_links_reader = csv.DictReader(urls, self.csv_fields)
            for row in article_links_reader:
                if row['Article_Link']:
                    yield Request(row['Article_Link'], self.parse, 'GET', None, None, meta={'original_url': row['Article_Link']})

    def parse(self, response):
        website_url = response.css('div.interview_head>div.data_box>div.btn>a::attr(href)').extract_first()
        self.links_array.append({ 'article_link': response.meta['original_url'], 'website_link': website_url })

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(GetWebsiteLink, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        with open('article_links.csv', 'wb') as write_urls:
            article_links_writer = csv.DictWriter(write_urls, self.csv_fields)
            for link in self.links_array:
                article_links_writer.writerow({'Article_Link': link['article_link'], 'Website_Link': link['website_link'], 'Status': 'status'})