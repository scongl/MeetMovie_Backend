from django.db import models


class Celebrity(models.Model):
    GENDER_CHOICES = [
        (0, "未知"),
        (1, "男"),
        (2, "女")
    ]

    celebrity_name = models.CharField(max_length=60, verbose_name='姓名')
    biography = models.TextField(blank=True, verbose_name='介绍')
    image = models.CharField(max_length=2047, blank=True, verbose_name='图片路径')           # 名人图片url，长度大于4000一般使用TextField

    birthday = models.CharField(max_length=40, blank=True, verbose_name='出生日期')
    place_of_birth = models.CharField(max_length=255, blank=True, verbose_name='出生地')
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, verbose_name='性别')
    career = models.CharField(max_length=255, blank=True, verbose_name='职业')

    class Meta:
        verbose_name_plural = verbose_name = '影人'

    def to_dict(self):
        d = {"celebrity_name": self.celebrity_name, "biography": self.biography, "image": self.image,
             "birthday": self.birthday, "place_of_birth": self.place_of_birth, "gender": self.gender,
             "career": self.career, "id": self.id}
        return d

    def __str__(self):
        return self.celebrity_name


class CelebrityImage(models.Model):
    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE, verbose_name='影人')
    path = models.CharField(max_length=2047, verbose_name='图片路径')

    class Meta:
        verbose_name_plural = verbose_name = '影人图片'

    def __str__(self):
        return self.celebrity.celebrity_name
