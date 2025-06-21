from bleach import clean
from django.db import models
from apps.sectors.models import Sector

class NewsArticle(models.Model):
    
    EN_NEWS_TYPES = [
        ('ad', 'advertisement'),
        ('event', 'event'),
        ('new', 'new'),
    ]

    AR_NEWS_TYPES = [
        ('اعلان', 'اعلان'),
        ('حدث', 'حدث'),
        ('خبر', 'خبر'),
    ]

    ar_title = models.CharField(max_length=255)
    en_title = models.CharField(max_length=255)
    ar_description = models.TextField(blank=True, null=True)
    en_description = models.TextField(blank=True, null=True)
    ar_content = models.TextField(blank=True, null=True)
    en_content = models.TextField(blank=True, null=True)
    ar_keywords = models.JSONField(blank=True, null=True, default=list)
    en_keywords = models.JSONField(blank=True, null=True, default=list)
    ar_source = models.CharField(max_length=255, blank=True, null=True)
    en_source = models.CharField(max_length=255, blank=True, null=True)

    image = models.ImageField(upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ar_new_type = models.CharField(max_length=20, choices=AR_NEWS_TYPES)
    en_new_type = models.CharField(max_length=20, choices=EN_NEWS_TYPES)
    sectors = models.ManyToManyField(Sector, related_name='news')
    is_active = models.BooleanField(default=True)
    is_event = models.BooleanField(default=False)
    month = models.PositiveIntegerField(blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    event_link = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.ar_content = clean(self.ar_content)
        self.en_content = clean(self.en_content)
        self.is_event = self.en_new_type == 'event'
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"


class MediaModel(models.Model):
    news_article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class NewImage(MediaModel):
    image = models.ImageField(upload_to='news/images/')


class NewVideo(MediaModel):
    video = models.FileField(upload_to='news/videos/')


class NewsPdf(MediaModel):
    pdf = models.FileField(upload_to='news/pdfs/')