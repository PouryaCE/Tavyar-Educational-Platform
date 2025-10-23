from django.contrib import admin
from .models import Course, Chapter, Lesson


# ===============================
# Inline برای نمایش و مدیریت درس‌ها در فصل
# ===============================
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'video', 'duration', 'order')
    ordering = ('order',)
    show_change_link = True


# ===============================
# Inline برای نمایش فصل‌ها در دوره
# ===============================
class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 1
    fields = ('title', 'description', 'order')
    ordering = ('order',)
    show_change_link = True


# ===============================
# Admin برای Course (دوره‌ها)
# ===============================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'teacher', 'level', 'price', 'has_certificate', 'created_at')
    list_filter = ('level', 'has_certificate', 'has_exam', 'course_format', 'category')
    search_fields = ('title', 'teacher__username', 'category__name')
    inlines = [ChapterInline]
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('مشخصات کلی دوره', {
            'fields': ('title', 'category', 'teacher', 'level', 'course_format', 'length_minutes')
        }),
        ('اطلاعات تکمیلی', {
            'fields': ('prerequisite', 'software', 'description')
        }),
        ('قیمت و گواهینامه', {
            'fields': ('price', 'discount_price', 'has_certificate', 'has_exam')
        }),
        ('تصاویر', {
            'fields': ('demo_pic', 'main_pic')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    verbose_name = "دوره"
    verbose_name_plural = "دوره‌ها"


# ===============================
# Admin برای Chapter (فصل‌ها)
# ===============================
@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    inlines = [LessonInline]
    ordering = ('course', 'order')


# ===============================
# Admin برای Lesson (درس‌ها)
# ===============================
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'video', 'duration', 'order')
    list_filter = ('chapter__course',)
    search_fields = ('title', 'chapter__title')
    ordering = ('chapter', 'order')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('مشخصات درس', {
            'fields': ('chapter', 'title', 'slug', 'order', 'duration')
        }),
        ('محتوا و ویدیو', {
            'fields': ('description', 'video')
        }),
    )
