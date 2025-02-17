from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок новости')

    main_image = models.ImageField(
        upload_to='news_images/',
        blank=True,
        null=True,
        verbose_name='Главное изображение',
    )

    preview_image = models.ImageField(
        upload_to='news_previews/',
        blank=True,
        null=True,
        verbose_name='Превью',
    )

    content = models.TextField(verbose_name='Текст новости')

    publication_date = models.DateTimeField(
        default=timezone.now, verbose_name='Дата публикации'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор новости',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        # Создание превью-изображения
        if self.main_image:
            img = Image.open(self.main_image)
            width, height = img.size
            min_side = min(width, height)
            new_size = (200, 200) if min_side >= 200 else (min_side, min_side)
            img.thumbnail(new_size, Image.LANCZOS)

            output = BytesIO()
            img.save(output, format='JPEG', quality=90)
            output.seek(0)

            self.preview_image = InMemoryUploadedFile(
                output,
                'ImageField',
                f'{self.main_image.name.split(".")[0]}_preview.jpg',
                'image/jpeg',
                sys.getsizeof(output),
                None,
            )
        super().save(*args, **kwargs)


class EmailTask(models.Model):
    recipients = models.TextField(help_text='Список адресатов (через запятую)')
    subject = models.CharField(max_length=255, help_text='Тема сообщения')
    message = models.TextField(help_text='Текст сообщения')
    send_at = models.DateTimeField(help_text='Время отправки')
    periodic_task = models.OneToOneField(
        PeriodicTask, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return f'EmailTask: {self.subject}'

    def save(self, *args, **kwargs) -> None:
        if not self.periodic_task:
            # Установка интервала
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=24, period=IntervalSchedule.HOURS
            )

            self.periodic_task = PeriodicTask.objects.create(
                interval=schedule,
                name=f'EmailTask: {self.subject}',
                task='news.tasks.send_custom_email',
                args=json.dumps([self.id]),
                start_time=self.send_at,
            )
        else:
            # Обновление время отправки, если оно изменилось
            self.periodic_task.start_time = self.send_at
            self.periodic_task.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:
        if self.periodic_task:
            self.periodic_task.delete()
        super().delete(*args, **kwargs)


class Comments(models.Model):
    content = models.TextField(max_length=200)

    related_news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
    )

    publication_date = models.DateTimeField(
        default=timezone.now, verbose_name='Дата комментария'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.content
