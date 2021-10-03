# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=no-member
from django.urls import path
from . import views 

urlpatterns = [
  path('yes/', views.NoteList.as_view()),
  path('yes/<int:pk>/', views.NoteDetail.as_view()), #api/v1/notes/1
  path('logs/<int:pk>/', views.LogDetail.as_view()),
]
