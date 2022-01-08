from django.urls import path
from .adminViews import *
urlpatterns = [
    # college-admin urls
    path('' ,Home, name="college-home"),
    path('course/<int:pk>/',subjects_list, name="subjects-list"),
    path('courses/',Course_list, name="college-course-list"),
]
