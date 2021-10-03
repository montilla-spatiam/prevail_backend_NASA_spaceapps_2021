# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=no-member
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from . import models


class NoteConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'notes'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        title = text_data_json['title']
        content = text_data_json['content']
        id = text_data_json['id']

        note = models.Note.objects.get(pk=id)
        note.title = title
        note.content = content
        note.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'add_note',
                'title': title,
                'content': content,
                'id': id
            }
        )

    def add_note(self, event):
        title = event['title']
        content = event['content']
        id = event['id']
        self.send(text_data=json.dumps({
            'title': title,
            'content': content,
            'id': id
        }))


class LogConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'logs'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        id = text_data_json['id']
        description = text_data_json['description']
        users = text_data_json['users']
        entries = text_data_json['entries']
        date_modified = text_data_json['date_modified']
        date_published = text_data_json['date_published']
        tags = text_data_json['tags']

        note = models.Log.objects.get(pk=id)
        note.id = id
        note.description = description
        note.users = users
        note.entries = entries
        note.date_modified = date_modified
        note.date_published = date_published
        note.tags = tags
        note.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'add_log',
                'id': id,
                'description': description,
                'users': users,
                'entries': entries,
                'date_modified': date_modified,
                'date_published': date_published,
                'tags': tags,
            }
        )

    def add_log(self, event):
        id = event['id']
        description = event['description']
        users = event['users']
        entries = event['entries']
        date_modified = event['date_modified']
        date_published = event['date_published']
        tags = event['tags']
        self.send(text_data=json.dumps({
            'id': id,
            'description': description,
            'users': users,
            'entries': entries,
            'date_modified': date_modified,
            'date_published': date_published,
            'tags': tags,
        }))
