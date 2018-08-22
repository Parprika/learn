"""learn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from web import views
from utils import kindeditor
from utils import relationship

urlpatterns = [
	path('admin/', admin.site.urls),
	path('login/', views.login),
	path('logout/', views.logout),
	path('index/', views.index),
	path('n/', include('note.urls')),
	path('upload/', kindeditor.upload),
	re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
	path('a/', include('activity.urls')),
	path('search/', include('search.urls')),
	path('follow/', relationship.follow),
	path('cancel_follow/', relationship.cancel_follow),
	re_path('u/(?P<userid>\d+)/message/', views.message),
	re_path('u/(?P<userid>\d+)/notice/', views.notice),
	re_path('u/(?P<userid>\d+)/note/', views.user_note),
	re_path('u/(?P<userid>\d+)/fond/', views.user_fond),
	re_path('u/(?P<userid>\d+)/follows/', views.user_follows),
	re_path('u/(?P<userid>\d+)/fans/', views.user_fans),
	re_path('u/(?P<userid>\d+)/activity/', views.user_activity),
]
