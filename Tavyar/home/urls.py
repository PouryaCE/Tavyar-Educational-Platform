from django.urls import path
from .views import index_view, rules_view
app_name = 'home'


urlpatterns = [
    path('', index_view, name='index'),
    path('rules', rules_view, name='rules'),
]