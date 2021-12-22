from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.College)
admin.site.register(models.Cource)
admin.site.register(models.Semester)
admin.site.register(models.Subject_Type)
admin.site.register(models.Subject)
admin.site.register(models.Exam)
admin.site.register(models.Paper)