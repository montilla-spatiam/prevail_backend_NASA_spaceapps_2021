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

class LogSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Log
    fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id','username', 'password')

        # So password is hidden on users get, ad required when creating a new user
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    # So that password is hashed
    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
