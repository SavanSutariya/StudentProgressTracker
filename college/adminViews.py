from django.shortcuts import redirect,render
from .models import *
def Home(request):
    return render(request,"college/college_dashboard.html")
def Course_list(request):
    courses = Cource.objects.filter(college=request.user.college)
    return render(request,"college/courses_list.html",{'courses':courses})
def Course_details(request,pk):
    
    subjects_list = Subject.objects.filter(semester=pk)
    print(subjects_list)
    return render(request, "college/course_details.html")