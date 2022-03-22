from django.shortcuts import HttpResponse, redirect, render,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import Http404,JsonResponse
import os
import csv
import re

def exportCsv(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Email'])

    for user in CustomUser.objects.all().values_list('first_name', 'last_name', 'email'):
        writer.writerow(user)


    response['Content-Disposition'] = 'attachment; filename="members.csv"'
    return response
    
# Ajax views
def get_semesters_ajax(request,pk):
    '''returns all semesters in json format'''
    
    semesters = Semester.objects.filter(course=pk)
    data = []
    for semester in semesters:
        data.append({"id":semester.id,"number"  :semester.number})
    return JsonResponse({"data":data})

def is_college_admin(user):
    '''checks if authenticated and is a college admin'''
    if user.is_authenticated:
        return user.userType == '1'
    else:
        return False

@user_passes_test(is_college_admin, login_url='/')
def Home(request):
    courses_list = Course.objects.filter(college=request.user.college)
    students_list = Student.objects.filter(user__college=request.user.college)
    faculties_list = Faculty.objects.filter(user__college=request.user.college)
    exams = Exam.objects.filter(semester__course__college=request.user.college)

    context = {
        'courses_list':courses_list,
        'students_list':students_list,
        'faculties_list':faculties_list,
        'exams_list':exams
    }
    return render(request, "college/college_dashboard.html",context)

@user_passes_test(is_college_admin, login_url='/')
def Course_list(request):
    courses = Course.objects.filter(college=request.user.college)
    return render(request, "college/courses_list.html", {'courses': courses})

@user_passes_test(is_college_admin, login_url='/')
def subjects_list(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if(request.user.college != course.college):  # check college admin related college
        raise PermissionDenied
    subjects_list = []
    semesters_list = Semester.objects.filter(course=pk)

    for semester in semesters_list:
        subjects = Subject.objects.filter(semester=semester)
        if subjects.exists():
            for subject in subjects:
                subjects_list.append(subject)
    context = {
        'subjects_list': subjects_list,
        'course': course
    }
    return render(request, "college/subjects_list.html", context)

@user_passes_test(is_college_admin, login_url='/')
def add_subject(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if(request.user.college != course.college):  # check college admin related college
        raise PermissionDenied
    faculties = Faculty.objects.filter(user__college=request.user.college)
    semesters_list = Semester.objects.filter(course=pk)
    subject_type = SubjectType.objects.all()

    if request.method == "POST":
        subject_code = request.POST.get('subject_code')
        if subject_code == '':
            messages.error(request , "Subejct Code must not be Empty")
            return redirect('college-add-subject',pk)
        elif re.findall('^[a-zA-Z][- 0-9]*',subject_code) == []:   
                messages.error(request , "Subject must not start with numeric value and special charachters")
                return redirect('college-add-subject',pk)
        subject_name = request.POST.get('subject_name')
        if subject_name == '':
            messages.error(request , "Name must not be Empty")
            return redirect('college-add-subject',pk)
        elif re.findall('^[a-zA-Z ]+$',subject_name) == []:   
                messages.error(request , "Name must not contain numeric Value")
                return redirect('college-add-subject',pk)
        sub_type = SubjectType.objects.get(id=request.POST.get('subject_types'))
        semester = Semester.objects.get(id=request.POST.get('semester'))
        faculty = Faculty.objects.get(id=request.POST.get('faculty'))
        subject = Subject(
            code=subject_code,
            name=subject_name,
            sub_type=sub_type,
            semester=semester,
            faculty=faculty,
        )
        subject.save()
        messages.success(request, "Subject added successfully")
        return redirect('subjects-list', pk)

    context = {
        'subject_type': subject_type,
        'semesters_list': semesters_list,
        'faculties': faculties,
    }

    return render(request, "college/add_subject.html", context)

@user_passes_test(is_college_admin, login_url='/')
def add_course(request):
    if request.method == 'POST':
        
        course_name = request.POST.get('course_name')
        if re.findall('^[a-zA-Z ]*$',course_name) == []:
            messages.error(request , "Course name must not contain numeric or other type of  value")
            return redirect('college-add-course')
        elif course_name == '':
            messages.error(request , "Course name must not be Empty")
            return redirect('college-add-course')
        college = request.user.college
        semester = request.POST.get('NoOfSem')
        if semester == '':
            messages.error(request , "Semester name must not be Empty")
            return redirect('college-add-course')     
        elif re.findall('^[0-9]*$',semester) == []:
            messages.error(request , "Smester name must not contain alphabetaic Value or other type of  value")       

        if int(semester) > 10 or int(semester) <= 0:
            messages.error(
                request, f"cannot enter insert {semester}. semester must be >0 and <=10")
            return redirect('college-add-course')
        course = Course(
            name=course_name,
            college=college
        )
        course.save()
        for i in range(1, int(semester)+1):
            semester = Semester(
                number=i,
                course=course
            )
            semester.save()
        messages.success(request, f"{course_name} has been added to {college}")
        return redirect('college-course-list')
    return render(request, "college/add_course.html")

@user_passes_test(is_college_admin, login_url='/')
def add_student(request):
    session_year_list = SessionYear.objects.all()
    course_list = Course.objects.filter(college=request.user.college)
    print(course_list)
    if request.method == "POST":
        username = request.POST.get('user_name')
        if username == '':
            messages.error(request , "Username is required")
            return redirect('college-add-student')
        elif re.findall('^[\w.@+\-]+?$',username) == []:
            messages.error(request , "Username is not valid")
            return redirect('college-add-student')

        firstname = request.POST.get('first_name')
        if firstname == '':
            messages.error(request , "Firstname is required")
            return redirect('college-add-student')
        elif re.findall('^[a-z A-Z]+?$',firstname) == []:
            messages.error(request , "firstname is not valid")
            return redirect('college-add-student')
        lastname = request.POST.get('last_name')
        if lastname == '':
            messages.error(request , "lastname is required")
            return redirect('college-add-student')
        elif re.findall('^[a-z A-Z]+?$',lastname) == []:
            messages.error(request , "lastname is not valid")
            return redirect('college-add-student')
        email = request.POST.get('email')
        if email == '':
            messages.error(request , "Email is required")
            return redirect('college-add-student')
        elif re.findall('^[a-z 0-9]+[/._]?[a-z 0-9][@][a-z 0-9]+[.]\w{2,3}$',email) == []:
            messages.error(request , "email is not valid")
            return redirect('college-add-student')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        profile_pic = request.FILES.get('profile_pic')
        session_year = SessionYear.objects.get(id=request.POST.get('session_year'))
        semester = Semester.objects.get(id=request.POST.get('semester'))
        if CustomUser.objects.filter(email=email).exists():
            messages.info(request, "email is already taken")
            return redirect('college-add-student')
        elif CustomUser.objects.filter(username=username).exists():
            messages.info(request, "username is already taken")
            return redirect('college-add-student')
        else:
            user = CustomUser(
                first_name=firstname,
                last_name=lastname,
                username=username,
                email=email,
                profile_pic=profile_pic,
                userType=3,
                college=request.user.college
            )
            user.set_password(f"{username}123")
            user.save()
            student = Student(
                user=user,
                address=address,
                gender=gender,
                session_year=session_year,
                semester=semester,
                dob=dob
            )
            student.save()
            messages.success(request, "student added successfully")
            return redirect('college-students-list')
    context = {
        'session_year_list': session_year_list,
        'courses_list': course_list
    }
    return render(request, "college/add_student.html", context)

@user_passes_test(is_college_admin, login_url='/')
def students_list(request):
    students_list = Student.objects.filter(user__college=request.user.college)
    context = {
        'students_list': students_list
    }
    return render(request, 'college/college_students_list.html', context)

@user_passes_test(is_college_admin, login_url='/')
def faculties_list(request):

    faculties_list = Faculty.objects.filter(user__college=request.user.college)
    context = {
        'faculties_list': faculties_list
    }
    return render(request, 'college/college_faculties_list.html', context)

@user_passes_test(is_college_admin, login_url='/')
def add_faculty(request):
    if request.method == "POST":
        username = request.POST.get('user_name')
        if username == '':
            messages.error(request , "Username is required")
            return redirect('college-add-faculty')
        elif re.findall('^[\w.@+\-]+?$',username) == []:
            messages.error(request , "Username is not valid")
            return redirect('college-add-faculty')
        firstname = request.POST.get('first_name')
        if firstname == '':
            messages.error(request , "Firstname is required")
            return redirect('college-add-faculty')
        elif re.findall('^[a-z A-Z]+?$',firstname) == []:
            messages.error(request , "firstname is not valid")
            return redirect('college-add-faculty')
        lastname = request.POST.get('last_name')
        if lastname == '':
            messages.error(request , "lastname is required")
            return redirect('college-add-faculty')
        elif re.findall('^[a-z A-Z]+?$',lastname) == []:
            messages.error(request , "lastname is not valid")
            return redirect('college-add-faculty')
        email = request.POST.get('email')
        if email == '':
            messages.error(request , "Email is required")
            return redirect('college-add-faculty')
        elif re.findall('^[a-z 0-9]+[/._]?[a-z 0-9][@][a-z 0-9]+[.]\w{2,3}$',email) == []:
            messages.error(request , "email is not valid")
            return redirect('college-add-faculty')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        profile_pic = request.FILES.get('profile_pic')
        if CustomUser.objects.filter(email=email).exists():
            messages.info(request, "email is already taken")
            return redirect('college-add-faculty')
        if CustomUser.objects.filter(username=username).exists():
            messages.info(request, "username is already taken")
            return redirect('college-add-faculty')
        else:
            user = CustomUser(
                first_name=firstname,
                last_name=lastname,
                username=username,
                email=email,
                profile_pic=profile_pic,
                userType=2,
                college=request.user.college
            )
            user.set_password(f"{username}123")
            user.save()
            faculty = Faculty(
                user=user,
                address=address,
                gender=gender,
            )
            faculty.save()
            messages.success(request, "faculty added successfully")
            return redirect('college-faculties-list')

    return render(request, 'college/add_faculty.html')

@user_passes_test(is_college_admin, login_url='/')
def user_profile(request):
    # check if fields are not empty
    if(request.method == "POST"):
        profile = request.FILES.get("profile_pic")
        ext = os.path.splitext(profile.name)[1]
        if profile == None:
            profile = request.user.profile_pic
        elif ext not in ['.jpg', '.png', '.jpeg']:
            profile = request.user.profile_pic
        else:
            try:
                os.remove(request.user.profile_pic.path)
            except:
                pass
        username = request.POST.get("username")
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        user = CustomUser.objects.get(id=request.user.id)
        user.username=username  
        user.first_name =fname
        user.last_name = lname
        user.profile_pic=profile
        user.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect('college-admin-profile')
    return render(request, 'college/user_profile.html')

@user_passes_test(is_college_admin, login_url='/')
def update_course(request,pk):
    course = get_object_or_404(Course, pk=pk)
    if(request.user.college != course.college):  # check college admin related college
        raise PermissionDenied
    else:
        semesters_list = Semester.objects.filter(course=course)
        context = {
            'course': course,
            'semesters_list': semesters_list 
            }
        if request.method == 'POST':
            course_name = request.POST.get('course_name') 
            if course_name == '':
                messages.error(request , "Course name must not be Empty")
                return redirect('college-update-course',pk)
            elif re.findall('^[-a-zA-Z ]+$',course_name) == []:   
                messages.error(request , "Course name must not contain numeric or other type of  value")
                return redirect('college-update-course',pk)
            course.name = request.POST.get('course_name')           
            course.save()
            messages.success(request, f"{course.name} is saved!")
            return redirect('college-course-list')
    return render(request, "college/update_course.html",context)

@user_passes_test(is_college_admin, login_url='/')
def update_subject(request,pk):
    subject = get_object_or_404(Subject,pk=pk)
    subject_types = SubjectType.objects.all()
    semesters = Semester.objects.filter(course=subject.semester.course)
    faculties = Faculty.objects.filter(user__college=request.user.college)
    if (subject.semester.course.college != request.user.college):
        raise PermissionDenied
    if request.method == "POST":
        code = request.POST.get('subject_code')
        if code == '':
            messages.error(request , "Subejct Code must not be Empty")
            return redirect('college-update-subject',pk)
        elif re.findall('^[a-zA-Z][- 0-9]*',code) == []:   
                messages.error(request , "Subject must not start with numeric value")
                return redirect('college-update-subject',pk)
        name = request.POST.get('subject_name')
        if code == '':
            messages.error(request , "Name must not be Empty")
            return redirect('college-update-subject',pk)
        elif re.findall('^[-a-zA-Z ]+$',name) == []:   
                messages.error(request , "Name must not contain numeric Value")
                return redirect('college-update-subject',pk)
        subtype = request.POST.get('subject_type')
        semester = request.POST.get('semester')
        facultie = request.POST.get('faculty')
        
        subject.code = code
        subject.name = name
        subject.sub_type = SubjectType.objects.get(pk=subtype)
        subject.semester = Semester.objects.get(pk=semester)
        subject.faculty = Faculty.objects.get(pk=facultie)
        subject.save()
        messages.success(request,f"{subject.name} has been updated!")
        return redirect('subjects-list')

    context = {
        'subject':subject,
        'subject_types':subject_types,
        'semesters_list':semesters,
        'faculties' : faculties,
    }
    return render(request,'college/update_subject.html',context)

@user_passes_test(is_college_admin, login_url='/')
def update_faculty(request,pk):
    faculty = get_object_or_404(Faculty,pk=pk)
    if (faculty.user.college != request.user.college):
        raise PermissionDenied
    if request.method == "POST":

        profile = request.FILES.get("profile_pic")
        if profile == None:
            profile = faculty.user.profile_pic
        else:
            try:
                os.remove(faculty.user.profile_pic.path)
            except:
                pass
        faculty.user.username = request.POST.get('username')
        if faculty.user.username == '':
           messages.error(request , "Username is required")
           return redirect('college-update-faculty',pk)
        elif re.findall('^[\w.@+\-]+?$',faculty.user.username) == []:
           messages.error(request , "Username is not valid")
           return redirect('college-update-faculty',pk)
        
        faculty.user.first_name = request.POST.get('first_name')
        if faculty.user.first_name == '':
            messages.error(request , "Firstname is required")
            return redirect('college-update-faculty',pk)
        elif re.findall('^[a-z A-Z]+?$',faculty.user.first_name) == []:
            messages.error(request , "firstname is not valid")
            return redirect('college-update-faculty',pk)
        
        faculty.user.last_name = request.POST.get('last_name')
        if faculty.user.last_name == '':
            messages.error(request , "lastname is required")
            return redirect('college-update-faculty',pk)
        elif re.findall('^[a-z A-Z]+?$',faculty.user.last_name) == []:
            messages.error(request , "lastname is not valid")
            return redirect('college-update-faculty',pk)
        #faculty.user.email = request.POST.get('user')
        #if faculty.user.email == '':
        #    messages.error(request , "Email is required")
        #    return redirect('college-update-faculty')
        #elif re.findall('^[a-z 0-9]+[/._]?[a-z 0-9][@][a-z 0-9]+[.]\w{2,3}$',faculty.user.email) == []:
        #    messages.error(request , "email is not valid")
        #    return redirect('college-update-faculty') 
        faculty.gender = request.POST.get('gender')
        faculty.address = request.POST.get('address')
        faculty.user.profile_pic = profile
        faculty.save()
        faculty.user.save()
        messages.success(request,'Faculty Profile Updated Successfully!')
        return redirect('college-faculties-list')
    context = {
        'faculty':faculty,
    }
    return render(request,'college/update_faculty.html',context)

@user_passes_test(is_college_admin, login_url='/')
def update_student(request,pk):
    student = get_object_or_404(Student,pk=pk)
    course_list = Course.objects.filter(college=request.user.college)
    print(course_list)
    session_years = SessionYear.objects.all()
    #semester = Semester.objects.get(id=request.POST.get('semester'))
    if (student.user.college != request.user.college):
        raise PermissionDenied
    if request.method == "POST":
        profile = request.FILES.get("profile_pic")
        if profile == None:
            profile = student.user.profile_pic
        else:
            try:
                os.remove(student.user.profile_pic.path)
            except:
                pass
        student.user.username = request.POST.get('username')
        if student.user.username == '':
            messages.error(request , "Username is required")
            return redirect('college-update-student',pk)
        elif re.findall('^[\w.@+\-]+?$',student.user.username) == []:
            messages.error(request , "Username is not valid")
            return redirect('college-update-student',pk)
        
        student.user.first_name = request.POST.get('first_name')
        if student.user.first_name == '':
            messages.error(request , "Firstname is required")
            return redirect('college-update-student',pk)
        elif re.findall('^[a-z A-Z]+?$',student.user.first_name) == []:
            messages.error(request , "firstname is not valid")
            return redirect('college-update-student',pk)
        
        student.user.last_name = request.POST.get('last_name')
        if student.user.last_name == '':
            messages.error(request , "lastname is required")
            return redirect('college-update-student',pk)
        elif re.findall('^[a-z A-Z]+?$',student.user.last_name) == []:
            messages.error(request , "lastname is not valid")
            return redirect('college-update-student',pk)
        
        student.address = request.POST.get('address')
        student.gender = request.POST.get('gender')
        student.user.profile_pic = profile
        student.session_year = SessionYear.objects.get(pk=request.POST.get('session_year'))
        student.dob = request.POST.get('dob')
        student.semester = Semester.objects.get(pk=request.POST.get('semester'))
        
        student.save()
        student.user.save()
        messages.success(request,'Student Profile Updated Successfully!')
        return redirect('college-students-list')
    context = {
        'student':student,
        'session_year_list':session_years,
        'course_list' : course_list,
    }
    return render(request,'college/update_student.html',context)

@user_passes_test(is_college_admin, login_url='/')
def delete_subject(request,pk):
    subject = get_object_or_404(Subject, pk=pk)
    if (subject.semester.course.college != request.user.college):
        raise PermissionDenied
    else:
        if(request.method == "POST"):
            subject.delete()
            messages.success(request, f"{subject.name} has been deleted!")
            return redirect('subjects-list' , subject.semester.course.id)
        context = {
            'obj':subject
        }
        return render(request,'college/delete_confirmation.html',context)

# @user_passes_test(is_college_admin, login_url='/')
# def delete_semester(request,pk):
#     semester = get_object_or_404(Semester, pk=pk)
#     if (semester.course.college != request.user.college):
#         raise PermissionDenied
#     else:
#         if(request.method == "POST"):
#             semester.delete()
#             messages.success(request, f"{semester.name} has been deleted!")
#             return redirect('college-course-list')
#         context = {
#             'obj':semester
#         }
#         return render(request,'college/delete_confirmation.html',context)
            
@user_passes_test(is_college_admin, login_url='/')
def delete_course(request,pk):
    course = get_object_or_404(Course, pk=pk)
    if (course.college != request.user.college):
        raise PermissionDenied
    else:
        if(request.method == "POST"):
            course.delete()
            messages.success(request, f"{course.name} has been deleted!")
            return redirect('college-course-list')
        context = {
            'obj':course
        }
        return render(request,'college/delete_confirmation.html',context)

@user_passes_test(is_college_admin, login_url='/')
def delete_faculty(request,pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if (faculty.user.college != request.user.college):
        raise PermissionDenied
    else:
        if(request.method == "POST"):
            faculty.user.delete()
            faculty.delete()
            os.remove(faculty.user.profile_pic.path)
            messages.success(request, f"{faculty.user.first_name} has been deleted!")
            return redirect('college-faculties-list')
        context = {
            'obj':faculty
        }
        return render(request,'college/delete_confirmation.html',context)

@user_passes_test(is_college_admin, login_url='/')
def delete_student(request,pk):
    student = get_object_or_404(Student, pk=pk)
    if (student.user.college != request.user.college):
        raise PermissionDenied
    else:
        if(request.method == "POST"):
            student.user.delete()
            student.delete()
            messages.success(request, f"{student.user.first_name} has been deleted!")
            return redirect('college-students-list')
        context = {
            'obj':student
        }
        return render(request,'college/delete_confirmation.html',context)

@user_passes_test(is_college_admin, login_url='/')
def exams_list(request):
    exams = Exam.objects.filter(semester__course__college=request.user.college)
    context = {
        'exams':exams
    }
    return render(request,'college/exam_list.html',context)

@user_passes_test(is_college_admin, login_url='/')
def add_exam(request):
    if request.method == "POST":
        name = request.POST.get('exam_name')
        if name == '':
            messages.error(request , "name is required")
            return redirect('college-add-exam')
        date = request.POST.get('exam_date')
        session_year = request.POST.get('session_year')
        semester = request.POST.get('semester')
        try:
            exam = Exam(name=name,date=date,session_year=SessionYear.objects.get(pk=session_year),semester=Semester.objects.get(pk=semester))
            exam.save()
            messages.success(request, f"{exam.name} has been added!")
        except:
            messages.error(request, f"Something went wrong!")
        return redirect('college-exams-list')
    session_year = SessionYear.objects.all()
    semesters = Semester.objects.filter(course__college=request.user.college)
    context = {
        'session_year_list':session_year,
        'semesters':semesters
    }
    return render(request,'college/add_exam.html',context)

@user_passes_test(is_college_admin, login_url='/')
def update_exam(request,pk):
    exam = get_object_or_404(Exam, pk=pk)
    if (exam.semester.course.college != request.user.college):
        raise PermissionDenied
    else:
        if request.method == "POST":
            exam.name = request.POST.get('exam_name')
            if exam.name == '':
               messages.error(request , "name is required")
               return redirect('college-update-exam')
            exam.date = request.POST.get('exam_date')
            exam.save()
            messages.success(request, f"{exam.name} has been updated!")
            return redirect('college-exams-list')
        context = {
            'exam':exam,            
        }
        return render(request,'college/update_exam.html',context)

@user_passes_test(is_college_admin, login_url='/')
def delete_exam(request,pk):
    exam = get_object_or_404(Exam, pk=pk)
    if (exam.semester.course.college != request.user.college):
        raise PermissionDenied
    else:
        if(request.method == "POST"):
            exam.delete()
            messages.success(request, f"{exam.name} has been deleted!")
            return redirect('college-exams-list')
        context = {
            'obj':exam
        }
        return render(request,'college/delete_confirmation.html',context)

@user_passes_test(is_college_admin, login_url='/')
def papers_list(request,pk):
    exam = get_object_or_404(Exam, pk=pk)
    papers = Paper.objects.filter(exam=exam)
    context = {
        'papers':papers,
        'exam':exam
    }
    return render(request,'college/papers_list.html',context)

@user_passes_test(is_college_admin, login_url='/')
def add_paper(request,pk):
    exam = get_object_or_404(Exam, pk=pk)
    subjects = Subject.objects.filter(semester__course=exam.semester.course)
    if (exam.semester.course.college != request.user.college):
        raise PermissionDenied
    else:
        if request.method == "POST":
            paper_name = request.POST.get('paper_name')
            try:
                paper = Paper(name=paper_name,exam=exam,subject=Subject.objects.get(pk=request.POST.get('subject')),total_marks=request.POST.get('paper_marks'))
                paper.save()
                messages.success(request, f"{paper.name} has been added!")
            except:
                messages.error(request, f"Something went wrong!")
            return redirect('college-papers-list',pk=pk)
        context = {
            'exam':exam,
            'subjects':subjects
        }
        return render(request,'college/add_paper.html',context)

@user_passes_test(is_college_admin, login_url='/')
def delete_paper(request,pk):
    paper = get_object_or_404(Paper, pk=pk)
    if (paper.exam.semester.course.college != request.user.college):
        raise PermissionDenied
    else:
        if(request.method == "POST"):
            paper.delete()
            messages.success(request, f"{paper.name} has been deleted!")
            return redirect('college-papers-list',pk=paper.exam.pk)
        context = {
            'obj':paper
        }
        return render(request,'college/delete_confirmation.html',context)