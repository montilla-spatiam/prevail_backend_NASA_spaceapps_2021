# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=no-member
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from . import models
from google.cloud import vision
import os
import json


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Note
        fields = '__all__'

class EntryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EntryData
        fields = '__all__'

class EntrySerializer(serializers.ModelSerializer):

    entry_data = EntryDataSerializer(required=False, allow_null=True)

    class Meta:
        model = models.Entry
        fields = ('id', 'user', 'date_modified', 'date_published',
                  'message', 'image', 'log', 'tags', 'raw_data', 'entry_data', 'data_visibility')

    def create(self, validated_data):
        message = validated_data.get('message')
        image = validated_data.get('image')
        tags = validated_data.get('tags')
        entry_data = None
        if validated_data.get('raw_data'):
            raw_data = json.loads(validated_data.get('raw_data'))
            entry_data = models.EntryData.objects.create(**raw_data)
        if(image):
            if tags :
                tags = detect_labels_uri(image) + ', ' + tags
            else: 
                tags = detect_labels_uri(image)

        user = validated_data.get('user')
        log = validated_data.get('log')

        entry = models.Entry.objects.create(message=message, image=image, tags=tags, user=user, log=log, raw_data="", entry_data=entry_data)

        log.entries.add(entry)

        return entry


class LogSerializer(serializers.ModelSerializer):
    entries = EntrySerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = models.Log
        fields = ('id', 'description', 'users', 'entries',
                  'date_modified', 'date_published', 'tags')

    def create(self, validated_data):
        description = validated_data.get('description')
        tags = validated_data.get('tags')
        users = validated_data.get('users')
        log = models.Log.objects.create(description=description, tags=tags)
        log.users.set(users)

        for user in log.users.all():
            user.logs.add(log)

        return log


class SimpleLogSerializer(serializers.ModelSerializer):

    users = serializers.SerializerMethodField()
    entries = serializers.SerializerMethodField()

    class Meta:
        model = models.Log
        fields = ('id', 'description', 'users', 'entries',
                  'date_modified', 'date_published', 'tags')

    def get_users(self, obj):
        users = obj.users.all().count()
        return users

    def get_entries(self, obj):
        entries = obj.entries.all().count()
        return entries


class UserSerializer(serializers.ModelSerializer):

    logs = SimpleLogSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = models.User
        fields = ('username', 'password', 'logs')

        # So password is hidden on users get, ad required when creating a new user
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    # So that password is hashed
    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

def detect_labels_uri(uri):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/montilla/Documents/Spatiam/Challenges/Nasa SpaceApps Hackathon 2021.nosync/DjangoRealTime/django-realtime-react/prevail_backend_NASA_spaceapps_2021/notes/cred.json'
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    label_arr = []

    for label in labels:
        label_arr.append(label.description)

    if response.error.message:
        return "image AI labeling not currently available"

    return(str(label_arr).replace('[', '').replace(']', '').replace("'",''))
