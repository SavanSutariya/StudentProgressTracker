from django.urls import path
from . import adminViews

urlpatterns = [
    # college-admin urls
<<<<<<< HEAD
    path('' ,Home, name="college-home"),
    path('course/<int:pk>/',subjects_list, name="subjects-list"),
    path('courses/',Course_list, name="college-course-list"),
    path('course/addsubject/<int:pk>',add_subject,name="add-subject"),
    path('course/addcourse/',add_course,name="add-course"),
    path('course/addstudent/',add_student,name="add-student")

]
=======
    path('' ,adminViews.Home, name="college-home"),
    path('courses/',adminViews.Course_list, name="college-course-list"),
    path('course/<int:pk>/',adminViews.subjects_list, name="subjects-list"),
    path('course/addsubject/<int:pk>',adminViews.add_subject,name="add-subject"),
    path('students/',adminViews.students_list,name="college-students-list"),
    path('faculties/',adminViews.faculties_list,name="college-faculties-list"),
]
>>>>>>> e39f67bfa0b90d70e36d62fd6b0ebf049848ec02
