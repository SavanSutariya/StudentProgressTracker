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

    # if (marks < 36) {
    #     return "dark"
    # } else if (marks < 48) {
    #     return "danger"
    # } else if (marks < 55) {
    #     return "warning"
    # } else if (marks < 60) {
    #     return "info"
    # } else if (marks < 70) {
    #     return "primary"
    # } else if (marks < 85) {
    #     return "success"
    # } else {
    #     return "success"
    # }

@register.filter(name='get_class_according_to_marks')
def get_class_according_to_marks(marks):
    if (marks < 36):
        return "dark"
    elif (marks < 48):
        return "danger"
    elif (marks < 55):
        return "warning"
    elif (marks < 60):
        return "info"
    elif (marks < 70):
        return "primary"
    elif (marks < 85):
        return "success"
    else:
        return "success"
