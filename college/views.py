from pydoc import resolve
from urllib import response
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from college.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import *

import csv
# Create your views here.

def is_superuser(user):
    '''checks if authenticated and is a student'''
    if user.is_authenticated:
        return user.is_superuser
    else:
        return False

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

@user_passes_test(is_superuser,login_url='/')
def add_college_admin(request):
    # <form id="quickForm" method="post" enctype="multipart/form-data">
    #                     {% csrf_token %}
    #                     <div class="card-body row">
    #                         <div class="form-group col-6">
    #                             <label>Username</label>
    #                             <input type="text" name="user_name" class="form-control" placeholder="Enter User name"
    #                                 required>
    #                         </div>
    #                         <div class="form-group col-6">
    #                             <label>E-mail</label>
    #                             <input type="email" name="email" class="form-control" placeholder="Enter email"
    #                                 required>
    #                         </div>
    #                         <div class="form-group col-6">
    #                             <label>Password</label>
    #                             <input type="password" name="password" class="form-control" placeholder="Enter Password"
    #                                 required>
    #                         </div>
    #                         <div class="form-group col-6">
    #                             <label>First Name</label>
    #                             <input type="text" name="first_name" class="form-control" placeholder="Enter First name"
    #                                 required>
    #                         </div>
    #                         <div class="form-group col-6">
    #                             <label>Last Name</label>
    #                             <input type="text" name="last_name" class="form-control" placeholder="Enter Last name"
    #                                 required>
    #                         </div>
    #                         <div class="form-group col-6">
    #                             <label>College</label>
    #                             <select type="" name="gender" class="form-control" placeholder="" required>
    #                                 <option value="">Select College</option>
    #                                 {% for college in colleges %}
    #                                     <option value="{{college.id}}">{{college.name}}</option>
    #                                 {% endfor %}
    #                             </select>
    #                         </div>
    #                         <div class="form-group col-6">
    #                             <label>Profile Photo</label>
    #                             <div class="custom-file">
    #                                 <input type="file" name="profile_pic" class="custom-file-input" id="customFile"
    #                                     required>
    #                                 <label class="custom-file-label" for="customFile">Choose Profile</label>
    #                             </div>
    #                         </div>
    #                         <div class="card-footer col-12">
    #                             <button type="submit" class="btn btn-primary">Add Faculty</button>
    #                         </div>
    #                 </form>
    if request.method == "POST":
        print(request.POST.get('college'))
        college = College.objects.get(id = request.POST.get('college'))
        user = CustomUser.objects.create_user(username = request.POST.get('user_name'),email = request.POST.get('email'),first_name = request.POST.get('first_name'),last_name = request.POST.get('last_name'),userType = '1',college = college, profile_pic = request.FILES.get('profile_pic'))
        user.set_password(request.POST.get('password'))
        user.save()
        messages.success(request,"College Admin Added Successfully")
        return redirect('add-college-admin')
    colleges = College.objects.all()
    context = {
        'colleges':colleges
    }
    return render(request,'college/add_college_admin.html',context)