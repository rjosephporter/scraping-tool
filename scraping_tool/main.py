import scrapy
from spiders.myspider import MySpider
from spiders.getwebsitelink import GetWebsiteLink
from spiders.websitecrawl import WebsiteCrawl
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import urlparse
import csv

csv_fields = ['Article_Link', 'Website_Link', 'Status']
links_array = []

configure_logging()
runner = CrawlerRunner()
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(MySpider)
    yield runner.crawl(GetWebsiteLink)
    with open('article_links.csv', 'rb') as links:
        article_links_reader = csv.DictReader(links, csv_fields)
        for row in article_links_reader:
            links_array.append(row)

    for links in links_array:
        parsed_uri = urlparse.urlparse(links['Website_Link'])
        allowedDomains = []
        allowedDomains.append('{uri.netloc}'.format(uri=parsed_uri))
        yield runner.crawl(WebsiteCrawl, allowed_domains = allowedDomains, start_urls = [links['Website_Link']], url_to_look = links['Article_Link'])    
    reactor.stop()

crawl()
reactor.run()

# process = CrawlerProcess()

# process.crawl(MySpider)
# process.crawl(GetWebsiteLink)

# with open('article_links.csv', 'rb') as links:
#     article_links_reader = csv.DictReader(links, csv_fields)
#     for row in article_links_reader:
#         links_array.append(row)

# for links in links_array:
#     parsed_uri = urlparse.urlparse(links['Website_Link'])
#     allowedDomains = []
#     allowedDomains.append('{uri.netloc}'.format(uri=parsed_uri))
#     process.crawl
#     process.crawl(WebsiteCrawl, allowed_domains = allowedDomains, start_urls = [links['Website_Link']], url_to_look = links['Article_Link'])

# process.start()