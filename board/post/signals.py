from django.db.models.signals import pre_save
from django.dispatch import receiver
from BD.models import Response
from .tasks import send_change_status

@receiver(pre_save, sender=Response)
def check_status(sender, instance, **kwargs):
    if instance.status != 'ожидает':
        send_change_status.delay(instance.id,)