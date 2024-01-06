from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.views import View
from django.views.generic import ListView, DeleteView, UpdateView

from .forms import CreatePostForm, ResponseForm, AcceptResponseForm, RejectResponseForm
from BD.models import Post, Response
from .tasks import send_response, notify


@login_required
class CreatePublish:
    def create(request):
        if request.method == 'POST':
            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(request.user)
                form.save_m2m()
            return redirect('create')

        form = CreatePostForm()

        data = {
            'data': form
        }

        return render(request, 'post/create.html', data)

class AllPosts(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'post/all_posts.html'
    context_object_name = 'posts'
    paginate_by = 9
    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.get_queryset()
        paginator = Paginator(posts, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            posts = paginator.page(page)

        except PageNotAnInteger:

            posts = paginator.page(1)

        except EmptyPage:

            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts

        return context

class AllCategory:
    def show(request):
        categories = Post.CATEGORY_CHOICES
        category_list = [category[0] for category in categories]
        category_images = {
            'Танки': '/static/category_img/templar.jpeg',
            'Хилы': '/static/category_img/druid.jpeg',
            'ДД': '/static/category_img/warior.jpeg',
            'Торговцы': '/static/category_img/thief.jpeg',
            'Гилдмастеры': '/static/category_img/ranger.jpeg',
            'Квестгиверы': '/static/category_img/asasin.jpeg',
            'Кузнецы': '/static/category_img/templar.jpeg',
            'Кожевники': '/static/category_img/bard.jpeg',
            'Зельевары': '/static/category_img/mage.jpeg',
            'Мастера заклинаний': '/static/category_img/pyro.jpeg',
        }
        return render(request, 'post/category.html', {'category': category_list, 'category_images': category_images})


class PostInfo(View):
    def get(request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        try:
            if request.user.is_authenticated:
                response_list = Response.objects.filter(post_id=post_id, user=request.user)
            else:
                response_list = None
        except Response.DoesNotExist:
            response_list = None
        form = ResponseForm()
        return render(request, 'post/post_info.html', {'post': post, 'form': form, 'response_list': response_list})


class ResponseInfo():
    def response(request, post_id):
        if request.method == 'GET':
            try:
                post = get_object_or_404(Post, pk=post_id)
                form = ResponseForm(request.GET)
                if form.is_valid():
                    title = form.cleaned_data['title']
                    text = form.cleaned_data['text']
                    user = request.user.id
                    send_response.delay(title, text, post_id, user)
                    notify.delay(user, post_id)
                    response = Response.objects.create(post=post, user=request.user, status='Ожидает')
                    return redirect('post_info', post_id)

            except Exception as e:
                print(f'Возникла ошибка при отправке отклика: {e}')
        else:
            print('Неверный запрос')


class Candidates():
    def show(request):
        user = request.user
        post_ids = Post.objects.filter(author=user).values_list('id', flat=True)
        posts = Post.objects.filter(id__in=post_ids)
        responses = Response.objects.filter(post__in=post_ids)
        data = {}
        for post in posts:
            data[post.id] = {'title': post.title, 'responses': responses.filter(post=post)}


        return render(request, 'post/post_responses.html', {'data': data})

    def Find(request):
        try:
            if request.method == 'GET':
                search_id = request.GET.get('Find_id', '')
                search_title = request.GET.get('Find_title', '')
                data = {}
                if search_id or search_title:
                    if search_id:
                        posts = Post.objects.filter(id=search_id, author=request.user)
                        responses = Response.objects.filter(post__in=posts).exclude(user=request.user)
                        for post in posts:
                            data[post.id] = {'title': post.title, 'responses': responses.filter(post=post)}
                    if search_title:
                        posts = Post.objects.filter(title__icontains=search_title)
                        for post in posts:
                            responses = Response.objects.filter(post=post).exclude(user=request.user)
                            data[post.id] = {'title': post.title, 'responses': responses}
                return render(request, 'post/post_responses.html', {'data': data})
            else:
                return render(request, 'post/post_responses.html', {'posts': None})
        except Exception as e:
            data = { 'error' : e }
            return data


class UpdatePost(UpdateView):
    model = Post
    fields = ['title', 'text', 'category', 'title_image', 'text_image']
    template_name = 'post/update.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect('all_posts')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return '/post/all_posts/'

class DeletePost(DeleteView):
    model = Post
    template_name = 'post/delete.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect('all_posts')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return '/post/all_posts/'

def accept_response(request):
    if request.method == 'POST':
        form = AcceptResponseForm(request.POST)
        if form.is_valid():
            response_id = form.cleaned_data['response_id']
            response = get_object_or_404(Response, id=response_id)
            response.accept()
    return redirect('candidates')

def reject_response(request):
    if request.method == 'POST':
        form = RejectResponseForm(request.POST)
        if form.is_valid():
            response_id = form.cleaned_data['response_id']
            response = get_object_or_404(Response, id=response_id)
            response.reject()
    return redirect('candidates')