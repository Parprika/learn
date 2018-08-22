from django.urls import path, re_path
from search import views

urlpatterns = [
	path('n/', views.search_note),
	path('u/', views.search_user),
	path('a/', views.search_activity),
]
