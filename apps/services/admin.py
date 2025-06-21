# admin.py
from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name_ar', 'name_en', 'sectors_list', 'link')
    search_fields = ('name_ar', 'name_en', 'description_ar', 'description_en')
    filter_horizontal = ('sectors',)
    list_filter = ('sectors',)

    def sectors_list(self, obj):
        return ", ".join([s.name_ar for s in obj.sectors.all()])

    sectors_list.short_description = 'Associated Sectors'