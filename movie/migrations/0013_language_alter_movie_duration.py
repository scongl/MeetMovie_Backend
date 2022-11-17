# Generated by Django 4.1 on 2022-11-17 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie", "0012_remove_movie_vote_average_movie_vote_sum_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name="movie", name="duration", field=models.SmallIntegerField(),
        ),
    ]
