from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'type_id', 'is_active')
    list_filter = ('is_active', 'type_id')
    search_fields = ('email', 'first_name', 'last_name', 'mobile')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'father_name', 'birth', 'national_code', 'mobile', 'postal_code', 'type_id', 'pic')}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'type_id', 'first_name', 'last_name', 'mobile', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
