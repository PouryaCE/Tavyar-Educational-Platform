from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.urls import reverse
from accounts.models import User
from category.models import Category
from django.conf import settings
from django.utils import timezone

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

    # اگر بخوای اسم پیش‌فرض id رو نگه داری، میتونی course_id رو حذف کنی
    course_id = models.AutoField(primary_key=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="دسته بندی", related_name="courses", db_index=True)
    title = models.CharField(max_length=150, verbose_name="عنوان دوره")
    slug = models.SlugField(max_length=160, unique=True, verbose_name="اسلاگ")
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="سطح آموزش", db_index=True)
    # واحد رو صریح کن: مثلاً دقیقه
    length_minutes = models.PositiveIntegerField(verbose_name="طول دوره (دقیقه)", default=0)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="مدرس دوره", related_name="courses", db_index=True)

    prerequisite = models.ManyToManyField('self', symmetrical=False, blank=True, verbose_name="پیش‌نیازها", related_name="required_for", help_text="دوره‌هایی که باید قبل از این گذرانده شوند")
    has_certificate = models.BooleanField(default=False, verbose_name="گواهینامه دارد؟")
    has_exam = models.BooleanField(default=False, verbose_name="آزمون دارد؟")
    course_format = models.CharField(max_length=50, choices=FORMAT_CHOICES, verbose_name="فرمت آموزش")
    software = models.TextField(blank=True, null=True, verbose_name="نرم‌افزار موردنیاز")

    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="قیمت دوره", validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="قیمت با تخفیف", validators=[MinValueValidator(0)], null=True, blank=True)

    demo_pic = models.URLField(blank=True, null=True, verbose_name="لینک تصویر دمو", max_length=500, help_text="لینک تصویر دمو را وارد کنید")
    main_pic = models.URLField(blank=True, null=True, verbose_name="لینک تصویر اصلی", max_length=500, help_text="لینک تصویر اصلی را وارد کنید")
    short_description = models.CharField(max_length=300, blank=True, null=True, verbose_name="توضیح کوتاه")
    description = models.TextField(verbose_name="توضیحات دوره")

    is_published = models.BooleanField(default=False, verbose_name="منتشر شده")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="تاریخ انتشار")

    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    class Meta:
        verbose_name = "دوره"
        verbose_name_plural = "دوره‌ها"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['teacher']),
            models.Index(fields=['level']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='price_non_negative'),
            # اگر discount_price موجود است باید کمتر یا مساوی price باشد
            models.CheckConstraint(check=(models.Q(discount_price__lte=models.F('price')) | models.Q(discount_price__isnull=True)), name='discount_lte_price'),
        ]

    def __str__(self):
        return self.title

    def get_price(self):
        """قیمت نهایی با اعمال تخفیف (اگر باشد)"""
        if self.discount_price is not None and self.discount_price > 0:
            return self.discount_price
        return self.price

    def get_total_duration(self):
        """محاسبه مجموع مدت زمان درس‌ها (در دقیقه)"""
        total = 0
        # اگر Lesson.duration را به عنوان DurationField داشته باشی باید تبدیل کنی
        for lesson in self.chapters.prefetch_related('lessons').all():
            for l in lesson.lessons.all():
                if l.duration:
                    total += int(l.duration.total_seconds() / 60)
        return total

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="chapters", verbose_name="دوره")
    title = models.CharField(max_length=150, verbose_name="عنوان فصل")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات فصل")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        ordering = ['order']
        verbose_name = "فصل"
        verbose_name_plural = "فصل‌ها"
        constraints = [
            models.UniqueConstraint(fields=['course', 'order'], name='unique_chapter_order_per_course')
        ]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="lessons", verbose_name="فصل")
    slug = models.SlugField(max_length=160, verbose_name="اسلاگ")
    title = models.CharField(max_length=150, verbose_name="عنوان درس")
    description = models.TextField(verbose_name="محتوای درس", blank=True)
    # اگر ویدیو لینک هست از URLField استفاده کن:
    video = models.URLField(max_length=500, verbose_name="لینک ویدیو", help_text="لینک ویدیو را وارد کنید", blank=True, null=True)
    # یا اگر فایل آپلود می‌شه از FileField:
    # video_file = models.FileField(upload_to='lessons/videos/', blank=True, null=True)
    duration = models.DurationField(blank=True, null=True, verbose_name="مدت زمان")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        ordering = ['order']
        verbose_name = "درس"
        verbose_name_plural = "درس‌ها"
        constraints = [
            models.UniqueConstraint(fields=['chapter', 'order'], name='unique_lesson_order_per_chapter')
        ]

    def __str__(self):
        return f"{self.chapter.title} - {self.title}"




