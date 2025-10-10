from django.db import models
from django.utils import timezone
from accounts.models import User
from category.models import Category

class Course(models.Model):
    LEVEL_CHOICES = (
        (1, 'مقدماتی'),
        (2, 'متوسط'),
        (3, 'پیشرفته'),
    )

    FORMAT_CHOICES = (
        ('video', 'ویدیویی'),
        ('text', 'متنی'),
        ('mixed', 'ترکیبی'),
    )

    course_id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="دسته بندی")
    title = models.CharField(max_length=150, verbose_name="عنوان دوره")
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="سطح آموزش")
    length = models.IntegerField(verbose_name="طول دوره")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="مدرس دوره", related_name="courses")
    prerequisite = models.ManyToManyField('self', symmetrical=False, blank=True, verbose_name="پیش‌نیازها",related_name="required_for")
    has_certificate = models.BooleanField(default=False, verbose_name="گواهینامه دارد؟")
    has_exam = models.BooleanField(default=False, verbose_name="آزمون دارد؟")
    course_format = models.CharField(max_length=50, choices=FORMAT_CHOICES, verbose_name="فرمت آموزش")
    software = models.TextField(blank=True, null=True, verbose_name="نرم‌افزار موردنیاز")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="قیمت دوره")
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="قیمت با تخفیف")
    demo_pic = models.ImageField(blank=True, null=True, verbose_name="تصویر دمو")
    main_pic = models.ImageField(blank=True, null=True, verbose_name="تصویر اصلی")
    description = models.TextField(verbose_name="توضیحات دوره")
    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    class Meta:
        verbose_name = "دوره"
        verbose_name_plural = "دوره‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return self.title





class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="chapters", verbose_name="دوره")
    title = models.CharField(max_length=150, verbose_name="عنوان فصل")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات فصل")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        ordering = ['order']
        verbose_name = "فصل"
        verbose_name_plural = "فصل‌ها"

    def __str__(self):
        return f"{self.course.title} - {self.title}"




class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="lessons", verbose_name="فصل")
    title = models.CharField(max_length=150, verbose_name="عنوان درس")
    description = models.TextField(verbose_name="محتوای درس")
    video = models.CharField(max_length=500, verbose_name="ویدیو", help_text="لینک ویدیو را وارد کنید", blank=True, null=True)
    duration = models.DurationField(blank=True, null=True, verbose_name="مدت زمان")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        ordering = ['order']
        verbose_name = "درس"
        verbose_name_plural = "درس‌ها"

    def __str__(self):
        return f"{self.chapter.title} - {self.title}"