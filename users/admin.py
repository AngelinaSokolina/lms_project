from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Payment


class CustomUserAdmin(UserAdmin):
    """Настройка отображения пользователей в админке"""
    model = CustomUser
    list_display = ['email', 'phone', 'city', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['email', 'phone']

    # Поля для просмотра
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('phone', 'city', 'avatar')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login',)}),
    )

    # Поля для создания пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )

    ordering = ['email']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Настройка отображения платежей в админке"""
    list_display = ['user', 'payment_date', 'amount', 'payment_method', 'course', 'lesson']
    list_filter = ['payment_method', 'payment_date']
    search_fields = ['user__email']


# Регистрируем модель CustomUser
admin.site.register(CustomUser, CustomUserAdmin)