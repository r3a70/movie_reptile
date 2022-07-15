import json
from pathlib import Path
from autoCelery.celery import app
from crawler.crawler.spiders import uptv_spider, hexdownload_spider
from celery.schedules import crontab
# from .database import session
# from .models import Movies, Tags, Country, Actors, Links

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MovieCrawler.settings')
application = get_wsgi_application()

from main.models import Movies, Tags, Country, Actors, Links


BASE_DIR = Path(__file__).resolve().parent.parent


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(
    #     crontab(hour=17, minute=25),
    #     uptv.s(),
    # )
    # sender.add_periodic_task(
    #     crontab(hour=18, minute=19),
    #     hex_dl.s(),
    # )
    sender.add_periodic_task(
        crontab(hour=11, minute=20),
        check_uptv.s(),
    )
    sender.add_periodic_task(
        crontab(hour=11, minute=50),
        check_hex_dl.s(),
    )


@app.task
def uptv():
    uptv_spider.run_upt()


@app.task
def hex_dl():
    hexdownload_spider.run_hex()


@app.task
def check_uptv():
    file = open("uptv.json", "r").read()
    data = json.loads(file)

    count = Movies.objects.count()
    try:
        for index, value in enumerate(data, start=count+1):
            query = Movies.objects.filter(name=value['name']).first()
            if query:
                continue

            if len(value['tags']) > 0:
                for _, v in enumerate(value['tags']):
                    new_tag = Tags(movie_id=index, tag=v)
                    new_tag.save()
            else:
                new_tag = Tags(movie_id=index, tag="0")
                new_tag.save()

            new_country = Country(movie_id=index, country=value['country'])
            new_country.save()

            if len(value['actors']) > 0:
                for _, v in enumerate(value['actors']):
                    new_actor = Actors(movie_id=index, actor=v)
                    new_actor.save()
            else:
                new_actor = Actors(movie_id=index, actor="0")
                new_actor.save()

            if len(value['links']) > 0:
                for _, v in enumerate(value['links']):
                    new_link = Links(movie_id=index, link=v)
                    new_link.save()
            else:
                new_link = Links(movie_id=index, link="0")
                new_link.save()

            new_movie = Movies(
                name=value['name'] if value['name'] is not None else "0",
                post_url=value['post_url'] if value['post_url'] is not None else "0",
                post_image=value['image'] if value['image'] is not None else "0",
                tags=new_tag,
                age=value['age'] if value['age'] is not None else "0",
                country=new_country,
                imdb=value['imdb'] if value['imdb'] is not None else "0",
                rating=value['rating'] if value['rating'] is not None else "0",
                site_rate=value['site_rate'] if value['site_rate'] is not None else "0",
                like=value['likes'] if value['likes'] is not None else 0,
                dislike=value['dislike'] if value['dislike'] is not None else 0,
                actors=new_actor,
                director=value['director'] if value['director'] is not None else "0",
                story=value['story'] if value['story'] is not None else "0",
                links=new_link
            )
            new_movie.save()

    except Exception as error:
        print(error)


@app.task
def check_hex_dl():
    file = open("hex_dl.json", "r").read()
    data = json.loads(file)

    count = Movies.objects.count()
    try:
        for index, value in enumerate(data, start=count + 1):
            query = Movies.objects.filter(name=value['name']).first()
            if query:
                continue
            if len(value['tags']) > 0:
                for _, v in enumerate(value['tags']):
                    new_tag = Tags(movie_id=index, tag=v)
                    new_tag.save()
            else:
                new_tag = Tags(movie_id=index, tag="0")
                new_tag.save()

            new_country = Country(movie_id=index, country=value['country'])
            new_country.save()

            if len(value['actors']) > 0:
                for _, v in enumerate(value['actors']):
                    new_actor = Actors(movie_id=index, actor=v)
                    new_actor.save()
            else:
                new_actor = Actors(movie_id=index, actor="0")
                new_actor.save()

            if len(value['links']) > 0:
                for _, v in enumerate(value['links']):
                    new_link = Links(movie_id=index, link=v)
                    new_link.save()
            else:
                new_link = Links(movie_id=index, link="0")
                new_link.save()

            new_movie = Movies(
                name=value['name'] if value['name'] is not None else "0",
                post_url=value['post_url'] if value['post_url'] is not None else "0",
                post_image=value['image'] if value['image'] is not None else "0",
                tags=new_tag,
                age=value['age'] if value['age'] is not None else "0",
                country=new_country,
                imdb=value['imdb'] if value['imdb'] is not None else "0",
                rating=value['rating'] if value['rating'] is not None else "0",
                site_rate=value['site_rate'] if value['site_rate'] is not None else "0",
                like=value['likes'] if value['likes'] is not None else 0,
                dislike=value['dislike'] if value['dislike'] is not None else 0,
                actors=new_actor,
                director=value['director'] if value['director'] is not None else "0",
                story=value['story'] if value['story'] is not None else "0",
                links=new_link
            )
            new_movie.save()
    except Exception as error:
        print(error)
