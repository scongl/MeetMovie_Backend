# Generated by Django 4.1 on 2022-11-15 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("comment", "0005_review_title"),
    ]

    operations = [
        migrations.RenameField(
            model_name="reply", old_name="user_info", new_name="author",
        ),
        migrations.RenameField(
            model_name="review", old_name="user_info", new_name="author",
        ),
    ]
