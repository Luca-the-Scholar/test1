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

my_data = read_csv_file('datejt.csv')

class JapanTimesSpider(scrapy.Spider):
    name = "contentjt"
    start_urls = my_data
    
    def parse(self, response):
        title = response.css('div.main.basic-post-type-single h1::text').get()

        article = response.css('div#jtarticle p::text').getall()

        authors = response.css('h5.writer a::text').getall()

        date = response.css('div.meta-right time::text').get()

        yield {
            'title': title,
            'article': article,
            'authors': authors,
            'date': date
        }
