from rest_framework import serializers
from .models import Movies, Tags, Country, Actors, Links


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ("__all__")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ("__all__")


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("__all__")


class ActorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actors
        fields = ("__all__")


class LinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = ("__all__")
