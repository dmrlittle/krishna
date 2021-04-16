from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.chat, name='pilot'),
    path('<str:room_id>', views.chat, name='chat'),
]