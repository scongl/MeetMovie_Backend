from django.db import models
from account.models import UserInfo
from movie.models import Movie


class Group(models.Model):
    avatar = models.ImageField(upload_to='Group/avatar/', default='Group/avatar/initial.jpg',
                               verbose_name='小组封面')          # 兴趣组的封面
    introduction = models.TextField(verbose_name='小组介绍')
    name = models.CharField(max_length=30, verbose_name='小组名')
    create_at = models.DateField(auto_now_add=True, verbose_name='创建于')

    members = models.ManyToManyField(UserInfo, verbose_name='小组成员')          # 小组成员
    movie = models.ManyToManyField(Movie, verbose_name='电影')               # 关于电影的兴趣小组

    class Meta:
        verbose_name_plural = verbose_name = '兴趣小组'

    def to_dict(self):
        d = {"id": self.id, "avatar": self.avatar.url, "create_at": self.create_at.strftime("%Y-%m-%d"),
             "introduction": self.introduction, "name": self.name}
        return d

    def __str__(self):
        return self.name


class Discussion(models.Model):
    # 帖子
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='兴趣小组')
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='作者', related_name='discussion_author')

    title = models.CharField(max_length=100, verbose_name='标题')
    content = models.CharField(max_length=10000, verbose_name='内容')

    liked_user = models.ManyToManyField(UserInfo, verbose_name='点过赞的人', related_name='discussion_liked_user')

    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建于')
    update_at = models.DateTimeField(auto_now=True, verbose_name='修改于')

    class Meta:
        verbose_name_plural = verbose_name = '讨论'

    def to_dict(self):
        d = {"id": self.id, "content": self.content, "title": self.title, "likes": self.liked_user.count(),
             "comment_count": self.comment_set.count(),
             "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
             "update_at": self.update_at.strftime("%Y-%m-%d %H:%M:%S")}
        return d

    def __str__(self):
        return self.title


class Comment(models.Model):
    # 帖子的回复
    content = models.CharField(max_length=10000, verbose_name='内容')
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='作者')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, verbose_name='讨论')

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

