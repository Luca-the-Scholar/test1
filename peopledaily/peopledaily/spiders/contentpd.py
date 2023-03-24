import scrapy
from scrapy.exporters import CsvItemExporter
import csv


def read_csv_file(filename):
   urls = []
   with open(filename, 'r') as csvfile:
       reader = csv.reader(csvfile)
       for row in reader:
           urls.append(''.join(row))
   return urls


my_data = read_csv_file('datepd.csv')


class PeopleArticleSpider(scrapy.Spider):
   name = "contentpd"
   start_urls = my_data
  
   custom_settings = {
       'FEED_FORMAT': 'csv',
       'FEED_URI': 'datepd.csv'
   }


   def parse(self, response):
       exporter = CsvItemExporter(open('contentpd.csv', 'a+b'))
       for contentpd in response.css('div.w860.d2txtCon.cf'):
           item = {
               'title': contentpd.css('h1::text').get(),
               'article': contentpd.css('p::text').getall(),
               'author': contentpd.css('div.editor::text').get(),
               'date': contentpd.css('span::text').get(),
           }
           exporter.export_item(item)
       exporter.finish_exporting()
