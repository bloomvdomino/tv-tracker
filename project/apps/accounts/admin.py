from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser', 'max_followed_progresses',
                    'created')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    fields = ('id', 'email', 'is_active', 'is_staff', 'is_superuser', 'max_followed_progresses',
              'created')
    readonly_fields = ('id', 'is_superuser', 'created')

    def has_add_permission(self, request):
        return False
