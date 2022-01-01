from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    USER = (('1',"CollegeAdmin"),('2',"Faculty"),('3',"Student") )
    userType = models.CharField(choices=USER,default=1, max_length=50)
    profile_pic = models.ImageField(upload_to='media/profile_pic')
