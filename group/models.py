from django.db import models
from account.models import UserInfo
from movie.models import Movie


class Group(models.Model):
    avatar = models.CharField(max_length=2047)          # 兴趣组的图片
    introduction = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    members = models.ManyToManyField(UserInfo)          # 小组成员
    movie = models.ManyToManyField(Movie)


class Discussion(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    content = models.TextField()
