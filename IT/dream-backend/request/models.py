from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Forum Model definition

class HelpRequest(models.Model):

    class HRObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )


    title = models.CharField(max_length=250)
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    # author = models.ForeignKey(
    #     User, on_delete=models.PROTECT, related_name='request_HelpRequest')
    #RECEIVER
    # receiver = models.ForeignKey(
    #     User, on_delete=models.PROTECT, related_name='request_HelpRequest')

    status = models.CharField(
        max_length=10, choices=options, default='published')
    #objects = models.Manager()  # default manager
    #hrobjects = HRObjects()  # custom manager

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title
