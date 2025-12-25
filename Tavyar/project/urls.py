# app/urls.py
from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('projects/', views.project_list, name='list'),
    path('projects/<int:pk>/', views.project_detail, name='detail'),
]
