from django.db import models

class VisionMission(models.Model):
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class QuickAccessService(models.Model):
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    linkname = models.CharField(max_length=255)
    # icon = models.ImageField(upload_to='quick_services/', blank=True, null=True)

    def __str__(self):
        return self.name

class UniversityInfo(models.Model):

    title = models.CharField(max_length=255)
    content = models.TextField()
    image1 = models.ImageField(upload_to='university_info/', blank=True, null=True)
    image2 = models.ImageField(upload_to='university_info/', blank=True, null=True)
    image3 = models.ImageField(upload_to='university_info/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Statistics(models.Model):

    title = models.CharField(max_length=255, default='احصائيات جامعة دمنهور', editable=False)
    instructors = models.PositiveIntegerField()
    students = models.PositiveIntegerField()
    employees = models.PositiveIntegerField()
    foreign_students = models.PositiveIntegerField()
    programs = models.PositiveIntegerField()
    colleges = models.PositiveIntegerField()

class StartYourFuture(models.Model):
    title = models.CharField(max_length=255, default='ابدأ مستقبلك', editable=False)
    subtitle = models.CharField(max_length=255, default='التقديم مفتوح الأن', editable=False)
    description = models.TextField()
    videourl = models.URLField() # youtube url
    url = models.URLField()
    moredetails = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title