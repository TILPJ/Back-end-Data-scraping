from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns = [
    path("", views.TilList.as_view(), name="til_list"),
    path("<int:til_id>/", views.TilDetail.as_view()),
]
