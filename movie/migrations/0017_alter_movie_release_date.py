# Generated by Django 4.1 on 2022-11-17 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie", "0016_movie_languages"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie", name="release_date", field=models.DateField(),
        ),
    ]
