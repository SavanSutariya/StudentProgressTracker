from django.shortcuts import HttpResponse, redirect, render,get_object_or_404
from django.contrib.auth.decorators import user_passes_test
import os
from college.adminViews import students_list
from .models import *
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import Http404

def is_student(user):
    '''checks if authenticated and is a Student'''
    if user.is_authenticated:
        return user.userType == '3'
    else:
        return False

@user_passes_test(is_student)
def Home(request):
    Home(request):
    '''Home Page for student'''
    return render(request, 'student/student_home.html')