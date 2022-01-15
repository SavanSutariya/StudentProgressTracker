from django.urls import path
from . import adminViews

urlpatterns = [
    # college-admin urls
    path('' ,adminViews.Home, name="college-home"),
    path('courses/',adminViews.Course_list, name="college-course-list"),
    path('course/<int:pk>/',adminViews.subjects_list, name="subjects-list"),
    path('course/addcourse/',adminViews.add_course,name="college-add-course"),
    path('course/addsubject/<int:pk>',adminViews.add_subject,name="college-add-subject"),
    path('students/',adminViews.students_list,name="college-students-list"),
    path('students/addstudent/',adminViews.add_student,name="college-add-student"),
    path('faculties/',adminViews.faculties_list,name="college-faculties-list"),
    path('faculties/addfaculty/',adminViews.add_faculty,name="college-add-faculty"),
]
