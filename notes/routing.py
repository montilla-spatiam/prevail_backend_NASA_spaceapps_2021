# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=no-member
from django.urls import re_path 

from . import consumers

websocket_urlpatterns = [
  re_path('ws/notes', consumers.NoteConsumer.as_asgi()),
  re_path('ws/logs', consumers.LogConsumer.as_asgi())
]
