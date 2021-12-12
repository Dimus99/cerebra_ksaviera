from django.urls import path

from api import views

urlpatterns = [
    path("get_variants/", views.mix_variants),
    path("get_open_requests/", views.mix_open_requests),
    path("", views.index, name="index"),
]
