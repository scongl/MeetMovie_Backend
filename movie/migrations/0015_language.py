# Generated by Django 4.1 on 2022-11-17 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie", "0014_delete_language"),
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
    ]