from django.http import HttpRequest, JsonResponse, HttpResponse
from django.core.serializers import serialize
from .models import Movies, Tags, Country, Actors, Links
import json


def main(request: HttpRequest):

    if request.method == "GET":

        parm = request.GET.get('id')

        movies = Movies.objects.filter(pk=parm if parm is not None else 1).first()
        tags = Tags.objects.filter(movie_id=movies.id).all()
        country = Country.objects.filter(movie_id=movies.id).all()
        actors = Actors.objects.filter(movie_id=movies.id).all()
        urls = Links.objects.filter(movie_id=movies.id).all()

        tags = serialize('json', tags)
        country = serialize('json', country)
        actors = serialize('json', actors)
        urls = serialize('json', urls)

        return JsonResponse(
            {
                "id": movies.id,
                "information": [{
                    "name": movies.name,
                    "post_url": movies.post_url,
                    "post_image": movies.post_image,
                    "genre": json.loads(tags),
                    "age": movies.age,
                    "country": json.loads(country),
                    "imdb": movies.imdb,
                    "rating": movies.rating,
                    "site_rate": movies.site_rate,
                    "likes": movies.like,
                    "dislike": movies.dislike,
                    "actors": json.loads(actors),
                    "urls": json.loads(urls)
                }]
            }
        )
