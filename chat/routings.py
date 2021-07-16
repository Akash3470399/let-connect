from django.urls import path
from .import consumers
ws_urlpatterns = [
    path('chat/<str:chatroom>/',consumers.ChatConsumer),
]