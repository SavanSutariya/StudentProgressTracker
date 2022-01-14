from io import SEEK_END
from django.http import request
from django.shortcuts import HttpResponse,redirect,render
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import *
from django.core.exceptions import PermissionDenied
def is_college_admin(user):
    return user.userType == '1'

@user_passes_test(is_college_admin, login_url='/')
def Home(request):
    return render(request,"college/college_dashboard.html")
@user_passes_test(is_college_admin, login_url='/')
def Course_list(request):
    courses = Course.objects.filter(college=request.user.college)
    return render(request,"college/courses_list.html",{'courses':courses})
@user_passes_test(is_college_admin, login_url='/')
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
@user_passes_test(is_college_admin, login_url='/')
def add_subject(request,pk):
    semesters_list = Semester.objects.filter(course=pk)
    subject_type = SubjectType.objects.all()

    if request.method == "POST":
        subject_code =  request.POST.get('subject_code')
        subject_name =  request.POST.get('subject_name')
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
 
    context = {
        'subject_type' : subject_type,
        'semesters_list' : semesters_list
    }
    
    return render(request, "college/add_subject.html",context)
@user_passes_test(is_college_admin, login_url='/')
def add_course(request):
    if request.method == 'POST':
        course_name =  request.POST.get('course_name')
        college = request.user.college
        semester = request.POST.get('NoOfSem')
        print(course_name,semester)

        course = Course(
                name = course_name,
                college = college
            )
        course.save()
        for i in range(1,int(semester)+1):
            semester = Semester(
                number = i,
                course = course
            )   
            semester.save()
        return redirect('college-course-list')
    return render(request, "college/add_course.html")
@user_passes_test(is_college_admin, login_url='/')
def add_student(request):
    session_year_list = SessionYear.objects.all()
    if request.method  == "POST":
        username = request.POST.get('user_name')
        firstname=request.POST.get('first_name')
        lastname=request.POST.get('last_name')
        email=request.POST.get('email')
        address =request.POST.get('address')
        gender=request.POST.get('gender')
        profile_pic = request.FILES.get('profile_pic')
        session_year = SessionYear.objects.get(id=request.POST.get('session_year'))
        if CustomUser.objects.filter(email=email).exists():
            print('email is already taken')
            return redirect('college-add-student')
        if CustomUser.objects.filter(username=username).exists():
            print('username is already taken')
        else:   
            user = CustomUser(
                first_name = firstname,
                last_name = lastname,
                username =username,
                email = email,
                profile_pic = profile_pic,
                userType = 3,
                college = request.user.college
            )
            user.set_password(f"{username}123")
            user.save()
            student = Student(
                user = user,
                address = address,
                gender = gender,
                session_year = session_year,
            )
            student.save()
            print('student add successfully') 
            return redirect('college-students-list')

    context = {
        'session_year_list' : session_year_list,
    }
    return render(request,"college/add_student.html",context)
@user_passes_test(is_college_admin, login_url='/')
def students_list(request):
    students_list = Student.objects.filter(user__college=request.user.college)
    context={
        'students_list':students_list
    }
    return render(request,'college/college_students_list.html',context)
@user_passes_test(is_college_admin, login_url='/')
def faculties_list(request):
    faculties_list = Faculty.objects.filter(user__college=request.user.college)
    context = {
        'faculties_list':faculties_list
    }
    return render(request,'college/college_faculties_list.html',context)