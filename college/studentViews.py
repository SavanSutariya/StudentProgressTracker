from distutils.archive_util import make_archive
from django.shortcuts import HttpResponse, redirect, render,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
import os
from .models import *
from django.contrib import messages
from django.http import JsonResponse

def Average(results):
    '''find average from marks from results'''
    
    total = 0
    count = 0
    for result in results:
        total += (100*result.marks)/result.paper.total_marks
        count += 1
    try:
        return total/count
    except (ZeroDivisionError):
        return 0
def is_student(user):
    '''checks if authenticated and is a student'''
    if user.is_authenticated:
        return user.userType == '3'
    else:
        return False

def get_average_by_types(student,typ):
    '''returns list of papers of a particular type'''
    if(str(typ).lower() == 'overall'):
        results = Result.objects.filter(student=student)
    else:
        results = Result.objects.filter(student=student,paper__subject__sub_type=typ)

    return Average(results)
score = []
last_updated = "No Result"
def get_score_history(student,papers_list):
    global score
    global last_updated
    results = []
    avg_paper_list = []
    for paper in papers_list:
            marks = Result.objects.filter(paper=paper,student=student)
            avgs = []
            if marks.count() > 0:
                avg_paper_list.append(paper)   
                for avg_paper in avg_paper_list:
                    marks = Result.objects.filter(paper=avg_paper,student=student)
<<<<<<< HEAD
=======
                    
>>>>>>> 5c2ba4900e8ae05701b0c5948389987a2c657d99
                    if len(marks) != 0:
                        last_updated=marks[0].last_updated
                        last_updated = last_updated.strftime("%d %b %y %I:%M %p")
                        avgs.append(Average(marks))
                date_str = paper.date.strftime("%d %b %y")
                results.append({"date":date_str,"marks": round(sum(avgs) / len(avgs), 2)})
            if len(avgs)!=0:
                score = avgs
    return results
def get_bar_results(student,papers_list):
    results = []
    for paper in papers_list:
        marks = Result.objects.filter(paper=paper,student=student)
        if marks.count() > 0:
            results.append({"paper":paper.name,"marks":marks[0].marks})
    return results
@user_passes_test(is_student,login_url='/')
def Home(request):
    '''Home Page for student'''
    student = get_object_or_404(Student,user=request.user)
    types = SubjectType.objects.all()
    avg_lst = []
    for t in types:
        result = get_average_by_types(student,t)
        avg_lst.append({'type':t.name,'avg':result})
    # charts 
    papers_list = Paper.objects.filter(subject__semester=student.semester).order_by('id')
    
    if(papers_list.count()>0):

        results = get_bar_results(student,papers_list)
        results2 = get_score_history(student,papers_list)
        try:
            avg_score = round(sum(score) / len(score),2)
        except (ZeroDivisionError):
            print("No Result")
            avg_score = 0   
    else:
        avg_score = 0
        
    context = {
        'types':types,
        'avg_lst':avg_lst,
        'results':results,
        'averages':results2,
        'score': avg_score,
        'last_updated': last_updated,
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
    print(exams_list)
    context = {
        'exams_list': exams_list,
    }
    return render(request, 'student/check_result.html',context)
@user_passes_test(is_student,login_url='/') 
def leaderboard(request):
    types = SubjectType.objects.all()
    context = {
        'sub_types':types,
    }
    return render(request, 'student/leaderboard.html',context)
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
def get_papers_ajax(request,pk):
    papers = Paper.objects.filter(exam = pk)
    print(papers) 
    student = get_object_or_404(Student,user=request.user)
    print(papers)
    data = []
    for paper in papers:
        try:
            marks = Result.objects.get(paper=paper,student=student)
            data.append({"id":paper.id,"paper":paper.name,"subject":marks.paper.subject.name,"marks":marks.marks,"total":marks.paper.total_marks})
        except:
            pass
    return JsonResponse({"data":data})

 