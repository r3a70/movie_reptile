import json
import os
import shutil
from pathlib import Path
from autoCelery.celery import app
from crawler.crawler.spiders import uptv_spider, hexdownload_spider
from celery.schedules import crontab
from .database import session
from .models import Movies, Tags, Country, Actors, Links

BASE_DIR = Path(__file__).resolve().parent.parent


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=13, minute=52),
        uptv.s(),
    )
    sender.add_periodic_task(
        crontab(hour=14, minute=30),
        hex_dl.s(),
    )
    sender.add_periodic_task(
        crontab(hour=14, minute=50),
        check_uptv.s(),
    )
    sender.add_periodic_task(
        crontab(hour=16, minute=16),
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
    db = session

    file = open("uptv.json", "r").read()
    data = json.loads(file)

    try:
        for index, value in enumerate(data, start=1):
            for i, v in enumerate(value["links"]):
                new_link = Links(movie_id=index, link=v)
                db.add(new_link)
                db.commit()
            for i, v in enumerate(value["actors"]):
                new_actor = Actors(movie_id=index, actor=v)
                db.add(new_actor)
                db.commit()
            for i, v in enumerate(value["country"]):
                new_country = Country(movie_id=index, country=v)
                db.add(new_country)
                db.commit()
            for i, v in enumerate(value["tags"]):
                new_tags = Tags(movie_id=index, tag=v)
                db.add(new_tags)
                db.commit()
            movie = Movies(
                name=value["name"] if value["name"] is not None else 0,
                post_url=value["post_url"] if value["post_url"] is not None else 0,
                post_image=value["image"] if value["image"] is not None else 0,
                tags_id=index,
                age=value["age"] if value["age"] is not None else 0,
                country_id=index,
                imdb=value["imdb"] if value["imdb"] is not None else 0,
                rating=value["rating"] if value["rating"] is not None else 0,
                site_rate=value["site_rate"] if value["site_rate"] is not None else 0,
                like=int(value["likes"]) if value["likes"] and type(value["likes"]) == int is not None else 0,
                dislike=int(value["dislike"]) if value["dislike"] is not None and type(value["likes"]) == int else 0,
                actors_id=index,
                director=value["director"] if value["director"] is not None else 0,
                story=value["story"] if value["story"] is not None else 0,
                links_id=index,
            )
            db.add(movie)
            db.commit()

    except Exception as error:
        print(error)


@app.task
def check_hex_dl():
    db = session

    file = open("hex_dl.json", "r").read()
    data = json.loads(file)

    try:
        for index, value in enumerate(data, start=1):
            for i, v in enumerate(value["links"]):
                new_link = Links(movie_id=index, link=v)
                db.add(new_link)
                db.commit()
            for i, v in enumerate(value["actors"]):
                new_actor = Actors(movie_id=index, actor=v)
                db.add(new_actor)
                db.commit()
            for i, v in enumerate(value["country"]):
                new_country = Country(movie_id=index, country=v)
                db.add(new_country)
                db.commit()
            for i, v in enumerate(value["tags"]):
                new_tags = Tags(movie_id=index, tag=v)
                db.add(new_tags)
                db.commit()
            movie = Movies(
                name=value["name"] if value["name"] is not None else 0,
                post_url=value["post_url"] if value["post_url"] is not None else 0,
                post_image=value["image"] if value["image"] is not None else 0,
                tags_id=index,
                age=value["age"] if value["age"] is not None else 0,
                country_id=index,
                imdb=value["imdb"] if value["imdb"] is not None else 0,
                rating=value["rating"] if value["rating"] is not None else 0,
                site_rate=value["site_rate"] if value["site_rate"] is not None else 0,
                like=int(value["likes"]) if value["likes"] and type(value["likes"]) == int is not None else 0,
                dislike=int(value["dislike"]) if value["dislike"] is not None and type(value["likes"]) == int else 0,
                actors_id=index,
                director=value["director"] if value["director"] is not None else 0,
                story=value["story"] if value["story"] is not None else 0,
                links_id=index,
            )
            db.add(movie)
            db.commit()

    except Exception as error:
        print(error)
