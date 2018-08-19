from django.contrib import admin

from .models import SendGridEmail


@admin.register(SendGridEmail)
class SendGridEmailAdmin(admin.ModelAdmin):
    list_display = ('title', 'template_id', 'categories')
    fields = ('title', 'template_id', 'categories')
