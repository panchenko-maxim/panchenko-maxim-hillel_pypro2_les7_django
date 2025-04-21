from celery import shared_task
from django.core.mail import send_mail
from tasks.models import Message

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