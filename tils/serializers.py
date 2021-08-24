from rest_framework import serializers

from .models import Til
from courses.models import MyCourse, ClipperSection, ClipperCourse
from courses.serializers import MyCourseSerializer, ClipperCourseSerializer
from accounts.models import CustomUser


class TilSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")
    mycourse = serializers.PrimaryKeyRelatedField(
        queryset=MyCourse.objects.all()
    )
    section = serializers.PrimaryKeyRelatedField(
        queryset=ClipperSection.objects.all()
    )
    course_title = serializers.SerializerMethodField()
    section_name = serializers.SerializerMethodField()
    site_name = serializers.SerializerMethodField()

    def get_course_title(self, obj):
        return obj.mycourse.course.title

    def get_section_name(self, obj):
        return obj.section.name

    def get_site_name(self, obj):
        return obj.mycourse.site.name

    class Meta:
        model = Til
        fields = [
            "id",
            "owner",
            "date",
            "star",
            "memo",
            "site_name",
            "mycourse",
            "course_title",
            "section",
            "section_name",
        ]
