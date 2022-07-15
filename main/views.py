from .serializers import MovieSerializer, TagSerializer, CountrySerializer, ActorsSerializer, LinksSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Movies, Tags, Country, Actors, Links


@api_view(['GET'])
def home(request: Request):
    return Response(
        {
            "main": "http://" + request.META['HTTP_HOST'] + '/api/v1/',
        }
    )


@api_view(["GET"])
def main(request: Request):

    if request.method == "GET":

        next_page = False
        main_query = False
        base_url = "http://" + request.META['HTTP_HOST'] + '/api/v1/'

        if request.query_params.get('name'):
            movies = Movies.objects.filter(name__icontains=request.query_params.get('name')).all()
        elif request.query_params.get('like'):
            max_res = int(request.query_params.get('like')) if int(request.query_params.get('like')) < 250 else 250
            movies = Movies.objects.all().order_by('-like').filter()[:max_res]
        elif request.query_params.get('actor'):
            movies = Movies.objects.filter(actors__actor__icontains=request.query_params.get('actor')).all()
        elif request.query_params.get('director'):
            movies = Movies.objects.filter(director__icontains=request.query_params.get('director')).all()
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
                nex_page = f"{base_url}?page={int(request.query_params.get('page'))+1}"
                previous_page = f"{base_url}?page={int(request.query_params.get('page'))-1}"
            else:
                nex_page = f"{base_url}?page={2}"
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


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def add_tag(request: Request):
    if request.method == "POST":
        new_movie = TagSerializer(data=request.data)
        if new_movie.is_valid():
            new_movie.save()
            return Response({"OK": new_movie.data}, status=status.HTTP_201_CREATED)

        return Response({"empty field detected!!!": new_movie.errors.keys()}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        if request.query_params.get('id'):
            queryset = Tags.objects.filter(id=request.query_params.get('id'), movie_id=request.data['movie_id']).first()
            if queryset:
                data = TagSerializer(data=request.data)

                if data.is_valid():
                    queryset.tag = request.data['tag']
                    queryset.save()
                    return Response({"OK": data.data}, status=status.HTTP_202_ACCEPTED)

                return Response({"OK": "data is invalid!"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"OK": "tag id not found"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_tag(request: Request, tag: int):
    tag_id = request.query_params.get('tg_id')
    if tag_id:
        queryset = Tags.objects.filter(movie_id=tag, id=tag_id).first()
    else:
        queryset = Tags.objects.filter(movie_id=tag).all()

    if queryset:
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response({"OK": "tag not found!!!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def add_country(request: Request):
    if request.method == "POST":
        new_movie = CountrySerializer(data=request.data)
        if new_movie.is_valid():
            new_movie.save()
            return Response({"OK": new_movie.data}, status=status.HTTP_201_CREATED)

        return Response({"empty field detected!!!": new_movie.errors.keys()}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        if request.query_params.get('id'):
            queryset = Country.objects.filter(id=request.query_params.get('id'), movie_id=request.data['movie_id']).first()
            if queryset:
                data = CountrySerializer(data=request.data)

                if data.is_valid():
                    queryset.country = request.data['country']
                    queryset.save()
                    return Response({"OK": data.data}, status=status.HTTP_202_ACCEPTED)

                return Response({"OK": "data is invalid!"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"OK": "country id not found"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_country(request: Request, country: int):
    country_id = request.query_params.get('ct_id')
    if country_id:
        queryset = Country.objects.filter(movie_id=country, id=country_id).first()
    else:
        queryset = Country.objects.filter(movie_id=country).all()

    if queryset:
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response({"OK": "country not found!!!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def add_actor(request: Request):
    if request.method == "POST":
        new_movie = ActorsSerializer(data=request.data)
        if new_movie.is_valid():
            new_movie.save()
            return Response({"OK": new_movie.data}, status=status.HTTP_201_CREATED)

        return Response({"empty field detected!!!": new_movie.errors.keys()}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        if request.query_params.get('id'):
            queryset = Actors.objects.filter(id=request.query_params.get('id'), movie_id=request.data['movie_id']).first()
            if queryset:
                data = ActorsSerializer(data=request.data)

                if data.is_valid():
                    queryset.actor = request.data['actor']
                    queryset.save()
                    return Response({"OK": data.data}, status=status.HTTP_202_ACCEPTED)

                return Response({"OK": "data is invalid!"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"OK": "actor id not found"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_actor(request: Request, actor: int):
    actor_id = request.query_params.get('ac_id')
    if actor_id:
        queryset = Actors.objects.filter(movie_id=actor, id=actor_id).first()
    else:
        queryset = Actors.objects.filter(movie_id=actor).all()

    if queryset:
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response({"OK": "country not found!!!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def add_link(request: Request):
    if request.method == "POST":
        new_movie = LinksSerializer(data=request.data)
        if new_movie.is_valid():
            new_movie.save()
            return Response({"OK": new_movie.data}, status=status.HTTP_201_CREATED)

        return Response({"empty field detected!!!": new_movie.errors.keys()}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        if request.query_params.get('id'):
            queryset = Links.objects.filter(id=request.query_params.get('id'), movie_id=request.data['movie_id']).first()
            if queryset:
                data = LinksSerializer(data=request.data)

                if data.is_valid():
                    queryset.link = request.data['link']
                    queryset.save()
                    return Response({"OK": data.data}, status=status.HTTP_202_ACCEPTED)

                return Response({"OK": "data is invalid!"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"OK": "link id not found"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_link(request: Request, link: int):
    link_id = request.query_params.get('li_id')
    if link_id:
        queryset = Links.objects.filter(movie_id=link, id=link_id).first()
    else:
        queryset = Links.objects.filter(movie_id=link).all()

    if queryset:
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response({"OK": "link not found!!!"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def add_movie(request: Request):
    if request.method == "POST":
        new_movie = MovieSerializer(data=request.data)
        if new_movie.is_valid():
            new_movie.save()
            return Response({"OK": new_movie.data}, status=status.HTTP_201_CREATED)

        return Response({"empty field detected!!!": new_movie.errors.keys()}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        if request.data.get('id'):
            queryset = Movies.objects.filter(id=request.data.get('id')).first()
            if queryset:
                data = MovieSerializer(queryset, data=request.data)
                if data.is_valid():
                    data.save()
                    return Response({"OK": data.data}, status=status.HTTP_202_ACCEPTED)

                return Response({"OK": "data is invalid!"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"OK": "movie id not found"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_movie(request: Request, movie: int):
    queryset = Movies.objects.filter(pk=movie).first()
    if queryset:
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_204_NO_CONTENT)
