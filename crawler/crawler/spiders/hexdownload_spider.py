import scrapy
from scrapy.crawler import CrawlerProcess


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

        next_page = response.css("div.navigation ul a::attr(href)").getall()[-1] if \
            response.css("div.navigation ul a::attr(href)").getall() else None
        if next_page:
            response.urljoin(next_page)
            yield scrapy.Request(next_page, self.parse)

    def post_parse(self, response: scrapy.http.Response):

        post_name = response.css("article header h1 a::text").get().strip() \
            if response.css("article header h1 a::text").get() else None

        post_url = response.url

        post_image = response.css("p.post-image a img::attr(src)").get()

        post_tags = response.css("p.film-genre a::text").getall()

        post_age = response.css("ul li.pg::text").get().replace("رده سنی :", "").strip()\
            if response.css("ul li.pg::text").get() else None

        post_country = response.css("p.film-country::text").getall()

        post_imdb = response.css("p.film-rate span a::attr(href)").get()

        post_ratting = "امتیاز " + response.css("p.film-rate strong::text").get() + " " + \
                       response.css("p.film-rate span::text").get() + "IMDB" if \
            response.css("p.film-rate strong::text").get() and response.css("p.film-rate span::text").get() else None

        post_actors = response.css("p.film-actor::text").getall()

        post_director = response.css("p.film-director::text").get().replace("کارگردان :", "").strip() if \
            response.css("p.film-director::text").get() is not None else "نامعلوم"

        post_story = response.css("p.film-story::text").get().strip().replace("\u200c", " ") if \
            response.css("p.film-story::text").get() else None

        post_links = response.css("li ul.l1nk a::attr(href)").getall()

        yield {
            "name": post_name,
            "post_url": post_url,
            "image": post_image,
            "tags": post_tags,
            "age": post_age,
            "country": post_country,
            "imdb": post_imdb,
            "rating": post_ratting,
            "site_rate": None,
            "likes": None,
            "dislike": None,
            "actors": post_actors,
            "director": post_director,
            "story": post_story,
            "links": post_links

        }


def run_hex():
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                "hex_dl.json": {"format": "json", "indent": 4},
            },
            "FEED_EXPORTERS": {
                'json': 'crawler.crawler.exporters.Utf8JsonItemExporter',
            },
        }
    )
    process.crawl(HexDlSpider)
    process.start()


