import jsend
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from courses.models import ClipperSite
from .models import Til
from .serializers import TilSerializer


class TilList(GenericAPIView):
    serializer_class = TilSerializer
    permission_classes = (IsAuthenticated,)

    # 1. 조회 조건이 없으면 모든 강의의 til이 최신순으로 조회됨
    # 2. site 필터링 조건이 있으면 해당 사이트의 모든 강의의 til이 최신순으로 조회됨
    # 3. star 필터링 조건이 있으면 북마크가 되어있는 til만 조회됨
    def get(self, request, format=None):
        if request.query_params:
            filter_param = self.request.query_params.get("filter", default="None")
            site_param = self.request.query_params.get("site", default="all")

            # site로 필터링
            if site_param != "all":
                try:
                    site_id = ClipperSite.objects.get(name=site_param).id
                except:
                    res = jsend.fail(data={"detail": "site does not exist."})
                    return Response(res)

                tils = Til.objects.filter(
                    owner=request.user, mycourse__site=site_id
                ).order_by("-date")
            else:
                tils = Til.objects.filter(owner=request.user).order_by("-date")

            # 북마크로 필터링
            if filter_param == "star":
                tils = tils.filter(star=True).order_by("-date")

            serializer = TilSerializer(tils, many=True)
            res = jsend.success(data={"tils": serializer.data})
            return Response(res)

        # 필터링 조건이 없는 경우, 모든 강의에 등록한 til을 최신순으로 정렬
        tils = Til.objects.filter(owner=request.user).order_by("-date")
        serializer = TilSerializer(tils, many=True)
        res = jsend.success(data={"tils": serializer.data})
        return Response(res)

    def post(self, request, format=None):
        serializer = TilSerializer(data=request.data)
        if serializer.is_valid() == False:
            res = jsend.fail(data=serializer.errors)
            return Response(res)

        serializer.save(owner=request.user)
        res = jsend.success(data={"detail": _("Successfully registered.")})
        return Response(res)


class TilDetail(GenericAPIView):
    serializer_class = TilSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, til_id):
        til = Til.objects.get(pk=til_id)
        return til

    def get(self, request, til_id, format=None):
        try:
            til = self.get_object(til_id)
        except:
            res = jsend.fail(data={"detail": _("This is not a registered")})
            return Response(res)

        serializer = TilSerializer(til)
        res = jsend.success(data=serializer.data)
        return Response(res)

    def put(self, request, til_id, format=None):
        try:
            til = self.get_object(til_id)
        except:
            res = jsend.fail(data={"detail": _("This is not a registered")})
            return Response(res)

        serializer = TilSerializer(til, data=request.data)
        if serializer.is_valid() == False:
            res = jsend.fail(data=serializer.errors)
            return Response(res)
        serializer.save()
        res = jsend.success(data={"detail": _("Successfully modified.")})
        return Response(res)

    def delete(self, request, til_id, format=None):
        try:
            til = self.get_object(til_id)
        except:
            res = jsend.fail(data={"detail": _("This is not a registered")})
            return Response(res)

        til.delete()
        res = jsend.success(data={"detail": _("Successfully deleted.")})
        return Response(res)
