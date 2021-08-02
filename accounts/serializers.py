from django.utils import translation
from django.conf import settings

from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator
from rest_auth.serializers import LoginSerializer, PasswordChangeSerializer
from rest_auth.registration.serializers import RegisterSerializer

from .models import CustomUser


class UserCheckSerializer(serializers.ModelSerializer):
    email_check = serializers.SerializerMethodField()

    def get_email_check(self, instance):
        if instance:
            return True
        else:
            return False

    class Meta:
        model = CustomUser
        fields = ["email_check"]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone_number", "date_of_birth"]


class LoginSerializer(LoginSerializer):
    username = None

    class Meta:
        model = CustomUser
        fields = ["id", "email", "password"]


class RegisterSerializer(RegisterSerializer):
    username = None
    password1 = serializers.CharField(write_only=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})
    phone_number = serializers.CharField(
        max_length=11,
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(),
                message=("Phone number already exists"),
            )
        ],
    )
    date_of_birth = serializers.CharField(max_length=8)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "password1",
            "password2",
            "phone_number",
            "date_of_birth",
        ]

    def save(self, request):
        user = super().save(request)
        user.phone_number = self.data.get("phone_number")
        user.date_of_birth = self.data.get("date_of_birth")
        user.save()
        return user


class FindEmailSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    phone_number = serializers.CharField(max_length=11, write_only=True)
    date_of_birth = serializers.CharField(max_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["user_email", "phone_number", "date_of_birth"]

    def get_user_email(self, instance):
        if instance:
            return instance[0].email
        else:
            return None


class PasswordChangeSerializer(PasswordChangeSerializer):
    user_email = serializers.EmailField(write_only=True)
    new_password1 = serializers.CharField(
        max_length=128, style={"input_type": "password"}
    )
    new_password2 = serializers.CharField(
        max_length=128, style={"input_type": "password"}
    )

    def __init__(self, *args, **kwargs):
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)
        user_email = self.request.data.get("user_email")
        if user_email:
            self.user = CustomUser.objects.get(email=user_email)
