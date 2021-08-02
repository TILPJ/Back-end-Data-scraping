from django.db import models
from conf.settings import base


class Til(models.Model):
    owner = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    date = models.DateField()
    mycourse = models.ForeignKey("courses.MyCourse", on_delete=models.CASCADE)
    section = models.ForeignKey("courses.ClipperSection", on_delete=models.CASCADE)
    star = models.BooleanField(default=False)
    memo = models.TextField(blank=True)

    def __str__(self):
        return self.memo
