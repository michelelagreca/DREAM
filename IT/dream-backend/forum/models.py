from email.policy import default
from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import CustomUser, Area


# Forum Model definition


class Category(models.Model):
    name = models.CharField(max_length=100)

    class CategoryObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset()

    objects = models.Manager()
    categoryobjects = CategoryObjects()

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Question(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=250)
    text_body = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='forum_Questions')
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default='1')
    area = models.ForeignKey(
        Area, on_delete=models.PROTECT, default=1)
    objects = models.Manager()

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return self.title


class Tip(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=250)
    text_body = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='forum_Tips')
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default='1')
    area = models.ForeignKey(
        Area, on_delete=models.PROTECT, default=1)
    likes = models.ManyToManyField(CustomUser, blank=True, related_name='user_likes_tip')
    dislikes = models.ManyToManyField(CustomUser, blank=True, related_name='user_dislikes_tip')
    is_star = models.BooleanField()
    objects = models.Manager()

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return self.title


class Answer(models.Model):
    class AnswerObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset()

    timestamp = models.DateTimeField(default=timezone.now)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE)
    text_body = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='forum_Answers')
    likes = models.ManyToManyField(CustomUser, blank=True, related_name='user_likes_answer')
    dislikes = models.ManyToManyField(CustomUser, blank=True, related_name='user_dislikes_answer')
    objects = models.Manager()
    answerobjects = AnswerObjects()

    class Meta:
        ordering = ('-timestamp',)

    # def __str__(self):
    #     return self.title
