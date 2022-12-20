from django.db import models
from celebrity.models import Celebrity


class Genre(models.Model):
    name = models.CharField(max_length=20, verbose_name='类型')          # 标签类型

    class Meta:
        verbose_name_plural = verbose_name = '电影类型'

    def to_dict(self):
        return {"id": self.id, "name": self.name}

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=20, verbose_name='语言')          # 语言


class Movie(models.Model):
    movie_name = models.CharField(max_length=60, verbose_name='电影名')
    overview = models.TextField(verbose_name='简介')
    release_date = models.DateField(verbose_name='发行日期')
    duration = models.SmallIntegerField(verbose_name='时长')                                       # 时长
    image = models.CharField(max_length=2047, verbose_name='封面图片路径')         # 封面图片url，长度大于4000一般使用TextField
    region = models.CharField(max_length=60, verbose_name='地区')                # 制片国家/地区(可能有多个，以'/'隔开)
    vote_sum = models.BigIntegerField(default=0, verbose_name='评分总和')         # 评分总和
    vote_count = models.BigIntegerField(default=0, verbose_name='评分数')         # 投票数

    celebrities = models.ManyToManyField(Celebrity, through="Position",
                                         verbose_name='演职人员')         # 电影和演员为多对多关系,指定中间表为Position
    genres = models.ManyToManyField(Genre, verbose_name='类型')                                      # 与标签形成多对多关系
    languages = models.ManyToManyField(Language, verbose_name='语言')                                # 语言

    class Meta:
        verbose_name_plural = verbose_name = '电影'

    def to_dict(self):
        d = {"id": self.id, "movie_name": self.movie_name, "image": self.image, "region": self.region,
             "vote_sum": self.vote_sum, "vote_count": self.vote_count, "duration": str(self.duration) + "分钟",
             "vote_average": self.vote_sum / self.vote_count if self.vote_count != 0 else 0.0,
             "overview": self.overview, "release_date": self.release_date.strftime("%Y-%m-%d")}

        return d

    def __str__(self):
        return self.movie_name


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
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='电影')
    path = models.CharField(max_length=2047, verbose_name='电影图片路径')

    class Meta:
        verbose_name_plural = verbose_name = '电影图片'

    def __str__(self):
        return self.movie


class MovieTrailer(models.Model):                                                 # 电影预告片表
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='电影')
    path = models.CharField(max_length=2047, verbose_name='电影预告片路径')

    class Meta:
        verbose_name_plural = verbose_name = '电影预告片'

    def __str__(self):
        return self.movie





