from .models import User
from .forms import RegisterForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # ✅ اعتبارسنجی ساده
        errors = []
        if not email or not password1 or not password2:
            errors.append("تمام فیلدها الزامی هستند.")
        if password1 != password2:
            errors.append("رمزهای عبور با هم مطابقت ندارند.")
        if User.objects.filter(email=email).exists():
            errors.append("ایمیل وارد شده قبلاً ثبت شده است.")

        if errors:
            return render(request, 'accounts/register.html', {'errors': errors})

        # ✅ ایجاد کاربر غیرفعال
        user = User(
            email=email,
            is_active=False
        )
        user.set_password(password1)
        user.save()

        # ✅ ساخت لینک فعال‌سازی
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = request.build_absolute_uri(f"/accounts/activate/{uid}/{token}/")

        # ✅ ارسال ایمیل فعال‌سازی
        mail_subject = "فعالسازی حساب کاربری"
        message = render_to_string('accounts/activation_email.html', {
            'user': user,
            'activation_link': activation_link,
        })
        email_message = EmailMessage(
            mail_subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        email_message.content_subtype = "html"
        email_message.send(fail_silently=False)

        # ✅ نمایش صفحه تأیید
        return render(request, 'accounts/registration_complete.html', {'email': user.email})

    # برای GET
    return render(request, 'accounts/register.html')




def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'accounts/activation_success.html', {'user': user})
    else:
        return render(request, 'accounts/activation_invalid.html')








def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"{user.email} خوش آمدی 🌸")
            return redirect("home:index")  # یا مسیر صفحه اصلی
        else:
            messages.error(request, "ایمیل یا رمز عبور اشتباه است ❌")

    return render(request, "accounts/login.html")