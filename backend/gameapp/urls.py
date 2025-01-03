from django.urls import path
from .views import createGame, createPlayer, getAnswers, getQuestion, getRandomQuestion

urlpatterns = [
    path('createGame/', createGame, name='createGame'),
    path('createPlayer/', createPlayer, name='createPlayer'),
    path('getQuestion/', getQuestion, name='get_question'),
    path('getAnswers/', getAnswers, name='get_answers'),
    path('getRandomQuestion/', getRandomQuestion, name='get_random_question'),
]