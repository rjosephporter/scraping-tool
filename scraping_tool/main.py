import scrapy
from spiders.myspider import MySpider
from spiders.websitecrawl import WebsiteCrawl
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()

process.crawl(MySpider)
process.crawl(WebsiteCrawl)
process.start()




