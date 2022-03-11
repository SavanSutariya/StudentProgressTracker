from django.urls import path
from . import facultyViews
urlpatterns = [
    path('', facultyViews.Home, name="faculty-home"),
    # path('profile/',facultyViews.user_profile, name="faculty-profile"),
    path('papers/',facultyViews.papers_list,name="faculty-papers-list"),
    path('papers/<int:pk>/',facultyViews.paper_marks,name="faculty-paper-marks"),

    path('profile/',facultyViews.user_profile, name="college-faculty-profile"),

]