from django.contrib import admin
from .models import Category





# Register your models here.
# ===============================
# Category Admin
# ===============================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('title',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'description')
        }),
        ('آیکون / تصویر', {
            'fields': ('icon',)
        }),
        ('زمان‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )