import scrapy
from scrapy.exporters import CsvItemExporter


class JapanTimeSpider(scrapy.Spider):
    name = "datejt"
    def start_requests(self):
        for i in range(13, 44): 
            url = f'https://www.japantimes.co.jp/news/world/page/{i}'
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        hrefs = response.css(".content_col a.more_link::attr(href)").getall()
        second_href = hrefs[1] if len(hrefs) > 1 else None
        yield {"second_href": second_href}
        
def closed(self, reason):
        articles = self.crawler.stats.get('item_scraped_count', 0)
        if articles:
            file = open('datejt.csv', 'wb')
            exporter = CsvItemExporter(file)
            exporter.start_exporting()
            for item in self.crawler.stats.get_value('items'):
                exporter.export_item(item)
            exporter.finish_exporting()
            file.close()
            self.log('Saved %s datejt to file' % articles)
