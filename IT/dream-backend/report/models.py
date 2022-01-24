# Harvest_report
from django.db import models
from django.utils import timezone
from users.models import CustomUser, Zone
from forum.models import Category

# Create your models here.


class HarvestReport(models.Model):
    class ReportObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    date = models.DateTimeField()
    zone = models.ForeignKey(
        Zone, on_delete=models.PROTECT, default=1)

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default=1)
    cropName = models.CharField(max_length=50)
    quantity = models.FloatField()
    genericProblems = models.CharField(max_length=500)
    weatherProblems = models.CharField(max_length=500)

    slug = models.SlugField(max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='report')
    status = models.CharField(
        max_length=10, choices=options, default='published')
    objects = models.Manager()  # default manager
    reportobjects = ReportObjects()  # custom manager

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self
