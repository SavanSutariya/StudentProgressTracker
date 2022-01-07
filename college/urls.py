from django.urls import path
from .adminViews import *
urlpatterns = [
    # college-admin urls
    path('',Home, name="college-home"),
    path('course/<int:pk>/',Course_details, name="college-course-detail"),
    path('courses/',Course_list, name="college-course-list"),
]
