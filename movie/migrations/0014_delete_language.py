# Generated by Django 4.1 on 2022-11-17 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("movie", "0013_language_alter_movie_duration"),
    ]

    operations = [
        migrations.DeleteModel(name="Language",),
    ]
