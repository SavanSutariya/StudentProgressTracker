from django.urls import path
from . import adminViews

urlpatterns = [
    # college-admin urls
    path('' ,adminViews.Home, name="college-home"),
    path('courses/',adminViews.Course_list, name="college-course-list"),
    path('course/<int:pk>/',adminViews.subjects_list, name="subjects-list"),
    path('course/addsubject/<int:pk>',adminViews.add_subject,name="add-subject"),
    path('students/',adminViews.students_list,name="college-students-list"),
    path('faculties/',adminViews.faculties_list,name="college-faculties-list"),
]