from django.shortcuts import HttpResponse, redirect, render,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
import os
from .models import *
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import Http404

def is_faculty(user):
    '''checks if authenticated and is a Faculty'''
    if user.is_authenticated:
        return user.userType == '2'
    else:
        return False

@user_passes_test(is_faculty,login_url='/')
def Home(request):
    '''Home Page for Faculty'''
    return render(request, 'faculty/faculty_home.html')

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
    results = Result.objects.filter(paper=paper)
    print(results)
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
        marks = int(request.POST.get('marks'))
        try:
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
        return redirect('faculty-paper-marks',paper.id)