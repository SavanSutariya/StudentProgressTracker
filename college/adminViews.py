from django.shortcuts import redirect,render
from .models import *
def Home(request):
    return render(request,"college/college_dashboard.html")
def Course_list(request):
    courses = Course.objects.filter(college=request.user.college)
    return render(request,"college/courses_list.html",{'courses':courses})

def subjects_list(request,pk):
    subjects_list = []
    semesters_list = Semester.objects.filter(course=pk)
    for semester in semesters_list:
        subjects = Subject.objects.filter(semester=semester)
        if subjects.exists():
            for subject in subjects:
                subjects_list.append(subject)
    context={
        'subjects_list':subjects_list,
    }
    return render(request, "college/subjects_list.html",context)