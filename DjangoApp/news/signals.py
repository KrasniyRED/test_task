from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News
from .tasks import send_news_notification


@receiver(post_save, sender=News)
def notify_about_new_news(sender, instance, created, **kwargs) -> None:
    if created:  # Проверяем, что новость только что создана
        send_news_notification.delay(instance.id)  # Запускаем задачу Celery
