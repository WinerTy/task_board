from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    CATEGORY_CHOICES = (
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('ДД', 'ДД'),
        ('Торговцы', 'Торговцы'),
        ('Гилдмастеры', 'Гилдмастеры'),
        ('Квестгиверы', 'Квестгиверы'),
        ('Кузнецы', 'Кузнецы'),
        ('Кожевники', 'Кожевники'),
        ('Зельевары', 'Зельевары'),
        ('Мастера заклинаний', 'Мастера заклинаний'),
    )
    title_image = models.ImageField(upload_to='images_title/', null=True, blank=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    text_image = models.ImageField(upload_to='images_text/', null=True, blank=True)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Response(models.Model):
    STATUS_CHOICES = (
        ('Ожидает', 'Ожидает'),
        ('Принят', 'Принят'),
        ('Отклонен', 'Отклонен'),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ожидает')

    def accept(self):
        self.status = 'Принят'
        self.save()


    def reject(self):
        self.status = 'Отклонен'
        self.save()

    def __str__(self):
        return f'{self.user.username} - {self.post.id} - {self.post.author}'

class Email(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return self.subject