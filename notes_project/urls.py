"""notes_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from notes import views
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, 'users')
router.register(r'logs', views.LogViewSet, 'logs')
router.register(r'entries', views.EntryViewSet, 'entries')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', obtain_auth_token),
    path('register/<str:token>/', views.RegisterView.as_view({'get': 'register'}), name='register'),

    path('api/v1/notes/', include('notes.urls')),

    path('api/loglist/', views.LogListViewSet.as_view()),

    path('api/', include(router.urls)),
    #path('logs/<int:pk>/', views.LogViewSet.as_view()), #api/v1/notes/1
]
