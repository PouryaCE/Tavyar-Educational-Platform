from django.urls import path
from .views import index_view, rules_view, help_view, interest_view
app_name = 'home'


urlpatterns = [
    path('', index_view, name='index'),
    path('rules', rules_view, name='rules'),
    path('help', help_view, name='help'),
    path('interest', interest_view, name='interest'),
]