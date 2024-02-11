from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from BD.models import Post, Response

@shared_task
def send_response(title, text, post_id, user):
    try:
        post = Post.objects.get(id=post_id)
        user = User.objects.get(id=user)
        url = reverse('post_info', args=[post_id])
        subject = {
            'title': title,
            'text': text,
            'user': user.username,
            'url': 'http://127.0.0.1:8000'+url,
            'category': f'{post.category}'
        }
        print(url)
        html_content = render_to_string('email/send_response.html', {'subject': subject})
        msg = EmailMultiAlternatives(
            f'На ваше объявление откликнулся: {subject["user"]}',
            '',
            settings.DEFAULT_FROM_EMAIL,
            [post.author.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except:
        pass

@shared_task
def notify(user, post_id):
    try:
        user = User.objects.get(id=user)
        url = reverse('post_info', args=[post_id])
        print(user.email)
        subject = {
            'user': user.username,
            'url': 'http://127.0.0.1:8000' + url
        }
        html_content = render_to_string('email/notify.html', {'subject': subject})
        msg = EmailMultiAlternatives(
            f'Вы откликнулись на объявление',
            '',
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except:
        pass


@shared_task
def send_change_status(instance_id):
    try:
        response = Response.objects.get(id=instance_id)
        url = reverse('post_info', args=[response.post.id])
        subject = {
            'status': response.status,
            'user': response.user.username,
            'url': 'http://127.0.0.1:8000' + url
        }
        html_content = render_to_string('email/change_status.html', {'subject': subject})
        msg = EmailMultiAlternatives(
            f'Статус вашего отклика изменен',
            '',
            settings.DEFAULT_FROM_EMAIL,
            [response.user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Response.DoesNotExist:
        pass
