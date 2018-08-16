from django.urls import path, re_path
from relationship import views

urlpatterns = [
	re_path('(?P<userid>\d+)/follows/$', views.follows),
	re_path('(?P<userid>\d+)/fans/$', views.fans),
	path('search/', views.search),
	path('follow/', views.follow),
	path('cancel_follow/', views.cancel_follow),
]
