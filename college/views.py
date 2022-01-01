from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from college.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate,logout,login
# Create your views here.

def home(request):
    return redirect('login')
def Login(request):
    return render(request,template_name='college/login.html')

def dologin(request):
    print(request.method)
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request,username = request.POST.get('email'),password = request.POST.get('password'))
        print(user.userType)
        if user != None:
            login(request,user)
            user_type = user.userType
            if user_type == '1':
                return HttpResponse("Admin")
            elif user_type == '2':
                return HttpResponse("Faculty")
            elif user_type == '3':
                return HttpResponse("Student")
            else:
                #message
                return redirect('login')
        else:
            #message
            return redirect('login')
    else:
        return redirect('login')