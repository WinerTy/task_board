from django.shortcuts import render
from .models import Post


class Main:
    def MainPage(request):
        latest_posts = Post.objects.order_by('-created_at')[:3]
        old_posts = Post.objects.order_by('created_at')[:3]
        slice_posts = Post.objects.all()[7:10]
        data = {
            'latest_posts': latest_posts,
            'old_posts': old_posts,
            'slice_posts': slice_posts
        }
        print(data)
        return render(request, 'default.html', data)
