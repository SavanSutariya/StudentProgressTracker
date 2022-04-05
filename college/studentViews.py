from audioop import avg
from multiprocessing import context
from django.shortcuts import HttpResponse, redirect, render,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
import os
from college.adminViews import exams_list, students_list
from .models import *
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.db.models import Avg

def Average(results):
    '''find average from marks from results'''
    obtained = 0
    total = 0
    for result in results:
        total += result.paper.total_marks
        obtained += result.marks

    try:
        return (100*obtained)/total
    except (ZeroDivisionError):
        return 0
def is_student(user):
    '''checks if authenticated and is a student'''
    if user.is_authenticated:
        return user.userType == '3'
    else:
        return False

@user_passes_test(is_student,login_url='/')
def Home(request):
    '''Home Page for student'''
    types = SubjectType.objects.all()
    overall = Result.objects.filter(student=request.user.student)
    types = SubjectType.objects.all()
    avg_lst = []
    for type in types:
        result = Result.objects.filter(student=request.user.student,paper__subject__sub_type=type)
        avg_lst.append({'type':type.name,'avg':round(Average(result), 2)})
    print(avg_lst)
    overall_average = round(Average(overall), 2)
    context = {
        'types':types,
        'overall':overall_average,
        'avg_lst':avg_lst
    }
    return render(request, 'student/student_home.html',context)
    
@user_passes_test(is_student,login_url='/')
def user_profile(request):
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
        return redirect('college-student-profile')
    return render(request, 'student/user_profile.html')

@user_passes_test(is_student,login_url='/') 
def check_result(request): 
    # student = get_object_or_404(Student,user=request.user)
    # exams_list = Exam.objects.filter(semester__course__college=request.user.college)
    # paper_list = Paper.objects.filter(exam__semester__course__college=request.user.college)
    # marks_list = Result.objects.filter(paper__exam__semester__course__college=request.user.college)
    # context = {
    #     'exams_list' : exams_list,
    #     'paper_list' : paper_list,
    #     'marks_list' : marks_list,
    # }
    student = get_object_or_404(Student,user=request.user)
    exams_list = Exam.objects.filter(semester=student.semester)
    context = {
        'exams_list': exams_list,
    }
    return render(request, 'student/check_result.html',context)
@user_passes_test(is_student,login_url='/') 
def get_papers_ajax(request,pk):
    papers = Paper.objects.filter(exam=pk)
    student = get_object_or_404(Student,user=request.user)
    data = []
    for paper in papers:
        marks = Result.objects.get(paper=paper,student=student)
        data.append({"id":paper.id,"paper":paper.name,"subject":marks.paper.subject.name,"marks":marks.marks,"total":marks.paper.total_marks})
    return JsonResponse({"data":data})
@user_passes_test(is_student,login_url='/') 
def get_marks_ajax(request,pk):
    student = get_object_or_404(Student,user=request.user)
    marks_list = Result.objects.filter(paper=pk,student=student)
  
    data = [] 
    for marks in marks_list:
        data.append({"paper":marks.paper.name,"subject":marks.paper.subject.name,"marks":marks.marks,"total":marks.paper.total_marks})
    return JsonResponse({"data" : data})
@user_passes_test(is_student,login_url='/') 
def suggestion(request):
    if request.method == "POST":
        student = get_object_or_404(Student,user=request.user)
        attachment = request.FILES.get("attachment")
        if attachment != None:
            ext = os.path.splitext(attachment.name)[1]
            if ext.lower() not in ['.jpg', '.png', '.jpeg', '.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls', '.txt']:
                messages.error(request, "Please Upload a valid file")
                return redirect('college-student-suggestion-box')
        message = request.POST.get("message")
        if message == "":
            messages.error(request, "Please Enter a message")
            return redirect('college-student-suggestion-box')
        try:
            suggestion = Suggestion(student=student,attachment=attachment,message=message)
            suggestion.save()
            messages.success(request, "Suggestion Submitted Successfully")
            return redirect('college-student-suggestion-box')
        except:
            messages.error(request, "Error Occured")
            return redirect('college-student-suggestion-box')
    return render(request, 'student/suggestion.html')
@user_passes_test(is_student,login_url='/')
def student_result_line_chart(request):
    student = get_object_or_404(Student,user=request.user)
    papers_list = Paper.objects.filter(subject__semester=student.semester).order_by('id')
    results = []
    result2 = []
    for paper in papers_list:
        marks = Result.objects.filter(paper=paper,student=student)
        if marks.count() > 0:
            results.append({"exam":paper.name,"marks":round(Average(marks), 2)})
    # list average score of student after every paper
    avg_paper_list = []
    for paper in papers_list:
        marks = Result.objects.filter(paper=paper,student=student)
        if marks.count() > 0:
            avg_paper_list.append(paper)
            avgs = []
            for avg_paper in avg_paper_list:
                marks = Result.objects.filter(paper=avg_paper,student=student)
                if len(marks) != 0:
                    last_updated=marks[0].last_updated
                    avgs.append(Average(marks))
            date_str = paper.date.strftime("%d %b %y")
            result2.append({"date":date_str,"marks": round(sum(avgs) / len(avgs), 2)})
    context = {
        'results':results,
        'averages':result2,
        'score': round(sum(avgs) / len(avgs),2),
        'last_updated':last_updated.strftime("%d %b %y %I:%M %p"),
    }
    return render(request, 'student/student_result_line_chart.html',context)
