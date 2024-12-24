from django.urls import path
from .views import createGame, createPlayer

urlpatterns = [
    path('createGame/', createGame, name='createGame'),
    path('createPlayer/', createPlayer, name='createPlayer'),
]