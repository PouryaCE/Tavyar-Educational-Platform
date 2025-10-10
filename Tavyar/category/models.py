from django.db import models
from django.utils import timezone


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, verbose_name="عنوان دسته‌بندی")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    icon = models.TextField(blank=True, null=True, verbose_name="آیکون یا تصویر دسته")
    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['title']

    def __str__(self):
        return self.title
