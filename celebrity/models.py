from django.db import models


class Celebrity(models.Model):
    GENDER_CHOICES = [
        (0, "未知"),
        (1, "男"),
        (2, "女")
    ]

    celebrity_name = models.CharField(max_length=60)
    biography = models.TextField(blank=True)
    image = models.CharField(max_length=2047, blank=True)           # 名人图片url，长度大于4000一般使用TextField

    birthday = models.CharField(max_length=40, blank=True)
    place_of_birth = models.CharField(max_length=255, blank=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES)
    career = models.CharField(max_length=255, blank=True)

    def to_dict(self):
        d = {"celebrity_name": self.celebrity_name, "biography": self.biography, "image": self.image,
             "birthday": self.birthday, "place_of_birth": self.place_of_birth, "gender": self.gender,
             "career": self.career}
        return d


class CelebrityImage(models.Model):
    celebrity = models.ForeignKey(Celebrity, on_delete=models.CASCADE)
    path = models.CharField(max_length=2047)
