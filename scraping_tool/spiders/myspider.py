import scrapy
import json
from scrapy import signals
from scrapy.http.request import Request

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://plus-japan.sakura.ne.jp/area.html']
    base_url = 'https://plus-japan.sakura.ne.jp'
    data = []

    def parse(self, response):
        for index, link in enumerate(response.css('div.archive_box2>div.img>a::attr(href)')):
            full_url = self.base_url + link.extract()
            row = {}
            row['ID'] = index
            row['Article_Links'] = []
            row['Article_Links'].append(full_url)
            self.data.append(row)
   
        for row in self.data:
            yield Request(row['Article_Links'][0], self.parse_article_link, meta={ 'id': row['ID'], 'original_url': row['Article_Links'][0] }, priority=row['ID'])
        
    def parse_article_link(self, response):
        website_url = response.css('div.interview_head>div.data_box>div.btn>a::attr(href)').extract_first()
        for row in self.data:
            if row['ID'] == response.meta['id']:
                if response.meta['original_url'] <> response.url:
                    self.data[row['ID']]['Article_Links'].append(response.url)
                yield Request(website_url, self.parse_website_url, meta={ 'id': row['ID'], 'original_url': website_url })
    
    def parse_website_url(self, response):
        for row in self.data:
            if row['ID'] == response.meta['id']:
                self.data[row['ID']]['Website_Link'] = response.url

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MySpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        with open('article_links.json', 'wb') as write_urls:
            json.dump(self.data, write_urls)