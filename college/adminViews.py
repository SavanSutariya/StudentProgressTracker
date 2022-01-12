from django.http import request
from django.shortcuts import HttpResponse,redirect,render
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.exceptions import PermissionDenied
def Home(request):
    return render(request,"college/college_dashboard.html")
@login_required(login_url='/')
def Course_list(request):
    courses = Course.objects.filter(college=request.user.college)
    return render(request,"college/courses_list.html",{'courses':courses})
@login_required(login_url='/')
def subjects_list(request,pk):
    if(request.user.college != Course.objects.get(pk=pk).college): #check college admin related college
        raise PermissionDenied       
    subjects_list = []
    semesters_list = Semester.objects.filter(course=pk)

    for semester in semesters_list:
        subjects = Subject.objects.filter(semester=semester)
        if subjects.exists():
            for subject in subjects:
                subjects_list.append(subject)
    context={
        'subjects_list':subjects_list,
        'course_id':pk
    }
    return render(request, "college/subjects_list.html",context)
@login_required(login_url='/')
def add_subject(request,pk):
    semesters_list = Semester.objects.filter(course=pk)
    subject_type = SubjectType.objects.all()

    if request.method == "POST":
        subject_code =  request.POST.get('subject_code')
        subject_name =  request.POST.get('subject_name')
        #subject_types =  request.POST.get('subject_types')
        #semesters =  request.POST.get('semester')
        sub_type =  SubjectType.objects.get(id = request.POST.get('subject_types'))
        semester =  Semester.objects.get(id = request.POST.get('semester'))
        

        if Subject.objects.filter(code=subject_code).exists():
            print('Alredy added')
            return redirect('add-subject',pk)
        else:                
            subject = Subject(
                code = subject_code,
                name = subject_name,
                sub_type = sub_type,
                semester = semester
            )
            subject.save()
            print('Added successfully')
            return redirect('subjects-list',pk)
        
        #print(subject_code,subject_name,subject_types,semesters)
 
    context = {
        'subject_type' : subject_type,
        'semesters_list' : semesters_list
    }
    
    return render(request, "college/add_subject.html",context)
@login_required(login_url='/')
def students_list(request):
    students_list = Student.objects.filter(user__college=request.user.college)
    context={
        'students_list':students_list
    }
    return render(request,'college/college_students_list.html',context)
@login_required(login_url='/')
def faculties_list(request):
    faculties_list = Faculty.objects.filter(user__college=request.user.college)
    context = {
        'faculties_list':faculties_list
    }
    return render(request,'college/college_faculties_list.html',context)