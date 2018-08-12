from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'created')
    search_fields = ('email',)
    fields = ('email', 'created', 'message')
    readonly_fields = ('email', 'created', 'message')

    def has_add_permission(self, request):
        return False
