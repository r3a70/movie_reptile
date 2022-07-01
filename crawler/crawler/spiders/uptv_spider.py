import scrapy
from scrapy.crawler import CrawlerProcess


class UptvSpider(scrapy.Spider):
    name = "uptv"

    def start_requests(self):
        urls = [
            "https://www.uptvs.com/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: scrapy.http.Response, **kwargs):
        posts = response.css("article div.row")

        for post in posts:
            post_url = post.css("div a::attr(href)").get()
            if post_url:
                yield scrapy.Request(post_url, callback=self.post_parse)

        for i in range(len(response.css("div.container div.row div.main-posts ul li a::attr(href)").getall())):

            if response.css("div.container div.row div.main-posts ul li a::text")[i].get() == "بعدی":

                next_page = response.css("div.container div.row div.main-posts ul li a::attr(href)")[i].get()
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

    def post_parse(self, response: scrapy.http.Response):

        def list_cleaner(val: list) -> list:
            val.remove('  ') if '  ' in val else val
            return val

        def create_post_rating(ratings: list, start: int, end: int) -> str:
            return ' '.join(ratings[start:end]) if start != end and len(ratings) >= end else ''.join(ratings[start]) \
                                                if len(ratings) >= start else ''.join(ratings)

        def find_director() -> str:
            return (
                       response.css("div.col-lg-12 div.post-single-artist a::text").getall()[-1] if
                       response.css("div.col-lg-12 div.post-single-artist a::attr(class)").getall() and
                       response.css("div.col-lg-12 div.post-single-artist a::attr(class)").getall()[-1][0:8]
                       == "director" else None
            )

        posts = response.css("div.container-sm")

        post_name = response.css("div h1::text").get().strip() if response.css("div h1::text").get() else None

        post_image = response.css("div a img::attr(src)").get()

        post_tags = list_cleaner(list(set(response.css("div.row span a::text").getall())))

        post_age = response.css("div.row span span::text").get().strip() \
            if response.css("div.row span span::text").get() else None

        post_country = response.css("div.row span.d-md-inline-block::text").getall()[1].strip() if \
            response.css("div.row span.d-md-inline-block::text").getall() else None

        post_imdb = response.css("div.row div div div.row div.col-md-auto a::attr(href)").get()

        post_ratings = create_post_rating(
            response.css("div.row div div div.row div.col-md-auto span::text").getall(), 0, 3
        )

        post_uptv_loves = create_post_rating(
            response.css("div.row div div div.row div.col-md-auto span::text").getall(), 3, 5
        )

        post_likes = response.css("span.like-count::text").get().strip() \
            if response.css("span.like-count::text").get() else 0

        post_dislike = response.css("span.dislike-count::text").get().strip() \
            if response.css("span.dislike-count::text").get() else 0

        post_video_actors = response.css("div.col-lg-12 div.mb-half a::text").getall()

        post_video_director = find_director()

        post_video_story = response.css("p.show-read-more::text").get().strip() if \
            response.css("p.show-read-more::text").get() else None

        post_download_links = response.css("a.btn-sm::attr(href)").getall()

        if not post_name:
            pass
        else:
            yield {
                "name": post_name,
                "post_url": response.url,
                "image": post_image,
                "tags": post_tags,
                "age": post_age,
                "country": post_country,
                "imdb": post_imdb,
                "rating": post_ratings,
                "site_rate": post_uptv_loves,
                "likes": post_likes,
                "dislike": post_dislike,
                "actors": post_video_actors,
                "director": post_video_director,
                "story": post_video_story,
                "links": post_download_links
            }


def run_upt():
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                "uptv.json": {"format": "json", "indent": 4},
            },
            "FEED_EXPORTERS": {
                'json': 'crawler.crawler.exporters.Utf8JsonItemExporter',
            },
        }
    )
    process.crawl(UptvSpider)
    process.start()
