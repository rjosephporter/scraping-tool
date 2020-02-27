import scrapy
import csv

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://plus-japan.sakura.ne.jp/area.html']
    base_url = 'https://plus-japan.sakura.ne.jp'
    csv_fields = ['Article_Link', 'Website_Link', 'Status']

    def parse(self, response):
        with open('article_links.csv', mode='wb') as article_links:
            article_links_writer = csv.DictWriter(article_links, self.csv_fields)
            for link in response.css('div.archive_box2>div.img>a::attr(href)'):
                full_url = self.base_url + link.extract()
                row = {'Article_Link': full_url, 'Website_Link': 'websitelink', 'Status': 'status'}
                article_links_writer.writerow(row)