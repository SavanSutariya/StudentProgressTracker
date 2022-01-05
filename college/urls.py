from django.urls import path
from .adminViews import *
urlpatterns = [
    path("",Home, name="college-home"),
]
