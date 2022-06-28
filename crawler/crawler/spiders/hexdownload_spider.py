import scrapy
import re


class HexDlSpider(scrapy.Spider):
    name = "hex-dl"

    def start_requests(self):
        urls = [
            "https://hexdownload.co/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: scrapy.http.Response, **kwargs):
        posts = response.css("article header")

        for post in posts:
            post_url = post.css("h2 a::attr(href)").get()
            if post_url:
                yield scrapy.Request(post_url, callback=self.post_parse)

    def post_parse(self, response: scrapy.http.Response):

        yield {
            "name": response.css("article header h1 a::text").get().strip(),
            "post_url": response.url,
            "image": response.css("p.post-image a img::attr(src)").get(),
            "tags": response.css("p.film-genre a::text").getall(),
            "age": response.css("ul li.pg::text").get().strip(),
            "country": response.css("p.film-country::text").getall(),
            "imdb": response.css("p.film-rate span a::attr(href)").get()

        }
