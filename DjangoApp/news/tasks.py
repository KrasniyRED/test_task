from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailTask, News


@shared_task
def send_news_notification(news_id: int) -> None:
    news = News.objects.get(id=news_id)
    email_task = EmailTask.objects.first()  # Берем первую настройку задачи
    if email_task:
        recipients = [
            email.strip() for email in email_task.recipients.split(',')
        ]
        subject = email_task.subject
        message = f'{email_task.message}\n\nНовая новость: {news.title}\n{news.content}'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            fail_silently=False,
        )
