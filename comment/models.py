from django.db import models
from account.models import UserInfo
from movie.models import Movie


class Rating(models.Model):
    VALUE_CHOICES = [
        (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
        (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)
    ]
    value = models.SmallIntegerField(choices=VALUE_CHOICES, verbose_name='评分')                 # 提交的评分，十分制
    content = models.CharField(max_length=350, blank=True, verbose_name='内容')                  # 附上的短评

    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建于')
    update_at = models.DateTimeField(auto_now=True, verbose_name='修改于')

    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='作者')       # 评论所属用户
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='电影')              # 所评分的电影

    class Meta:
        verbose_name_plural = verbose_name = '短评'

    def to_dict(self):
        d = {"value": self.value, "content": self.content,
             "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
             "update_at": self.update_at.strftime("%Y-%m-%d %H:%M:%S")}
        return d

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        is_create = self.id is None

        super().save(*args, **kwargs)

        if is_create:
            self.movie.vote_sum += self.value
            self.movie.vote_count += 1
            self.movie.save()

    def delete(self, *args, **kwargs):
        self.movie.vote_sum -= self.value
        self.movie.vote_count -= 1
        self.movie.save()
        super().delete(*args, **kwargs)


class Review(models.Model):
    title = models.CharField(max_length=500, verbose_name='标题')
    content = models.TextField(verbose_name='内容')                                            # 长评内容

    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='作者', related_name='review_author')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='电影')

    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建于')
    update_at = models.DateTimeField(auto_now=True, verbose_name='修改于')

    liked_user = models.ManyToManyField(UserInfo, verbose_name='点过赞的用户', related_name='review_liked_user')

    class Meta:
        verbose_name_plural = verbose_name = '影评'

    def to_dict(self):
        d = {"id": self.id, "title": self.title, "content": self.content,
             "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
             "update_at": self.update_at.strftime("%Y-%m-%d %H:%M:%S"),
             "likes": self.liked_user.count(), "reply_count": self.reply_set.count()}

        return d

    def __str__(self):
        return self.title


class Reply(models.Model):
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='作者')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, verbose_name='回复的影评')

    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建于')
    update_at = models.DateTimeField(auto_now=True, verbose_name='修改于')

    class Meta:
        verbose_name_plural = verbose_name = '回复'

    def to_dict(self):
        d = {"id": self.id, "content": self.content,
             "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
             "update_at": self.update_at.strftime("%Y-%m-%d %H:%M:%S")}

        return d

    def __str__(self):
        return self.content
