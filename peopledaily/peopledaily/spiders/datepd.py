import scrapy
from scrapy.exporters import CsvItemExporter


class PeopleDailySpider(scrapy.Spider):
   name = "datepd"
   def start_requests(self):
       for i in range(21, 62):
           url = f'http://en.people.cn/90777/index{i}.html'
           yield scrapy.Request(url, callback=self.parse)


   def parse(self, response):
       for world in response.css('ul.foreign_list8.cf'):
           for href in world.css('li a::attr(href)').getall():
               yield {
                   'article': 'http://en.people.cn' + href,
               }


       next_page = response.css('div.page_n.clearfix a::attr(href)').get()
       if next_page is not None:
           next_page = response.urljoin(next_page)
           yield scrapy.Request(next_page, callback=self.parse)


   def closed(self, reason):
       articles = self.crawler.stats.get('item_scraped_count', 0)
       if articles:
           file = open('datepd.csv', 'wb')
           exporter = CsvItemExporter(file)
           exporter.start_exporting()
           for item in self.crawler.stats.get_value('items'):
               exporter.export_item(item)
           exporter.finish_exporting()
           file.close()
           self.log('Saved %s datepd to file' % articles)
