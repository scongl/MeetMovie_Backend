# Generated by Django 4.1 on 2022-11-03 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie", "0009_alter_movie_vote_average_alter_movie_vote_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="vote_average",
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=8),
        ),
    ]
