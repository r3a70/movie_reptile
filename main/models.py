from django.db import models


class Movies(models.Model):
    name = models.CharField(max_length=500)
    post_url = models.CharField(max_length=500)
    post_image = models.CharField(max_length=500)
    tags = models.ForeignKey("Tags", on_delete=models.SET_NULL, null=True, related_name="tag_id")
    age = models.CharField(max_length=500)
    country = models.ForeignKey("Country", on_delete=models.SET_NULL, null=True, related_name="country_id")
    imdb = models.CharField(max_length=500)
    rating = models.CharField(max_length=500)
    site_rate = models.CharField(max_length=500)
    like = models.IntegerField()
    dislike = models.IntegerField()
    actors = models.ForeignKey("Actors", on_delete=models.SET_NULL, null=True, related_name="actor_id")
    director = models.CharField(max_length=500)
    story = models.TextField()
    links = models.ForeignKey("Links", on_delete=models.SET_NULL, null=True, related_name="link_id")

    class Meta:
        db_table = 'movies'


class Tags(models.Model):
    movie_id = models.IntegerField()
    tag = models.CharField(max_length=1024)

    class Meta:
        db_table = 'tags'


class Country(models.Model):
    movie_id = models.IntegerField()
    country = models.CharField(max_length=1024)

    class Meta:
        db_table = 'country'


class Actors(models.Model):
    movie_id = models.IntegerField()
    actor = models.CharField(max_length=2048)

    class Meta:
        db_table = 'actors'


class Links(models.Model):
    movie_id = models.IntegerField()
    link = models.CharField(max_length=2048)

    class Meta:
        db_table = 'links'
