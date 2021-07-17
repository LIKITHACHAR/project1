"""vehicle URL Configuration

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
from django.urls import path 
from . import views
from  .import settings
from django.conf.urls.static import static

 

urlpatterns = [
    # path('admin/', admin.site.urls),
    #path('',include('newapi.urls'))
    path('', views.login),
    path('home.html', views.userregistration ),
    path('in.html',views.login),
    #path('loged.html',views.login),
    path('loged.html',views.linking),
    path('forgotpw.html',views.forgotpw),
    path('services.html',views.services),
    path('fine.html',views.fine),
    path('admin.html',views.admin),
    path('admin-lg.html',views.adminlgd),
    path("view",views.viewing),
    path('generate.html',views.generate),
    path('dock.html',views.dock),
    path("vnom",views.vnumber),
    path("udata/<unam>/",views.udata),
    path("verify",views.verify),
    path('uploadfine.html',views.uplfine),
    path('uploadcase.html',views.uplcase),
    path('status.html',views.status),
    path('trans.html',views.trans),
    path("reject",views.reject),
    path("reupload",views.reupload),
    path("payfine",views.payfine),
    path("clrfine",views.clrfine),
    # path("search",views.search),
    path('admn',views.admn,name='admn'),
    
]
if settings.DEBUG:
    
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
