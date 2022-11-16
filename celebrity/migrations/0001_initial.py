# Generated by Django 4.1 on 2022-10-23 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Celebrity",
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
                ("celebrity_name", models.CharField(max_length=50)),
                ("introduction", models.CharField(max_length=1023)),
            ],
        ),
    ]
