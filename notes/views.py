# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=no-member
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from .permissions import IsPOST
from django.http import HttpResponse
from .models import User
from .serializers import UserSerializer
from . import models
from . import serializers

class RegisterView(viewsets.ModelViewSet):
    def register(self, request):
        token = request.GET.get("token")
        response = "Invalid"
        if(token=="SPACEAPPS"):
            response = "Valid"
        return HttpResponse(response)

class NoteList(generics.ListCreateAPIView):
    queryset = models.Note.objects.all().order_by('-created_at', '-updated_at')
    serializer_class = serializers.NoteSerializer

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Note.objects.all()
    serializer_class = serializers.NoteSerializer

class LogListViewSet(generics.ListCreateAPIView):
    queryset = models.Log.objects.all().order_by('-date_modified' , '-date_published')
    serializer_class = serializers.LogSerializer
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [IsAuthenticated]

class LogViewSet(viewsets.ModelViewSet):
    queryset = models.Log.objects.all()
    serializer_class = serializers.LogSerializer
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_path='add_user', url_name='get_uuid')
    def add_user(self, request, pk=None):
        log = models.Log.objects.get(id=pk)
        user = request.user

        log.users.add(user)
        user.logs.add(log)

        serializer = serializers.SimpleLogSerializer(log)
        return HttpResponse(JSONRenderer().render(serializer.data), content_type='application/json')

class EntryViewSet(viewsets.ModelViewSet):
    queryset = models.Entry.objects.all()
    serializer_class = serializers.EntrySerializer
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [IsAuthenticated | IsPOST]

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated], url_path='me', url_name='my_user')
    def get_me(self, request, pk=None):
        serializer = UserSerializer(Token.objects.get(
            key=request.META['HTTP_AUTHORIZATION'].replace('Token ', '')).user)
        return HttpResponse(JSONRenderer().render(serializer.data), content_type='application/json')
