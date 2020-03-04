import scrapy
from spiders.myspider import MySpider
from spiders.websitecrawl import WebsiteCrawl
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import urlparse
import json

data=[]
s = get_project_settings()

configure_logging(s)
runner = CrawlerRunner(s)
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(MySpider)

    with open('article_links.json', 'rb') as json_file:
        data = json.load(json_file)

    total_websites = len(data)

    for row in data:
        parsed_uri = urlparse.urlparse(row['Website_Link'])
        allowedDomains = []
        allowedDomains.append('{uri.netloc}'.format(uri=parsed_uri))
        yield runner.crawl(WebsiteCrawl, row_id = row['ID'], allowed_domains = allowedDomains, start_urls = [row['Website_Link']], urls_to_look = row['Article_Links'], total = total_websites)
    reactor.stop()

crawl()
reactor.run()