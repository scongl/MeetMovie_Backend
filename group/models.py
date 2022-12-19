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
    # 帖子
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    content = models.CharField(max_length=10000)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        d = {"id": self.id, "content": self.content, "title": self.title,
             "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
             "update_at": self.update_at.strftime("%Y-%m-%d %H:%M:%S")}
        return d


class Comment(models.Model):
    # 帖子的回复
    content = models.CharField(max_length=10000)
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        d = {"id": self.id, "content": self.content,
             "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
             "update_at": self.update_at.strftime("%Y-%m-%d %H:%M:%S")}
        return d

