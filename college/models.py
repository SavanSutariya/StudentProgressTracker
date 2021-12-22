from django.db import models

# Create your models here.

class College(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()

class Cource(models.Model):
    name =  models.CharField(max_length=50)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

class Semester(models.Model):
    numberOfSem = models.IntegerField()
    course = models.ForeignKey(Cource, on_delete=models.CASCADE)

class Subject_Type(models.Model):
    name = models.CharField(max_length=30)

class Subject(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Subject_Type,on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)

class Exam(models.Model):
    name = models.CharField(max_length=50)

class Paper(models.Model):
    total_marks = models.IntegerField()
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)

# remaining stuff all types of users
# Subject allocation, feedback, result,