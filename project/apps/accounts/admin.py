from django.contrib import admin

from .models import PasswordResetToken, User


class AddedProgressesFilter(admin.SimpleListFilter):
    title = "Added progresses"
    parameter_name = 'added_progresses'

    def lookups(self, request, model_admin):
        return [('yes', "Yes"), ('no', "No")]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        ids = [user.id for user in queryset if user.added_progresses_count]
        if self.value() == 'yes':
            return queryset.filter(id__in=ids)
        return queryset.exclude(id__in=ids)


class FollowedProgressesFilter(admin.SimpleListFilter):
    title = "Followed progresses"
    parameter_name = 'followed_progresses'

    def lookups(self, request, model_admin):
        return [('yes', "Yes"), ('no', "No")]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        ids = [user.id for user in queryset if user.followed_progresses_count]
        if self.value() == 'yes':
            return queryset.filter(id__in=ids)
        return queryset.exclude(id__in=ids)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'added_progresses_count', 'followed_progresses_count',
                    'max_followed_progresses', 'is_active', 'is_staff', 'is_superuser',
                    'created')
    list_filter = (AddedProgressesFilter, FollowedProgressesFilter, 'is_active', 'is_staff',
                   'is_superuser')
    search_fields = ('id', 'email',)
    fieldsets = (
        (None, {
            'fields': ('id', 'created', 'email', 'is_active', 'is_staff', 'is_superuser')
        }),
        ("Progresses", {
            'fields': ('added_progresses_count', 'followed_progresses_count',
                       'max_followed_progresses')
        }),
    )
    readonly_fields = ('id', 'is_superuser', 'added_progresses_count', 'followed_progresses_count',
                       'created')

    def has_add_permission(self, request):
        return False


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_valid', 'created')
    search_fields = ('user__email',)
    fields = ('id', 'user', 'is_valid', 'created')
    readonly_fields = ('id', 'user', 'is_valid', 'created')

    def is_valid(self, obj):
        return obj.is_valid
    is_valid.boolean = True

    def has_add_permission(self, request):
        return False
