from pydoc import resolve
from urllib import response
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from college.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from .models import *

import csv
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        if request.user.userType == '1':
            return redirect('college-home')
        elif request.user.userType == '2':
            return redirect('faculty-home')
        elif request.user.userType == '3':
            return redirect('student-home')
            
    else:
        return redirect('login')
def Login(request): 
    return render(request,template_name='college/login.html')
def Logout(request):
    logout(request)
    return redirect('home')
def dologin(request):
    if request.method == "POST":
        '''if request.POST.get('email') == "":
            messages.error(request , "Email is required")
            return redirect('login')
        elif request.POST.get('password') == "":
            messages.error(request , "Password is required")
            return redirect('login')'''
           

        user = EmailBackEnd.authenticate(request,username = request.POST.get('email'),password = request.POST.get('password'))
        if user != None:
            login(request,user)
            user_type = user.userType
            if user_type == '1':
                messages.info(request,f"welcome {user.get_full_name()}")
                return redirect('college-home')
            elif user_type == '2':
                messages.info(request,f"welcome {user.get_full_name()}")
                return redirect('faculty-home')
            elif user_type == '3':
                messages.info(request,f"welcome {user.get_full_name()}")
                return redirect('student-home')
            else:
                messages.error(request,"User type dosen't match")
                return redirect('login')
        else:
            messages.error(request,"Incorrect credentials")
            return redirect('login')
    else:
        return redirect('login')

def exportCsv():
    response = HttpResponse(content_type = 'text/csv')
    writer = csv.writer(response)
    writer.writerow(['username','first_name','last_name'])

    for user in CustomUser.objects.all().values_list('username','first_name','last_name'):
        writer.writerow(user)
    
    response['Content-Disposition'] = 'attachment; filename="user.csv"'