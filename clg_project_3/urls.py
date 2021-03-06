"""clg_project_3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from college import views,adminViews 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.site.site_header = "SPT SuperAdmin"

urlpatterns = [
    path('', views.home, name="home"), #landing page
    path('admin/', admin.site.urls),
    path('college/', include('college.clg_urls')),
    path('faculty/', include('college.fac_urls')),
    path('student/',include('college.stu_urls')),
    path('login/', views.Login,name="login"),
    path('dologin/', views.dologin,name="do-login"),
    # add college admin
    path('add-college-admin/', views.add_college_admin,name="add-college-admin"),
    path('logout/', views.Logout,name="logout")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()