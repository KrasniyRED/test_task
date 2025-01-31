from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class News(models.Model):
    
    title = models.CharField(max_length=200, verbose_name="Заголовок новости")
    
    main_image = models.ImageField(upload_to='news_images/', verbose_name="Главное изображение")
    
    preview_image = models.ImageField(upload_to='news_previews/',blank=True,null=True, verbose_name="Превью")

    content = models.TextField(verbose_name="Текст новости")
    
    publication_date = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор новости")

    def save(self, *args, **kwargs):
        # Создание превью-изображения
        if self.main_image:
            img = Image.open(self.main_image)
            width, height = img.size
            min_side = min(width, height)
            new_size = (200, 200) if min_side >= 200 else (min_side, min_side)
            img.thumbnail(new_size, Image.ANTIALIAS)

            output = BytesIO()
            img.save(output, format='JPEG', quality=90)
            output.seek(0)

            self.preview_image = InMemoryUploadedFile(
                output, 'ImageField', f"{self.main_image.name.split('.')[0]}_preview.jpg",
                'image/jpeg', sys.getsizeof(output), None
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
