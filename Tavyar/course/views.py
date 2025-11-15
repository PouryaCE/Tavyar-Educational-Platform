# courses/views.py
from django.shortcuts import render, redirect
from .models import Course, Lesson
from django.shortcuts import get_object_or_404



def course_list(request):
    courses = Course.objects.all().select_related('teacher', 'category')
    return render(request, 'course/course_list.html', {'courses': courses})


def course_detail(request, slug):
    """وقتی کاربر وارد صفحه‌ی دوره شد، اولین درس را باز کن."""
    course = get_object_or_404(
        Course.objects.prefetch_related('chapters__lessons'),
        slug=slug
    )

    # پیدا کردن اولین فصل و اولین درس
    first_chapter = course.chapters.first()
    if first_chapter and first_chapter.lessons.exists():
        first_lesson = first_chapter.lessons.first()
        return redirect('courses:lesson_detail', course_slug=course.slug, lesson_slug=first_lesson.slug)

    # اگر هنوز درسی وجود ندارد
    return render(request, 'course/course_empty.html', {'course': course})


def lesson_detail(request, course_slug, lesson_slug):
    """نمایش درس انتخاب‌شده همراه با منوی فصل‌ها و درس‌ها."""
    lesson = get_object_or_404(
        Lesson.objects.select_related('chapter__course'),
        slug=lesson_slug,
        chapter__course__slug=course_slug
    )

    course = lesson.chapter.course
    chapters = course.chapters.prefetch_related('lessons').all()

    context = {
        'course': course,
        'lesson': lesson,
        'chapters': chapters,
    }
    return render(request, 'course/lesson_detail.html', context)
