# Generated by Django 4.1 on 2022-11-15 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie", "0012_remove_movie_vote_average_movie_vote_sum_and_more"),
        ("celebrity", "0009_celebrityimage"),
        ("account", "0004_userinfo_prefer_genres"),
    ]

    operations = [
        migrations.AddField(
            model_name="userinfo",
            name="like_celebrities",
            field=models.ManyToManyField(to="celebrity.celebrity"),
        ),
        migrations.AddField(
            model_name="userinfo",
            name="like_movies",
            field=models.ManyToManyField(to="movie.movie"),
        ),
    ]
