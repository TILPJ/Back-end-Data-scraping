import jsend
from django.conf import settings
from django.contrib.auth import login as django_login, logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from rest_framework import response
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView

from allauth.account import app_settings as allauth_settings
from rest_auth.app_settings import TokenSerializer

from rest_auth.views import LoginView, LogoutView, PasswordChangeView
from rest_auth.registration.views import RegisterView

from .models import CustomUser
from .serializers import (
    UserCheckSerializer,
    FindEmailSerializer,
    PasswordChangeSerializer,
)


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "email_check": reverse("rest_email_check", request=request, format=format),
            "login": reverse("rest_login", request=request, format=format),
            "logout": reverse("rest_logout", request=request, format=format),
            "find_email": reverse("find_email", request=request, format=format),
            "password_change": reverse(
                "rest_password_change", request=request, format=format
            ),
            "register": reverse("rest_register", request=request, format=format),
            "logged_in_user": reverse(
                "rest_user_details", request=request, format=format
            ),
            "mycourses": reverse("mycourse_list", request=request, format=format),
            "sites": reverse("site_list", request=request, format=format),
            "courses": reverse("course_list", request=request, format=format),
            "sections": reverse("section_list", request=request, format=format),
            "tils": reverse("til_list", request=request, format=format),
            "mysites": reverse("mysite_list", request=request, format=format),
        }
    )


# 회원 여부 체크
class UserCheck(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        if not self.request.query_params:
            res = jsend.fail(data={"message": "Please enter your email"})
            return Response(res)

        email_param = self.request.query_params.get("email", default="")
        email = CustomUser.objects.filter(email=email_param)
        serializer = UserCheckSerializer(email)
        res = jsend.success(data=serializer.data)
        return Response(res)


# 로그인
# rest_auth.views.LoginView overriding
class LoginView(LoginView):
    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, "REST_USE_JWT", False):
            data = {"user": self.user, "token": self.token}
            serializer = serializer_class(
                instance=data, context={"request": self.request}
            )
        else:
            serializer = serializer_class(
                instance=self.token, context={"request": self.request}
            )

        res = jsend.success(data=serializer.data)  # jsend 적용
        response = Response(res, status=status.HTTP_200_OK)
        if getattr(settings, "REST_USE_JWT", False):
            from rest_framework_jwt.settings import api_settings as jwt_settings

            if jwt_settings.JWT_AUTH_COOKIE:
                from datetime import datetime

                expiration = datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA
                response.set_cookie(
                    jwt_settings.JWT_AUTH_COOKIE,
                    self.token,
                    expires=expiration,
                    httponly=True,
                )
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(
            data=self.request.data, context={"request": request}
        )
        if self.serializer.is_valid(raise_exception=False) == False:
            res = jsend.fail(data=self.serializer.errors)  # jsend 적용
            return Response(res)

        self.login()
        return self.get_response()


# 로그아웃
# rest_auth.views.LogoutView overriding
class LogoutView(LogoutView):
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, "REST_SESSION_LOGIN", True):
            django_logout(request)

        res = jsend.success(data={"detail": _("Successfully logged out.")})  # jsend 적용
        response = Response(res, status=status.HTTP_200_OK)
        if getattr(settings, "REST_USE_JWT", False):
            from rest_framework_jwt.settings import api_settings as jwt_settings

            if jwt_settings.JWT_AUTH_COOKIE:
                response.delete_cookie(jwt_settings.JWT_AUTH_COOKIE)
        return response


# 회원 가입
# rest_auth.registration.views.RegisterView overriding
class RegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=False) == False:
            res = jsend.fail(data=serializer.errors)  # jsend 적용
            return Response(res)

        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        res = jsend.success(self.get_response_data(user))  # jsend 적용
        return Response(res, status=status.HTTP_201_CREATED, headers=headers)


# 이메일 찾기
class FindEmailView(GenericAPIView):
    serializer_class = FindEmailSerializer
    permissions = (AllowAny,)

    def get_object(self, request):
        user_email = CustomUser.objects.filter(
            phone_number=request.data["phone_number"],
            date_of_birth=request.data["date_of_birth"],
        )
        return user_email

    def post(self, request, format=None):
        serializer = FindEmailSerializer(data=request.data)  # input 유효성 검사
        if serializer.is_valid() == False:
            res = jsend.fail(data=serializer.errors)
            return Response(res)

        user_email = self.get_object(request)
        serializer = FindEmailSerializer(user_email)
        res = jsend.success(data=serializer.data)
        return Response(res)


# 비밀번호 변경
# rest_auth.views.PasswordChangeView overriding
class PasswordChangeView(PasswordChangeView):
    serializer_class = PasswordChangeSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=False) == False:
            res = jsend.fail(data=serializer.errors)  # jsend 적용
            return Response(res)

        serializer.save()
        res = jsend.success(
            data={"detail": _("New password has been saved.")}
        )  # jsend 적용
        return Response(res)
