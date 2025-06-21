from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import VisionMission, QuickAccessService, UniversityInfo, Statistics, StartYourFuture


# Resources
class VisionMissionResource(resources.ModelResource):
    class Meta:
        model = VisionMission


class QuickAccessServiceResource(resources.ModelResource):
    class Meta:
        model = QuickAccessService


class UniversityInfoResource(resources.ModelResource):
    class Meta:
        model = UniversityInfo


class StatisticsResource(resources.ModelResource):
    class Meta:
        model = Statistics


class StartYourFutureResource(resources.ModelResource):
    class Meta:
        model = StartYourFuture


# Admin classes
@admin.register(VisionMission)
class VisionMissionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = VisionMissionResource
    list_display = ('title', 'truncated_description', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

    def truncated_description(self, obj):
        return obj.description[:100] + '...' if len(obj.description) > 100 else obj.description

    truncated_description.short_description = 'Description'


@admin.register(QuickAccessService)
class QuickAccessServiceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = QuickAccessServiceResource
    list_display = ('title', 'linkname', 'formatted_link')
    search_fields = ('title', 'description', 'linkname')

    def formatted_link(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.link, obj.link)

    formatted_link.short_description = 'Link'


@admin.register(UniversityInfo)
class UniversityInfoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UniversityInfoResource
    list_display = ('title', 'image_previews', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('image_previews', 'created_at', 'updated_at')

    def image_previews(self, obj):
        return format_html(
            ' '.join(
                f'<img src="{img.url}" style="height:50px;" />'
                for img in [obj.image1, obj.image2, obj.image3] if img
            )
        )

    image_previews.short_description = 'Images'


@admin.register(Statistics)
class StatisticsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = StatisticsResource
    list_display = ('title', 'instructors', 'students', 'employees', 'foreign_students')
    list_editable = ('instructors', 'students', 'employees', 'foreign_students')


@admin.register(StartYourFuture)
class StartYourFutureAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = StartYourFutureResource
    list_display = ('title', 'subtitle', 'video_preview', 'created_at')
    search_fields = ('title', 'subtitle', 'description')
    readonly_fields = ('created_at', 'updated_at')

    def video_preview(self, obj):
        return format_html(
            '<a href="{}" target="_blank">Watch Video</a>',
            obj.videourl
        )

    video_preview.short_description = 'Preview'
