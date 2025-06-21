# admin.py
from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from ckeditor.widgets import CKEditorWidget
from django.db import models
from .models import NewsArticle, NewImage, NewVideo, NewsPdf


class NewsArticleResource(resources.ModelResource):
    class Meta:
        model = NewsArticle
        exclude = ('ar_content', 'en_content')


class MediaInline(admin.TabularInline):
    extra = 1
    readonly_fields = ('preview',)


class NewImageInline(MediaInline):
    model = NewImage
    fields = ('image', 'preview')

    def preview(self, obj):
        return format_html('<img src="{}" style="max-height:100px;" />', obj.image.url) if obj.image else "-"


class NewVideoInline(MediaInline):
    model = NewVideo
    fields = ('video', 'preview')

    def preview(self, obj):
        return format_html('<a href="{}" target="_blank">🎥 Preview</a>', obj.video.url) if obj.video else "-"


class NewsPdfInline(MediaInline):
    model = NewsPdf
    fields = ('pdf', 'preview')

    def preview(self, obj):
        return format_html('<a href="{}" target="_blank">📄 View</a>', obj.pdf.url) if obj.pdf else "-"


@admin.register(NewsArticle)
class NewsArticleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = NewsArticleResource
    formfield_overrides = {models.TextField: {'widget': CKEditorWidget}}
    inlines = [NewImageInline, NewVideoInline, NewsPdfInline]
    list_display = ('ar_title', 'en_title', 'type', 'is_active', 'created_at')
    search_fields = ('ar_title', 'en_title', 'ar_content', 'en_content')
    list_filter = ('ar_new_type', 'is_active')
    filter_horizontal = ('sectors',)
    readonly_fields = ('created_at', 'updated_at')

    def type(self, obj):
        return f"{obj.get_ar_new_type_display()} / {obj.get_en_new_type_display()}"


@admin.register(NewImage)
class NewImageAdmin(admin.ModelAdmin):
    list_display = ('news_article', 'preview')
    raw_id_fields = ('news_article',)

    def preview(self, obj):
        return format_html('<img src="{}" style="max-height:50px;" />', obj.image.url)


@admin.register(NewVideo)
class NewVideoAdmin(admin.ModelAdmin):
    list_display = ('news_article', 'preview')
    raw_id_fields = ('news_article',)

    def preview(self, obj):
        return format_html('<a href="{}" target="_blank">🎥 Play</a>', obj.video.url)


@admin.register(NewsPdf)
class NewsPdfAdmin(admin.ModelAdmin):
    list_display = ('news_article', 'preview')
    raw_id_fields = ('news_article',)

    def preview(self, obj):
        return format_html('<a href="{}" target="_blank">📄 Open</a>', obj.pdf.url)