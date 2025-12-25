from django.shortcuts import render
from project.models import Project

# Create your views here.


def index_view(request):
    projects = Project.objects.order_by('-created_at')[:3]
    context = {'projects': projects}
    return render(request, template_name="home/index.html", context=context)
