from django.contrib import admin

from source.apps.website.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "user", "created")
    search_fields = ("user__email", "email")
    fields = ("user", "email", "created", "message")
    readonly_fields = ("user", "email", "created", "message")

    def has_add_permission(self, request):
        return False
