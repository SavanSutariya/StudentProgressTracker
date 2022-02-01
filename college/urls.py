from django.urls import path
from . import adminViews

urlpatterns = [
    # college-admin urls
    path('' ,adminViews.Home, name="college-home"),
    path('profile/',adminViews.user_profile, name="college-admin-profile"),

    path('courses/',adminViews.Course_list, name="college-course-list"),
    path('course/add/',adminViews.add_course,name="college-add-course"),
    path('course/update/<int:pk>',adminViews.update_course,name="college-update-course"),
    path('course/delete/<int:pk>',adminViews.delete_course,name="college-delete-course"),

    path('course/<int:pk>',adminViews.subjects_list, name="subjects-list"),
    path('course/addsubject/<int:pk>',adminViews.add_subject,name="college-add-subject"),
    path('course/updatesubject/<int:pk>',adminViews.update_subject,name="college-update-subject"),
    path('course/deletesubject/<int:pk>',adminViews.delete_subject,name="college-delete-subject"),

    path('students/',adminViews.students_list,name="college-students-list"),
    path('students/add/',adminViews.add_student,name="college-add-student"),
    path('students/update/<int:pk>',adminViews.update_student,name="college-update-student"),
    path('students/delete/<int:pk>',adminViews.delete_student,name="college-delete-student"),

    path('faculties/',adminViews.faculties_list,name="college-faculties-list"),
    path('faculties/add/',adminViews.add_faculty,name="college-add-faculty"),
    path('faculties/update/<int:pk>',adminViews.update_faculty,name="college-update-faculty"),
    path('faculties/delete/<int:pk>',adminViews.delete_faculty,name="college-delete-faculty"),

    path('exams/',adminViews.exams_list,name="college-exams-list"),
    path('exams/add/',adminViews.add_exam,name="college-add-exam"),
    path('exams/update/<int:pk>',adminViews.update_exam,name="college-update-exam"),
    # path('exams/delete/<int:pk>',adminViews.delete_exam,name="college-delete-exam"),

    path('exams/<int:pk>',adminViews.papers_list,name="college-papers-list"),
    path('exams/addpaper/<int:pk>',adminViews.add_paper,name="college-add-paper"),
]
