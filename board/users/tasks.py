from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from BD.models import Email

@shared_task
def send_email_to_subscribers(email_id):
    try:
        email = Email.objects.get(id=email_id)
        subscribers = User.objects.filter(groups__name='Subscriber')
        emails = [user.email for user in subscribers]
        subject = {
            'text': email.message,
        }
        html_content = render_to_string('email/custom_email.html', {'subject': subject})
        msg = EmailMultiAlternatives(
            email.subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            emails
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Email.DoesNotExist:
        pass