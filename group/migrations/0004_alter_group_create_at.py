# Generated by Django 4.1 on 2022-11-18 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("group", "0003_discussion_content_discussion_title_group_movie"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="create_at",
            field=models.DateField(auto_now_add=True),
        ),
    ]
