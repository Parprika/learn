from django.urls import path, re_path
from note import views

urlpatterns = [
	path('new/', views.note_new),
	re_path('(?P<noteid>\d+)/$', views.note_detail),
	re_path('(?P<noteid>\d+)/edit/', views.note_edit),
	path('delete/', views.note_delete),
	path('fond/', views.fond),
	path('cancel_fond/', views.cancel_fond),
]
