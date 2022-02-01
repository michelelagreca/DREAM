from django.db import models
from django.utils import timezone

from forum.models import Category
from users.models import CustomUser

HR_OPTIONS_EXT = [
    'accepted',
    'not_accepted',
    'closed',
    'declined',
]

TR_OPTIONS_EXT = [
        'pending',
        'review',
        'farmer',
        'declined',
        'accepted',
]


class HelpRequest(models.Model):
    HR_OPTIONS = (
        ('accepted', 'Accepted'),
        ('not_accepted', 'Not-accepted'),
        ('closed', 'Closed'),
        ('declined', 'Declined'),
    )

    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=250)
    content = models.TextField()

    author = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='hrrequest_author')
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='hrrequest_receiver')
    status = models.CharField(
        max_length=20, choices=HR_OPTIONS, default='not_accepted')

    objects = models.Manager()  # default manager

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return str(self.id) + " " + self.title


class TipRequest(models.Model):
    TIP_OPTIONS = (
        ('pending', 'Pending'),
        ('review', 'Policymaker Review'),
        ('farmer', 'Farmer Turn'),
        ('declined', 'Declined'),
        ('accepted', 'Accepted'),
    )

    timestamp = models.DateTimeField(default=timezone.now)
    proposed_title = models.CharField(max_length=250)
    proposed_tip = models.TextField()

    author = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='tiprequest_author')
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='tiprequest_receiver')
    status = models.CharField(
        max_length=20, choices=TIP_OPTIONS, default='not_accepted')
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, blank=False)

    objects = models.Manager()  # default manager

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return str(self.id) + " " + self.proposed_title
