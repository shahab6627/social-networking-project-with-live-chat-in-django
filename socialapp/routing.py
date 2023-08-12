from .consumers import ChatConsumer
from django.urls import path
websockets_urlpatterns = [
    path("ws/chat/<str:slug>", ChatConsumer.as_asgi())
]