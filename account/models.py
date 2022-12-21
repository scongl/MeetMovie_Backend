from django.db import models
from django.contrib.auth.models import AbstractUser
from movie.models import Movie, Genre
from celebrity.models import Celebrity


class UserInfo(AbstractUser):
    # AbstractUser已存在username, password, 标记是否是管理员等属性

    introduction = models.CharField(max_length=300, verbose_name="个人简介", blank=True)
    nickname = models.CharField(max_length=150, verbose_name='昵称')

    avatar = models.ImageField(upload_to='User/avatar/', default='User/avatar/initial.jpg', verbose_name='头像')

    prefer_genres = models.ManyToManyField(Genre, verbose_name='喜爱的电影类型')

    like_movies = models.ManyToManyField(Movie, verbose_name='收藏的电影')
    like_celebrities = models.ManyToManyField(Celebrity, verbose_name='收藏的影人')

    class Meta(AbstractUser.Meta):
        pass

    def to_dict(self):
        # 图片路径返回相对url
        d = {"id": self.id, "username": self.username, "nickname": self.nickname,
             "introduction": self.introduction, "avatar": self.avatar.url,
             "email": self.email, "create_at": self.date_joined.strftime("%Y-%m-%d %H:%M:%S")}

        return d

    def __str__(self):
        return self.username






