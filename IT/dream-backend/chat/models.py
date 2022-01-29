from django.db import models
from django.utils import timezone
from request.models import HelpRequest, TipRequest


# Create your models here.

class HrMessage(models.Model):
    timestamp = models.DateTimeField(default=timezone.now, blank=False)
    body = models.CharField(max_length=250, blank=False)
    isFromSender = models.BooleanField(blank=False)  # in the context where they are associated
    reference_hr = models.ForeignKey(HelpRequest, on_delete=models.CASCADE, blank=False)

    objects = models.Manager()

    class Meta:
        ordering = ('-timestamp',)


def __str__(self):
    return self.body


class TipMessage(models.Model):
    timestamp = models.DateTimeField(default=timezone.now, blank=False)
    body = models.CharField(max_length=250, blank=False)
    isFromFarmer = models.BooleanField(blank=False)  # in the context where they are associated
    reference_tip = models.ForeignKey(TipRequest, on_delete=models.CASCADE, blank=False)

    objects = models.Manager()

    class Meta:
        ordering = ('-timestamp',)


def __str__(self):
    return self.body
