# Generated by Django 4.1 on 2022-10-23 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("celebrity", "0002_celebrity_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="celebrity",
            name="celebrity_name",
            field=models.CharField(max_length=60),
        ),
    ]
