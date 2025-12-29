from django.shortcuts import render
from project.models import Project
from course.models import Course
# Create your views here.


def index_view(request):
    projects = Project.objects.order_by('-created_at')[:3]
    latest_courses = (
        Course.objects.select_related('teacher').order_by('-created_at')[:3]
    )
    context = {'projects': projects, 'latest_courses': latest_courses}
    return render(request, template_name="home/index.html", context=context)


def rules_view(request):
    return render(request, template_name="home/rules.html")


def help_view(request):
    return render(request, template_name="home/help.html")

def interest_view(request):
    return render(request, template_name="home/interest.html")