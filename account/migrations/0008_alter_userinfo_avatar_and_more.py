# Generated by Django 4.1 on 2022-12-20 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "celebrity",
            "0010_alter_celebrity_options_alter_celebrityimage_options_and_more",
        ),
        ("movie", "0018_alter_genre_options_alter_movie_options_and_more"),
        ("account", "0007_alter_userinfo_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinfo",
            name="avatar",
            field=models.ImageField(
                default="User/avatar/initial.jpg",
                upload_to="User/avatar/",
                verbose_name="头像",
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="like_celebrities",
            field=models.ManyToManyField(
                to="celebrity.celebrity", verbose_name="收藏的影人"
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="like_movies",
            field=models.ManyToManyField(to="movie.movie", verbose_name="收藏的电影"),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="nickname",
            field=models.CharField(max_length=150, verbose_name="昵称"),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="prefer_genres",
            field=models.ManyToManyField(to="movie.genre", verbose_name="喜爱的电影类型"),
        ),
    ]