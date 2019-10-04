from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_staff", "is_superuser", "created", "last_login")
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("id", "email")
    fields = ("id", "created", "last_login", "email", "is_active", "is_staff", "is_superuser")
    readonly_fields = ("id", "created", "last_login", "email", "is_superuser")

    def has_add_permission(self, request):
        return False
