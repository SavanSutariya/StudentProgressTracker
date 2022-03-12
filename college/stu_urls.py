from django.urls import URLPattern, path
from . import studentViews

urlpatterns = [
    path('', studentViews.Home, name="student-home"),
]


