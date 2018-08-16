from django.urls import path, re_path
from note import views

urlpatterns = [
	re_path('user-(?P<userid>\d+)/$', views.user_note),
	path('new/', views.note_new),
	re_path('(?P<noteid>\d+)/$', views.note_detail),
	re_path('(?P<noteid>\d+)/edit/', views.note_edit),
	path('delete/', views.note_delete),
	re_path('explore/', views.note_explore),
	re_path('user-(?P<userid>\d+)/fond/', views.user_fond_note),
	path('fond/', views.fond),
	path('cancel_fond/', views.cancel_fond),
]
