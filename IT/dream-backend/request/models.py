from django.db import models
from django.utils import timezone


# HelpRequest Model definition
from users.models import CustomUser


class HelpRequest(models.Model):
    class HRObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('accepted', 'Accepted'),
        ('not_accepted', 'Not-accepted'),
        ('closed', 'Closed'),
    )
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=250)
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='hrrequest_author')
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='hrrequest_receiver')

    status = models.CharField(
        max_length=20, choices=options, default='not_accepted')

    objects = models.Manager()  # default manager

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return str(self.id) + " " + self.title


class TipRequest(models.Model):
    class TRObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    proposed_title = models.CharField(max_length=250)
    proposed_tip = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    # author = models.ForeignKey(
    #     User, on_delete=models.PROTECT, related_name='request_HelpRequest')
    # RECEIVER
    # receiver = models.ForeignKey(
    #     User, on_delete=models.PROTECT, related_name='request_HelpRequest')

    status = models.CharField(
        max_length=10, choices=options, default='published')

    # objects = models.Manager()  # default manager
    # trobjects = TRObjects()  # custom manager

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title
