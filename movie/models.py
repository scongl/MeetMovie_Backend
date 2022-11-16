from django.db import models
from celebrity.models import Celebrity


class Genre(models.Model):
    name = models.CharField(max_length=20)          # 标签类型


class Movie(models.Model):
    movie_name = models.CharField(max_length=60)
    overview = models.TextField()
    release_date = models.CharField(max_length=20)
    duration = models.CharField(max_length=20)                                  # 时长，形式类似1H30M, 2H0M等表示小时和分钟
    image = models.CharField(max_length=2047)                                   # 封面图片url，长度大于4000一般使用TextField
    region = models.CharField(max_length=60)                                    # 制片国家/地区(可能有多个，以'/'隔开)
    vote_sum = models.BigIntegerField(default=0)                                                # 评分总和
    vote_count = models.BigIntegerField(default=0)                                              # 投票数

    celebrities = models.ManyToManyField(Celebrity, through="Position")         # 电影和演员为多对多关系,指定中间表为Position
    genres = models.ManyToManyField(Genre)                                      # 与标签形成多对多关系


class Position(models.Model):
    POSITION_CHOICES = [
        (0, '导演'),
        (1, '编剧'),
        (2, '参演')
    ]

    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    position = models.SmallIntegerField(choices=POSITION_CHOICES)


class MovieImage(models.Model):                                                   # 电影图片表
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    path = models.CharField(max_length=2047)


class MovieTrailer(models.Model):                                                 # 电影预告片表
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    path = models.CharField(max_length=2047)





