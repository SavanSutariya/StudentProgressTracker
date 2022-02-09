from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
# Create your models here.
class College(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='media/college_logo')

    def __str__(self):
        return self.name
    def save(self):
        img = Image.open(self.logo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        super().save()
    

class Course(models.Model):
    name = models.CharField(max_length=50)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    def __str__(self):
        return self.name+" :"+self.college.name

class Semester(models.Model):
    number = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        # return str(self.number)
        return self.course.name+" :"+str(self.number)
    def get_subjects(self):
        return Subject.objects.filter(semester=self)

class CustomUser(AbstractUser):
    USER = (('1',"CollegeAdmin"),('2',"Faculty"),('3',"Student") )
    userType = models.CharField(choices=USER,default=1, max_length=50)
    profile_pic = models.ImageField(upload_to='media/profile_pic')
    college = models.ForeignKey(College, on_delete=models.CASCADE)

class Faculty(models.Model):
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=7, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SubjectType(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Subject(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    sub_type = models.ForeignKey(SubjectType, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty , on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    # def save(self):
    #     super().save()
    #     img = Image.open(self.profile_pic.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_pic.path)

class SessionYear(models.Model):
    session_start = models.CharField(max_length=100)
    session_end = models.CharField(max_length=100)

class Student(models.Model):
    user = models.OneToOneField(CustomUser , on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=7, null=False)
    session_year = models.ForeignKey(SessionYear , on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

class Exam(models.Model):
    name = models.CharField(max_length=50)
    session_year = models.ForeignKey(SessionYear , on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    date = models.DateField()
    def __str__(self):
        return self.name

class Paper(models.Model):
    name = models.CharField(max_length=50)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    def __str__(self):
        return self.name

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    marks = models.IntegerField()
    def __str__(self):
        return self.paper.name+" : "+str(self.marks)