# Generated by Django 4.1 on 2022-12-19 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("group", "0005_alter_group_avatar"),
    ]

    operations = [
        migrations.AddField(
            model_name="discussion",
            name="create_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="discussion",
            name="update_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="discussion",
            name="content",
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name="discussion",
            name="title",
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("content", models.CharField(max_length=10000)),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("update_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "discussion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="group.discussion",
                    ),
                ),
            ],
        ),
    ]