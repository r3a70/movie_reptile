from .serializers import MovieSerializer, TagSerializer, CountrySerializer, ActorsSerializer, LinksSerializer
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .models import Movies, Tags, Country, Actors, Links


@api_view(["GET"])
def main(request: Request):

    if request.method == "GET":

        next_page = False
        main_query = False

        if request.query_params.get('name'):
            movies = Movies.objects.filter(name__icontains=request.query_params.get('name')).all()
        elif request.query_params.get('like'):
            movies = Movies.objects.order_by('like').all()
        elif request.query_params.get('page'):
            next_page = True
            next_page = request.query_params.get('page')
            movies = Movies.objects.filter(id__gte=50 * (int(next_page) - 1), id__lte=50 * int(next_page)).all()
        else:
            next_page = True
            main_query = True
            movies = Movies.objects.filter(id__lte=50).all()

        movie_serializer = MovieSerializer(movies, many=True)

        if next_page:
            if not main_query:
                nex_page = f"http://127.0.0.1:8000/?page={int(request.query_params.get('page'))+1}"
                previous_page = f"http://127.0.0.1:8000/?page={int(request.query_params.get('page'))-1}"
            else:
                nex_page = f"http://127.0.0.1:8000/?page={2}"
                return Response(
                    {
                        "next": nex_page,
                        "information": movie_serializer.data
                    },
                    status=status.HTTP_200_OK
                )

            if movies:

                if int(int(request.query_params.get('page'))-1) <= 0:

                    return Response(
                        {
                            "next": nex_page,
                            "information": movie_serializer.data
                        },
                        status=status.HTTP_200_OK
                    )

                else:

                    return Response(
                        {
                            "next": nex_page,
                            "previous": previous_page,
                            "information": movie_serializer.data
                        },
                        status=status.HTTP_200_OK
                    )

            else:
                return Response(
                    {
                        "previous": previous_page,
                        "information": movie_serializer.data
                    },
                    status=status.HTTP_200_OK
                )

        else:
            return Response(
                {
                    "information": movie_serializer.data
                },
                status=status.HTTP_200_OK
            )


@api_view(["GET"])
def specify_movie(request: Request, movie: int):

    if request.method == "GET":

        movies = Movies.objects.filter(pk=movie).first()
        tags = Tags.objects.filter(movie_id=movie).all()
        country = Country.objects.filter(movie_id=movie).all()
        actors = Actors.objects.filter(movie_id=movie).all()
        link = Links.objects.filter(movie_id=movie).all()

        if not movies:
            return Response(
                {
                    "information": "Not found any movie by this movie id"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        movie_serializer = MovieSerializer(movies)
        tag_serializer = TagSerializer(tags, many=True)
        country_serializer = CountrySerializer(country, many=True)
        actors_serializer = ActorsSerializer(actors, many=True)
        links_serializer = LinksSerializer(link, many=True)

        return Response(
            {
                "information": movie_serializer.data,
                "genre": tag_serializer.data,
                "country": country_serializer.data,
                "actors": actors_serializer.data,
                "links": links_serializer.data,
            },
            status=status.HTTP_200_OK
        )
