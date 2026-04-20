from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SupportEmployee
from tickets.models import EmployeeLanguage

class EmployeeLanguageInline(admin.TabularInline):
    model = EmployeeLanguage
    extra = 1

@admin.register(SupportEmployee)
class SupportEmployeeAdmin(UserAdmin):
    inlines = [EmployeeLanguageInline]
    model = SupportEmployee
    list_display = ("employee_id", "first_name", "last_name", "tier", "is_staff", "is_active")
    ordering = ("employee_id",)
    search_fields = ("employee_id", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("employee_id", "password")}),
        ("Personal info", {"fields": ("first_name", "middle_name", "last_name", "tier")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("employee_id", "first_name", "middle_name", "last_name", "tier", "password1", "password2", "is_staff", "is_active"),
        }),
    )