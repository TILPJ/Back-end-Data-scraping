import jsend
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import ClipperSite, ClipperCourse, ClipperSection, MyCourse
from .serializers import (
    ClipperCourseSerializer,
    ClipperSiteSerializer,
    ClipperSectionSerializer,
    MyCourseSerializer,
    MySiteSerializer,
)


class SiteList(GenericAPIView):
    serializer_class = ClipperSiteSerializer
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        # 사이트명으로 검색하는 경우
        if request.query_params:
            search_param = self.request.query_params.get("search", default="")
            sites = ClipperSite.objects.filter(
                Q(name__icontains=search_param)
            ).distinct()
            serializer = ClipperSiteSerializer(sites, many=True)
            res = jsend.success(data={"sites": serializer.data})
            return Response(res)

        # 검색 조건이 없는 경우
        sites = ClipperSite.objects.all()
        serializer = ClipperSiteSerializer(sites, many=True)
        res = jsend.success(data={"sites": serializer.data})
        return Response(res)


class CourseList(GenericAPIView):
    serializer_class = ClipperCourseSerializer
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        # 강의명으로 검색하거나, 학습사이트별로 필터링하는 경우
        if request.query_params:
            search_param = self.request.query_params.get("search", default="")
            site_param = self.request.query_params.get("site", default="")
            if site_param != "":
                try:
                    site_id = ClipperSite.objects.get(name=site_param).id
                except:
                    res = jsend.fail(data={"detail": "site does not exist."})
                    return Response(res)
            else:
                site_id = 1
            courses = ClipperCourse.objects.filter(
                Q(title__icontains=search_param) & Q(site_id=site_id)
            )
            serializer = ClipperCourseSerializer(courses, many=True)
            res = jsend.success(data={"courses": serializer.data})
            return Response(res)

        # 검색 또는 필터링 조건이 없는 경우
        courses = ClipperCourse.objects.all()
        serializer = ClipperCourseSerializer(courses, many=True)
        res = jsend.success(data={"courses": serializer.data})
        return Response(res)


class SectionList(GenericAPIView):
    serializer_class = ClipperSectionSerializer
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        # 강의별로 필터링
        if request.query_params:
            course_param = int(self.request.query_params.get("course", default=0))
            sections = ClipperSection.objects.filter(chapter__course=course_param)
            serializer = ClipperSectionSerializer(sections, many=True)
            res = jsend.success(data={"sections": serializer.data})
            return Response(res)
        else:
            res = jsend.fail(data={"detail": _("Please enter the course id.")})
            return Response(res)


class MySiteList(GenericAPIView):
    serializer_class = MySiteSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, fotmat=None):
        sites = MyCourse.objects.filter(owner=request.user).distinct("site")
        serializer = MySiteSerializer(sites, many=True)
        res = jsend.success(data={"mysites": serializer.data})
        return Response(res)


class MyCourseList(GenericAPIView):
    serializer_class = MyCourseSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        mycourse = MyCourse.objects.filter(owner=request.user)
        serializer = MyCourseSerializer(mycourse, many=True)
        res = jsend.success(data={"mycourses": serializer.data})
        return Response(res)

    def post(self, request, format=None):
        serializer = MyCourseSerializer(data=request.data)
        if serializer.is_valid() == False:
            res = jsend.fail(data=serializer.errors)
            return Response(res)

        serializer.save(owner=request.user)
        res = jsend.success(data={"detail": _("Successfully registered.")})
        return Response(res)


class MyCourseDetail(GenericAPIView):
    serializer_class = MyCourseSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, mycourse_id):
        mycourse = MyCourse.objects.get(pk=mycourse_id)
        return mycourse

    def get(self, request, mycourse_id, format=None):
        try:
            mycourse = self.get_object(mycourse_id)
        except:
            res = jsend.fail(data={"detail": _("This is not a registered")})
            return Response(res)

        serializer = MyCourseSerializer(mycourse)
        res = jsend.success(data=serializer.data)
        return Response(res)

    def put(self, request, mycourse_id, format=None):
        try:
            mycourse = self.get_object(mycourse_id)
        except:
            res = jsend.fail(data={"detail": _("This is not a registered")})
            return Response(res)

        serializer = MyCourseSerializer(mycourse, data=request.data)
        if serializer.is_valid() == False:
            res = jsend.fail(data=serializer.errors)
            return Response(res)
        serializer.save()
        res = jsend.success(data={"detail": _("Successfully modified.")})
        return Response(res)

    def delete(self, request, mycourse_id, format=None):
        try:
            mycourse = self.get_object(mycourse_id)
        except:
            res = jsend.fail(data={"detail": _("This is not a registered")})
            return Response(res)

        mycourse.delete()
        res = jsend.success(data={"detail": _("Successfully deleted.")})
        return Response(res)
