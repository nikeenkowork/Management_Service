from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "email",
        "role",
        "is_verified",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "is_verified",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "email",
    )

    ordering = (
        "email",
    )

    fieldsets = (
        (None, {
            "fields": (
                "email",
                "password",
            ),
        }),
        ("Персональная информация", {
            "fields": (
                "first_name",
                "last_name",
            ),
        }),
        ("Роль и права", {
            "fields": (
                "role",
                "is_verified",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        ("Важные даты", {
            "fields": (
                "last_login",
                "date_joined",
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "role",
                "is_verified",
                "is_active",
                "is_staff",
            ),
        }),
    )
