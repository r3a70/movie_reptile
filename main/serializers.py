from rest_framework import serializers
from .models import Movies, Tags, Country, Actors, Links


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ['id', 'name', 'post_url', 'post_image', 'age', 'imdb', 'rating', 'site_rate', 'like', 'dislike',
                  'director']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['movie_id', 'tag']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['movie_id', 'country']


class ActorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actors
        fields = ['movie_id', 'actor']


class LinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = ['movie_id', 'link']
