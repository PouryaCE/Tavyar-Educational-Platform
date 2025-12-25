# app/admin.py
from django.contrib import admin
from .models import Project
from django.utils.html import format_html

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview_image', 'technologies', 'created_at', 'github_link', 'live_demo_link')
    list_filter = ('created_at',)
    search_fields = ('title', 'technologies')
    readonly_fields = ('preview_image', 'created_at')  # اضافه کردن created_at به readonly
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'technologies', 'image', 'preview_image', 'github_url', 'live_demo')
        }),
        ('زمان‌بندی', {
            'fields': ('created_at',),  # الان بدون مشکل نمایش داده می‌شود
        }),
    )

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:120px; height:auto; border-radius:8px;" />', obj.image)
        return "تصویری ندارد"
    preview_image.short_description = 'پیش‌نمایش تصویر'

    def github_link(self, obj):
        if obj.github_url:
            return format_html('<a href="{}" target="_blank">گیت‌هاب</a>', obj.github_url)
        return '-'
    github_link.short_description = 'گیت‌هاب'

    def live_demo_link(self, obj):
        if obj.live_demo:
            return format_html('<a href="{}" target="_blank">نسخه آنلاین</a>', obj.live_demo)
        return '-'
    live_demo_link.short_description = 'نسخه آنلاین'

admin.site.register(Project, ProjectAdmin)
