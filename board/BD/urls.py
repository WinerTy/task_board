
from django.urls import path


from .views import Main

urlpatterns = [
    path('', Main.MainPage, name="main"),
]