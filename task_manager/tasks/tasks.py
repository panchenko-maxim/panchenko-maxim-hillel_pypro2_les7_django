from celery import shared_task
from django.core.mail import send_mail
from tasks.models import Message
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_message(message_id):
    message = Message.objects.get(id=message_id)

    send_mail(
        'Test subj',
        message.content,
        'from@mail.com',
        ['to@mail.com'],
        fail_silently=False
    )

    message.sent = True
    message.save()


@shared_task
def log_sent_messages_count():
    message_count = Message.objects.filter(sent=True).count()
    logger.info(f'Total sent messages is: {message_count}')
