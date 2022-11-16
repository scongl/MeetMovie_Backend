from django.db import models
from account.models import UserInfo
from movie.models import Movie


class Rating(models.Model):
    VALUE_CHOICES = [
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
        (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)
    ]
    value = models.SmallIntegerField(choices=VALUE_CHOICES)                 # 提交的评分，十分制
    content = models.CharField(max_length=350, blank=True)                  # 附上的短评
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)       # 评论所属用户
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)              # 所评分的电影


class Review(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()                                            # 长评内容

    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        d = {"id": self.id, "title": self.title, "content": self.content,
             "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
             "update_at": self.update_at.strftime("%Y-%m-%d %H:%M:%S")}

        return d


class Reply(models.Model):
    content = models.TextField()
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        d = {"id": self.id, "content": self.content,
             "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
             "update_at": self.update_at.strftime("%Y-%m-%d %H:%M:%S")}

        return d

