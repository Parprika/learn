from django.urls import path, re_path
from activity import views

urlpatterns = [
	path('new/', views.activity_new),
	re_path('(?P<activity_id>\d+)/$', views.activity_detail),
	path('end/', views.end_activity),
	path('join/', views.join_activity),
	path('quit/', views.quit_activity),
	re_path('(?P<activity_id>\d+)/sign/', views.sign),
	re_path('(?P<activity_id>\d+)/members/', views.members),
]
