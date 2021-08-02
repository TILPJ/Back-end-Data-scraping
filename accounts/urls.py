from django.urls import path

from rest_auth.views import (
    UserDetailsView,
)

from .views import (
    UserCheck,
    LoginView,
    LogoutView,
    RegisterView,
    FindEmailView,
    PasswordChangeView,
)

urlpatterns = [
    path("api/email/check/", UserCheck.as_view(), name="rest_email_check"),
    path("api/login/", LoginView.as_view(), name="rest_login"),
    path("api/logout/", LogoutView.as_view(), name="rest_logout"),
    path("api/email/find/", FindEmailView.as_view(), name="find_email"),
    path(
        "api/password/change/",
        PasswordChangeView.as_view(),
        name="rest_password_change",
    ),
    path("api/registration/", RegisterView.as_view(), name="rest_register"),
    path("api/user/", UserDetailsView.as_view(), name="rest_user_details"),
]
