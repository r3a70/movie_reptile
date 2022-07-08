# Generated by Django 4.0.5 on 2022-07-08 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
                ('actor', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'actors',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
                ('country', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
                ('link', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'links',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
                ('tag', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('post_url', models.CharField(max_length=255)),
                ('post_image', models.CharField(max_length=255)),
                ('age', models.CharField(max_length=255)),
                ('imdb', models.CharField(max_length=255)),
                ('rating', models.CharField(max_length=255)),
                ('site_rate', models.CharField(max_length=255)),
                ('like', models.IntegerField()),
                ('dislike', models.IntegerField()),
                ('director', models.CharField(max_length=255)),
                ('story', models.TextField()),
                ('actors', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actor_id', to='main.actors')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='country_id', to='main.country')),
                ('links', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_id', to='main.links')),
                ('tags', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_id', to='main.tags')),
            ],
            options={
                'db_table': 'movies',
            },
        ),
    ]
