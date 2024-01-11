from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "activation_code", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ("username", 'first_name', 'last_name', 'activation_code')}),
        ('Permissions', {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        },
         ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', "username", 'password1', 'password2', 'activation_code'),
        }),
    )



# Aдминка для пользователя - как реализовать ее можно подсмотреть в документацию django
# Обычно её всегда оформляют, но в текущей задачи делать её необязательно
# @admin.register(CustomUser)
# class MyUserAdmin(admin.ModelAdmin):
#     model = CustomUser
#     list_display = ('email', 'phone', )
#     readonly_fields = ("image_", "last_login")
#     filter_horizontal = ()
#     list_filter = ('role', 'email')
#     list_per_page = 10
#     list_max_show_all = 100


admin.site.register(CustomUser, CustomUserAdmin)
