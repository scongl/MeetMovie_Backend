from django.db import models
from django.contrib.auth.models import AbstractUser
from movie.models import Movie, Genre
from celebrity.models import Celebrity


class UserInfo(AbstractUser):
    # AbstractUser已存在username, password, 标记是否是管理员等属性
    # 暂时未添加avatar字段

    introduction = models.CharField(max_length=300, verbose_name="个人简介", blank=True)
    nickname = models.CharField(max_length=150)

    avatar = models.CharField(max_length=2047)

    prefer_genres = models.ManyToManyField(Genre)

    like_movies = models.ManyToManyField(Movie)
    like_celebrities = models.ManyToManyField(Celebrity)

    class Meta(AbstractUser.Meta):
        pass

    def to_dict(self):
        d = {"id": self.id, "username": self.username, "nickname": self.nickname,
             "introduction": self.introduction, "avatar": self.avatar,
             "email": self.email, "create_at": self.date_joined.strftime("%Y-%m-%d %H:%M:%S")}

        return d








