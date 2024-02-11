from .views import CreatePublish, AllPosts, AllCategory, PostInfo, UpdatePost, DeletePost, ResponseInfo, Candidates
from django.conf import settings

from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('create/', CreatePublish.create, name='create'),
    path('all_posts/', AllPosts.as_view(), name='all_posts'),
    path('category/', AllCategory.show, name='category'),
    path('detail/<int:post_id>/', PostInfo.get, name='post_info'),
    path('detail/<int:pk>/update', UpdatePost.as_view(), name='update_post'),
    path('detail/<int:pk>/delete', DeletePost.as_view(), name='delete_post'),
    path('detail/<int:post_id>/response', ResponseInfo.response, name='response'),
    path('candidates/', Candidates.show, name='candidates'),
    path('candidates/sort/', Candidates.Find, name='candidates_sort'),
    path('accept_response/', views.accept_response, name='accept_response'),
    path('reject_response/', views.reject_response, name='reject_response'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)