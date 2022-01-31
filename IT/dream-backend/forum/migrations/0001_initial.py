# Generated by Django 4.0 on 2022-01-31 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=250)),
                ('text_body', models.TextField()),
                ('is_star', models.BooleanField()),
                ('area', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='users.area')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_Tips', to='users.customuser')),
                ('category', models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='forum.category')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='user_dislikes_tip', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='user_likes_tip', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=250)),
                ('text_body', models.TextField()),
                ('area', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='users.area')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_Questions', to='users.customuser')),
                ('category', models.ForeignKey(default='1', on_delete=django.db.models.deletion.PROTECT, to='forum.category')),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('text_body', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_Answers', to='users.customuser')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='user_dislikes_answer', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='user_likes_answer', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.question')),
            ],
            options={
                'ordering': ('-timestamp',),
            },
        ),
    ]
