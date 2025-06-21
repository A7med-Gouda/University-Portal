# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Sector


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'name_en', 'sector_type', 'current_head', 'created_at')
    search_fields = ('name_ar', 'name_en', 'description_ar', 'description_en')
    list_filter = ('sector_type', 'created_at')
    raw_id_fields = ('head',)
    readonly_fields = ('created_at', 'updated_at', 'image_preview', 'structure_preview')

    fieldsets = (
        ('Arabic Content', {
            'fields': (
                'name_ar',
                'description_ar',
                'message_ar',
                'speech_ar'
            )
        }),
        ('English Content', {
            'fields': (
                'name_en',
                'description_en',
                'message_en',
                'speech_en'
            )
        }),
        ('Media & Structure', {
            'fields': (
                'image',
                'image_preview',
                'organizational_structure',
                'structure_preview'
            )
        }),
        ('Relationships', {
            'fields': (
                'sector_type',
                'head',
            )
        }),
        ('Metadata', {
            'fields': (
                'created_at',
                'updated_at'
            )
        }),
    )

    def image_preview(self, obj):
        return format_html('<img src="{}" style="max-height: 200px;" />', obj.image.url) if obj.image else "-"

    image_preview.short_description = 'Image Preview'

    def structure_preview(self, obj):
        return format_html('<img src="{}" style="max-height: 200px;" />',
                           obj.organizational_structure.url) if obj.organizational_structure else "-"

    structure_preview.short_description = 'Structure Preview'

    def current_head(self, obj):
        return obj.head.user.get_full_name() if obj.head else "-"

    current_head.short_description = 'Current Head'