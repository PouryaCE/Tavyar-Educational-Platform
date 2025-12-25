# app/views.py
from django.shortcuts import render, get_object_or_404
from .models import Project


def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'project/project_list.html', {'projects': projects})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    technologies = []
    if project.technologies:
        technologies = [t.strip() for t in project.technologies.split(',')]

    return render(request, 'project/project_detail.html', {
        'project': project,
        'technologies': technologies,
    })
