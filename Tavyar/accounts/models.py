# accounts/models.py
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone
from .manager import UserManager
import random



class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        (1, 'مدیر'),
        (2, 'مدرس'),
        (3, 'کاربر ویژه'),
        (4, 'کاربر عادی'),
    )


    email_verified = models.BooleanField(default=False, verbose_name="ایمیل تایید شده")
    verification_code = models.CharField(max_length=6, blank=True, null=True, verbose_name="کد تایید ایمیل")
    # custom fields
    email = models.EmailField(unique=True, max_length=255, verbose_name="ایمیل")
    type_id = models.IntegerField(null=True, blank=True, choices=USER_TYPES, verbose_name="نوع کاربر", default=4)  # نوع کاربر (یا FK به جدول نوع‌ها)
    mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name="شماره موبایل", unique=True)
    national_code = models.CharField(max_length=10, blank=True, null=True, unique=True, verbose_name="کد ملی")
    first_name = models.CharField(max_length=150, blank=True, verbose_name="نام")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="نام خانوادگی")
    father_name = models.CharField(max_length=150, blank=True, verbose_name="نام پدر")
    birth = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")
    pic = models.ImageField(upload_to='user_pics/', blank=True, null=True, verbose_name="عکس پروفایل")
    postal_code = models.CharField(max_length=20, blank=True, null=True)


    # standard django fields
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_staff = models.BooleanField(default=False)
    # created_at, updated_at
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # هنگام create_superuser تنها ایمیل و پسورد لازم است

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.email
    
    def generate_verification_code(self):
        code = str(random.randint(100000, 999999))
        self.verification_code = code
        self.save()
        return code
