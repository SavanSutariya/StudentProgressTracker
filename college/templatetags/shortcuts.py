from django import template
from ..models import *
register = template.Library()

@register.filter(name='printname')
def printname(value):
    return "Hello "+value

@register.filter(name='get_result')
def get_result(student,paper):
    try:
        result = Result.objects.get(student=student,paper=paper)
        return result.marks
    except:
        return None