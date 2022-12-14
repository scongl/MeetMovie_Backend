# Generated by Django 4.1 on 2022-12-21 00:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("group", "0009_alter_comment_options_alter_discussion_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="discussion", name="likes",),
        migrations.AddField(
            model_name="discussion",
            name="liked_user",
            field=models.ManyToManyField(
                related_name="discussion_liked_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="点过赞的人",
            ),
        ),
        migrations.AlterField(
            model_name="discussion",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="discussion_author",
                to=settings.AUTH_USER_MODEL,
                verbose_name="作者",
            ),
        ),
    ]
