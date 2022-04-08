from django.urls import path
from . import studentViews

urlpatterns = [
    path('' ,studentViews.Home, name="student-home"),
    path('profile/',studentViews.user_profile,name="college-student-profile"),
    path('checkResult/',studentViews.check_result,name="college-student-result"),
    path('ajax/get-papers/<int:pk>',view=studentViews.get_papers_ajax, name="ajax-get-no-of-papers"),
    path('ajax/get-marks/<int:pk>',view=studentViews.get_marks_ajax, name="ajax-get-no-of-marks"),
    path('suggestion/',studentViews.suggestion,name="college-student-suggestion-box"),
]


