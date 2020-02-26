import scrapy
import csv

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://plus-japan.sakura.ne.jp/area.html']
    base_url = 'https://plus-japan.sakura.ne.jp'

    def parse(self, response):
        with open('article_links.csv', mode='wb') as article_links:
            article_links_writer = csv.writer(article_links, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for link in response.css('div.archive_box2>div.img>a::attr(href)'):
                full_url = self.base_url + link.extract()        
                article_links_writer.writerow([full_url, 'test'])