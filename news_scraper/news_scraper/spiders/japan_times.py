import scrapy
import csv
from datetime import datetime, timedelta


class JapanTimesSpider(scrapy.Spider):
    name = "japan_times"
    allowed_domains = ["japantimes.co.jp"]
    start_urls = [
        "https://www.japantimes.co.jp/news/world/",
    ]
    # specify the start and end dates to scrape
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 2, 28)

    articles = []

    def parse(self, response):
        articles = response.css("div#main-content article")
        for article in articles:
            category = article.css("div.category>a::text").get()
            if category != "World":
                continue

            url = article.css("h3>a::attr(href)").get()
            yield scrapy.Request(url, callback=self.parse_article)

        next_page_url = response.css("a.next::attr(href)").get()
        if next_page_url is not None:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_article(self, response):
        title = response.css("h1::text").get()
        author = response.css("div.author>a::text").get()
        date = response.css("div.meta time::text").get()
        content = response.css("div#article-body>p::text").getall()

        self.articles.append({
            "title": title,
            "author": author,
            "date": date,
            "content": " ".join(content)
        })

    def closed(self, reason):
        filename = f"{self.name}_articles.csv"
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "author", "date", "content"])
            writer.writeheader()
            writer.writerows(self.articles)
        self.log(f"Saved file {filename}")
