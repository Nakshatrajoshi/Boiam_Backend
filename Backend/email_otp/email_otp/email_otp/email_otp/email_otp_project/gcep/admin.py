from django.contrib import admin

from .models import ContactForm


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'institute', 'created_at')
    list_filter = ('created_at', 'institute')
    search_fields = ('first_name', 'last_name', 'email', 'institute', 'message')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Professional Information', {
            'fields': ('institute', 'designation', 'job_title')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
