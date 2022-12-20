# Generated by Django 4.1 on 2022-12-20 18:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("movie", "0018_alter_genre_options_alter_movie_options_and_more"),
        ("group", "0008_discussion_likes"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment", options={"verbose_name": "回复", "verbose_name_plural": "回复"},
        ),
        migrations.AlterModelOptions(
            name="discussion",
            options={"verbose_name": "讨论", "verbose_name_plural": "讨论"},
        ),
        migrations.AlterModelOptions(
            name="group",
            options={"verbose_name": "兴趣小组", "verbose_name_plural": "兴趣小组"},
        ),
        migrations.AlterField(
            model_name="comment",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="作者",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="content",
            field=models.CharField(max_length=10000, verbose_name="内容"),
        ),
        migrations.AlterField(
            model_name="comment",
            name="create_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="创建于"),
        ),
        migrations.AlterField(
            model_name="comment",
            name="discussion",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="group.discussion",
                verbose_name="讨论",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="update_at",
            field=models.DateTimeField(auto_now=True, verbose_name="修改于"),
        ),
        migrations.AlterField(
            model_name="discussion",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="作者",
            ),
        ),
        migrations.AlterField(
            model_name="discussion",
            name="content",
            field=models.CharField(max_length=10000, verbose_name="内容"),
        ),
        migrations.AlterField(
            model_name="discussion",
            name="create_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="创建于"),
        ),
        migrations.AlterField(
            model_name="discussion",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="group.group",
                verbose_name="兴趣小组",
            ),
        ),
        migrations.AlterField(
            model_name="discussion",
            name="likes",
            field=models.IntegerField(default=0, verbose_name="点赞数"),
        ),
        migrations.AlterField(
            model_name="discussion",
            name="title",
            field=models.CharField(max_length=100, verbose_name="标题"),
        ),
        migrations.AlterField(
            model_name="discussion",
            name="update_at",
            field=models.DateTimeField(auto_now=True, verbose_name="修改于"),
        ),
        migrations.AlterField(
            model_name="group",
            name="avatar",
            field=models.ImageField(
                default="Group/avatar/initial.jpg",
                upload_to="Group/avatar/",
                verbose_name="小组封面",
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="create_at",
            field=models.DateField(auto_now_add=True, verbose_name="创建于"),
        ),
        migrations.AlterField(
            model_name="group",
            name="introduction",
            field=models.TextField(verbose_name="小组介绍"),
        ),
        migrations.AlterField(
            model_name="group",
            name="members",
            field=models.ManyToManyField(
                to=settings.AUTH_USER_MODEL, verbose_name="小组成员"
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="movie",
            field=models.ManyToManyField(to="movie.movie", verbose_name="电影"),
        ),
        migrations.AlterField(
            model_name="group",
            name="name",
            field=models.CharField(max_length=30, verbose_name="小组名"),
        ),
    ]