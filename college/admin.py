from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
# class UserModel(UserAdmin):
#     list_display = ['username','userType']
class subjectModel(ModelAdmin):
    list_display = ['code','name']

admin.site.register(CustomUser)
admin.site.register(College)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(SubjectType)
admin.site.register(Student)
admin.site.register(SessionYear)
admin.site.register(Faculty) 
admin.site.register(Subject,subjectModel)
admin.site.register(Exam)
admin.site.register(Paper)
admin.site.register(Result)