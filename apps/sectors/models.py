from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from uuid import uuid4


class Sector(models.Model):
    """Model representing a university sector with bilingual support"""

    class SectorType(models.TextChoices):
        MAIN = 'main', _('القطاع الرئيسي')
        UNITS = 'units', _('الوحدات')
        CENTERS = 'centers', _('المراكز')
        SECTOR = 'sector', _('القطاع الفرعي')

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sector_type = models.CharField(
        max_length=10,
        choices=SectorType.choices,
        default=SectorType.MAIN,
        verbose_name=_('نوع القطاع')
    )

    # Arabic Fields
    name_ar = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('الاسم بالعربية')
    )
    description_ar = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name=_('الوصف بالعربية')
    )
    message_ar = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_('رسالة القطاع بالعربية')
    )
    speech_ar = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name=_('كلمة رئيس القطاع بالعربية')
    )

    # English Fields
    name_en = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('الاسم بالإنجليزية')
    )
    description_en = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name=_('الوصف بالإنجليزية')
    )
    message_en = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_('رسالة القطاع بالإنجليزية')
    )
    speech_en = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name=_('كلمة رئيس القطاع بالإنجليزية')
    )

    # Media Fields
    image = models.ImageField(
        upload_to='sectors/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name=_('صورة القطاع الرئيسية')
    )
    organizational_structure = models.ImageField(
        upload_to='sectors/structures/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name=_('الهيكل التنظيمي'),
        help_text=_('رفع صورة الهيكل التنظيمي للقطاع')
    )

    # Relationships
    head = models.OneToOneField(
        'users.Staff',
        on_delete=models.SET_NULL,
        related_name='headed_sectors',
        null=True,
        blank=True,
        verbose_name=_('رئيس القطاع'),
        help_text=_('اختر الموظف المسؤول عن هذا القطاع')
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    class Meta:
        verbose_name = _('قطاع')
        verbose_name_plural = _('القطاعات')
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['name_ar', 'name_en'],
                name='unique_sector_names'
            )
        ]
        indexes = [
            models.Index(fields=['name_ar'], name='name_ar_idx'),
            models.Index(fields=['name_en'], name='name_en_idx'),
        ]

    def __str__(self):
        return f"{self.name_ar} / {self.name_en}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('sector-detail', args=[str(self.id)])

    @property
    def current_head(self):
        """Get current head or acting head"""
        return self.head or self.staff_members.filter(is_acting_head=True).first()

    @property
    def logo_url(self):
        """Get absolute URL for sector logo"""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/images/default-sector-logo.png'

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


# class SectorService(models.Model):
#     """الخدمات المقدمة ضمن كل قطاع"""
#     sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='services')
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     link = models.URLField(blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.name} - {self.sector.name}"