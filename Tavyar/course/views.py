# courses/views.py
from django.shortcuts import render
from .models import Course
from django.shortcuts import get_object_or_404



def course_list(request):
    courses = Course.objects.all().select_related('teacher', 'category')
    return render(request, 'course/course_list.html', {'courses': courses})


def course_detail(request, id):
    course = get_object_or_404(
        Course.objects.prefetch_related('chapters__lessons'),
        course_id=id
    )
    first_lesson = None
    if course.chapters.exists():
        first_chapter = course.chapters.first()
        if first_chapter.lessons.exists():
            first_lesson = first_chapter.lessons.first()
    return render(request, 'course/course_detail.html', {
        'course': course,
        'first_lesson': first_lesson,
    })
