from django.urls import re_path
from chat.services import consumers


websocket_urlpatterns = [
    re_path(r'ws/chat/room/(?P<id>\d+)/$',
            consumers.ChatConsumer.as_asgi()),
]
