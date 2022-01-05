from django.shortcuts import redirect,render

def Home(request):
    return render(request,"college/college_dashboard.html")
