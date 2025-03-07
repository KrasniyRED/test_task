# Generated by Django 5.1.6 on 2025-02-14 08:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_emailtask'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор новости'),
        ),
        migrations.AlterField(
            model_name='news',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to='news_images/', verbose_name='Главное изображение'),
        ),
    ]
