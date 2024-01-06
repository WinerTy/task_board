from django.dispatch import receiver
from django.db.models.signals import post_save
from BD.models import Email
from .tasks import send_email_to_subscribers

@receiver(post_save, sender=Email)
def send_email_signal(sender, instance, created, **kwargs):
    try:
        print('Дошел до сигнала')
        if created:
            print('Объект создан')
            print(instance.id)
            send_email_to_subscribers.delay(instance.id)
    except Exception as e:
        print(e)