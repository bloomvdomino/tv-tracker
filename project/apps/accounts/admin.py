from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "max_following_shows",
        "is_active",
        "is_staff",
        "is_superuser",
        "created",
        "last_login",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("id", "email")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "created",
                    "last_login",
                    "email",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("Progresses", {"fields": ("max_following_shows",)}),
    )
    readonly_fields = ("id", "is_superuser", "created", "last_login", "email")

    def has_add_permission(self, request):
        return False
