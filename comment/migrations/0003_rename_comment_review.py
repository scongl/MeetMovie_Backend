# Generated by Django 4.1 on 2022-11-14 07:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("movie", "0011_movietrailer_movieimage"),
        ("comment", "0002_comment"),
    ]

    operations = [
        migrations.RenameModel(old_name="Comment", new_name="Review",),
    ]
