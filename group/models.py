from django.db import models
from account.models import UserInfo
from movie.models import Movie


class Group(models.Model):
    avatar = models.ImageField(upload_to='Group/avatar/', default='Group/avatar/initial.jpg')          # 兴趣组的封面
    introduction = models.TextField()
    create_at = models.DateField(auto_now_add=True)

    members = models.ManyToManyField(UserInfo)          # 小组成员
    movie = models.ManyToManyField(Movie)               # 关于电影的兴趣小组

    def to_dict(self):
        d = {"id": self.id, "avatar": self.avatar.url, "create_at": self.create_at.strftime("%Y-%m-%d"),
             "introduction": self.introduction}
        return d


class Discussion(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    content = models.TextField()
