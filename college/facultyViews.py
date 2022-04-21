import re
from django.shortcuts import HttpResponse, redirect, render,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
import os
from django.contrib.auth.decorators import user_passes_test
from college.adminViews import faculties_list
from .models import *
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import Http404
from django.http import JsonResponse


def is_faculty(user):
    '''checks if authenticated and is a Faculty'''
    if user.is_authenticated:
        return user.userType == '2'
    else:
        return False

def get_average_by_types(student,typ):
    '''returns list of papers of a particular type'''
    if(typ == 'overall'):
        results = Result.objects.filter(student=student)
    else:
        results = Result.objects.filter(student=student,paper__subject__sub_type=typ)


@user_passes_test(is_faculty,login_url='/')
def Home(request):
    '''Home Page for Faculty'''
    subjects_list = Subject.objects.filter(faculty__user=request.user)
    # students_list = Student.objects.filter()
    papers_list=Paper.objects.filter(subject__faculty__user=request.user)
    context = {
        'subjects_list':subjects_list,
        'papers_list':papers_list
    }
    return render(request, 'faculty/faculty_home.html',context)

@user_passes_test(is_faculty,login_url='/')
def papers_list(request):
    '''
    This view is for the faculty to see the list of papers
    '''
    faculty = get_object_or_404(Faculty,user=request.user)
    papers = Paper.objects.filter(subject__faculty=faculty)
    return render(request, 'faculty/papers_list.html', {'papers':papers})

@user_passes_test(is_faculty,login_url='/')
def paper_marks(request,pk):
    '''
    This view is for the faculty to add the marks of a paper
    '''
    paper = get_object_or_404(Paper,pk=pk)
    students_list = Student.objects.filter(semester=paper.subject.semester)
    # if paper.subject.faculty != request.user.faculty:
    #     raise PermissionDenied
    # if request.method == 'POST':
    #     for student in paper.students.all():
    #         marks = request.POST.get(str(student.id))
    #         if marks:
    #             try:
    #                 marks = int(marks)
    #             except:
    #                 messages.error(request,'Invalid Marks')
    #                 return redirect('faculty-paper-marks',pk=pk)
    #             if marks < 0 or marks > 100:
    #                 messages.error(request,'Invalid Marks')
    #                 return redirect('faculty-paper-marks',pk=pk)
    #             try:
    #                 marksheet = Marksheet.objects.get(student=student,paper=paper)
    #                 marksheet.marks = marks
    #                 marksheet.save()
    #             except Marksheet.DoesNotExist:
    #                 marksheet = Marksheet(student=student,paper=paper,marks=marks)
    #                 marksheet.save()
    #     messages.success(request,'Marks Added')
    #     return redirect('faculty-paper-marks',pk=pk)
    context = {
        'paper':paper,
        'students_list': students_list
    }
    return render(request, 'faculty/paper_marks.html',context)


@user_passes_test(is_faculty, login_url='/')
def user_profile(request):
    # check if fields are not empty
    if(request.method == "POST"):
        profile = request.FILES.get("profile_pic")
        if profile == None:
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
        return redirect('college-faculty-profile')
    return render(request, 'faculty/user_profile.html')

@user_passes_test(is_faculty, login_url='/')
def save_marks(request):
    if request.method == 'POST':
        student = Student.objects.get(id=request.POST.get('student'))
        paper = Paper.objects.get(id=request.POST.get('paper'))
        marks = request.POST.get('marks')
        if marks:
            try:
                marks = int(marks)
                if(marks == None):
                    marks = 0
                elif(marks < 0 or marks > 100):
                    messages.error(request,'Invalid Marks')
                else:
                    print("Heloooo")
                    Result.objects.update_or_create(student=student,paper=paper,defaults={'marks':marks})
                    messages.success(request,'Marks saved')
            except:
                messages.error(request,'something went wrong')
        else:
            messages.warning(request,'Field must not be Empty')
        return redirect('faculty-paper-marks',paper.id)

@user_passes_test(is_faculty, login_url='/')
def leaderboard(request):
    courses_list = Course.objects.filter(college=request.user.college)
    types = SubjectType.objects.all()
    context = {
        'courses_list':courses_list,
        'sub_types':types
    }
    return render(request,'faculty/leaderboard.html',context)

def leaderboard_ajax(request,pk):
    semester = get_object_or_404(Semester, pk=pk)
    students = Student.objects.filter(semester=semester)
    # students = Student.objects.all()
    data = []
    for student in students:
        # check if type in get:
        if(request.GET.get('type') != None):
            try:
                # if type is specified
                score = round(get_average_by_types(student,int(request.GET.get('type'))),2)
            except (ValueError):
                # executes when type is non integer e.g. 'overall' or user is doing something suspecious
                score = round(get_average_by_types(student,'overall'),2)
        else:
            # executes when there is no get parameter named 'type'
            score = round(get_average_by_types(student,'overall'),2)
        data.append({
            'profile':student.user.profile_pic.url,
            'name':student.user.get_full_name(),
            'stud_id':student.id,
            'score':score
        })
        print(data)
        data.sort(key=lambda x: x['score'], reverse=True)
        print(data)
    return JsonResponse({'data':data})