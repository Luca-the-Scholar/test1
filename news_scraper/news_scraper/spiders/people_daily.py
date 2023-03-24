import scrapy
import csv


class PeopleDailySpider(scrapy.Spider):
    name = "people_daily"
    allowed_domains = ["en.people.cn"]
    start_urls = [
        "http://en.people.cn/90001/90777/90851/index1.html",
        "http://en.people.cn/90001/90777/90851/index2.html",
        "http://en.people.cn/90001/90777/90851/index3.html",
        "http://en.people.cn/90001/90777/90851/index4.html",
        "http://en.people.cn/90001/90777/90851/index5.html",
        "http://en.people.cn/90001/90777/90851/index6.html",
        "http://en.people.cn/90001/90777/90851/index7.html",
        "http://en.people.cn/90001/90777/90851/index8.html",
        "http://en.people.cn/90001/90777/90851/index9.html",
        "http://en.people.cn/90001/90777/90851/index10.html"
    ]

    articles = []

    def parse(self, response):
        articles = response.css("div.articleList>ul>li")
        for article in articles:
            category = article.css("span.subTitle::text").get()
            if category != "World":
                continue

            url = article.css("a::attr(href)").get()
            yield scrapy.Request(url, callback=self.parse_article)

        next_page_url = response.css("a.next::attr(href)").get()
        if next_page_url is not None:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_article(self, response):
        title = response.css("h1::text").get()
        author = response.css("div.author::text").get().strip().replace("By ", "")
        date = response.css("div.date::text").get().strip()
        content = response.css("div#p_content>div>p::text").getall()

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
