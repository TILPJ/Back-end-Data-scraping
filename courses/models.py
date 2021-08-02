from django.db import models

# inspectdb를 사용하여 외부 앱의 모델을 가져옴
# data scraping을 수행하는 clipper app의 model들
# Site, Course, Chapter, Section
class ClipperSite(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = "clipper_site"

    def __str__(self):
        return self.name


class ClipperCourse(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=500)
    thumbnail_link = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    instructor = models.CharField(max_length=300, blank=True, null=True)
    course_link = models.CharField(max_length=500)
    site = models.ForeignKey("ClipperSite", on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "clipper_course"

    def __str__(self):
        return self.title


class ClipperChapter(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=500)
    course = models.ForeignKey("ClipperCourse", on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "clipper_chapter"

    def __str__(self):
        return self.name


class ClipperSection(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=500)
    chapter = models.ForeignKey("ClipperChapter", on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "clipper_section"

    def __str__(self):
        return self.name


# 학습 카드
class MyCourse(models.Model):
    owner = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    site = models.ForeignKey("ClipperSite", on_delete=models.CASCADE)
    course = models.ForeignKey("ClipperCourse", on_delete=models.CASCADE)

    def __str__(self):
        return self.course.title
