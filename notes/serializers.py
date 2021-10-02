# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=no-member
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from . import models

class NoteSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Note
    fields = '__all__'

class EntrySerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Entry
    fields = '__all__'

class LogSerializer(serializers.ModelSerializer):
    entries = EntrySerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = models.Log
        fields = ('id', 'description', 'users', 'entries',
                  'date_modified', 'date_published', 'tags')

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
        
