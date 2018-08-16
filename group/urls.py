from django.urls import path, re_path
from group import views

urlpatterns = [
	re_path('user-(?P<userid>\d+)/$', views.user_group),
	path('new/', views.group_new),
	re_path('(?P<groupid>\d+)/$', views.group_detail),
]
