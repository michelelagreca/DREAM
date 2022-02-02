# Harvest_report
from django.db import models
from django.utils import timezone
from users.models import CustomUser, Area
from forum.models import Category

# Create your models here.


class HarvestReport(models.Model):
    class ReportObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset()

    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    date = models.DateTimeField()
    area = models.ForeignKey(
        Area, on_delete=models.PROTECT, default=1)

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT)
    cropName = models.CharField(max_length=50)
    quantity = models.FloatField()
    genericProblems = models.CharField(max_length=500)
    weatherProblems = models.CharField(max_length=500)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='report')

    objects = models.Manager()  # default manager
    reportobjects = ReportObjects()  # custom manager

    class Meta:
        ordering = ('-date',)
