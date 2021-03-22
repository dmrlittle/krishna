from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.pilot, name='pilot'),
    path('chat/<str:room_id>', views.chat, name='chat'),
]