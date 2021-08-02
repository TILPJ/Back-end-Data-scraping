from rest_framework import serializers

from .models import ClipperSite, ClipperCourse, ClipperChapter, ClipperSection, MyCourse


class ClipperSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClipperSite
        fields = ["id", "name"]


class ClipperCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClipperCourse
        fields = [
            "id",
            "title",
            "instructor",
            "thumbnail_link",
            "description",
            "course_link",
        ]


class ClipperSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClipperSection
        fields = ["id", "name"]


class MyCourseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")
    site_info = ClipperSiteSerializer(source="site", read_only=True)
    course_info = ClipperCourseSerializer(source="course", read_only=True)
    site = serializers.PrimaryKeyRelatedField(
        queryset=ClipperSite.objects.all(), write_only=True
    )
    course = serializers.PrimaryKeyRelatedField(
        queryset=ClipperCourse.objects.all(), write_only=True
    )

    class Meta:
        model = MyCourse
        fields = ["id", "owner", "site", "course", "site_info", "course_info"]


class MySiteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")
    site_name = serializers.SerializerMethodField()

    def get_site_name(self, obj):
        return obj.site.name

    class Meta:
        model = MyCourse
        fields = ["owner", "site_name"]
