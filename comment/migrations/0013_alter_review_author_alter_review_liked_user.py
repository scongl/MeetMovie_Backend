# Generated by Django 4.1 on 2022-12-21 00:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("comment", "0012_alter_rating_value"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="review_author",
                to=settings.AUTH_USER_MODEL,
                verbose_name="作者",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="liked_user",
            field=models.ManyToManyField(
                related_name="review_liked_user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="点过赞的用户",
            ),
        ),
    ]
