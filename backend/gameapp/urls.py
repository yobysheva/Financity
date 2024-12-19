from django.urls import path
from .views import createGame

urlpatterns = [
    path('createGame/', createGame, name='createGame'),
]