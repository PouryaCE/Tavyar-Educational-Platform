from django.shortcuts import render
from .models import User
from .forms import RegisterForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # لینک فعال‌سازی
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(f"/accounts/activate/{uid}/{token}/")

            # ارسال ایمیل
            mail_subject = "فعالسازی حساب کاربری"
            message = render_to_string('activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            email = EmailMessage(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            email.content_subtype = "html"
            email.send(fail_silently=False)

            return render(request, 'registration_complete.html', {'email': user.email})

        else:
            print(form.errors)  # اینجا خطاهای فرم چاپ می‌شوند
            return render(request, 'register.html', {'form': form})

    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # تا زمانی که ایمیل فعال نشود غیرفعال بماند
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # ساخت لینک فعال‌سازی
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(
                f"/accounts/activate/{uid}/{token}/"
            )

            # محتوای ایمیل (می‌توان از قالب استفاده کرد)
            mail_subject = "فعالسازی حساب کاربری"
            message = render_to_string('activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            email = EmailMessage(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            email.content_subtype = "html"
            email.send(fail_silently=False)
        else:
            print(form.errors)

            return render(request, 'registration_complete.html', {'email': user.email})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'activation_success.html', {'user': user})
    else:
        return render(request, 'activation_invalid.html')
