from django.urls import path
from .views import (createGame, createPlayer, getAnswers, getQuestion, getRandomQuestion, getRandomChance, getChance, \
    getRandomProfession, connectToGame, getInfoAboutGame, changePlayer, addActionAnswer, addActionChance, getAnswerOutcome, \
                    changeBalance, checkScip, getActiveGames)

urlpatterns = [
    path('createGame/', createGame, name='createGame'),
    path('getInfoAboutGame/', getInfoAboutGame, name='getInfoAboutGame'),
    path('connectToGame/', connectToGame, name='connectToGame'),
    path('createPlayer/', createPlayer, name='createPlayer'),
    path('getQuestion/', getQuestion, name='get_question'),
    path('getAnswers/', getAnswers, name='get_answers'),
    path('getRandomQuestion/', getRandomQuestion, name='get_random_question'),
    path('getRandomChance/', getRandomChance, name='get_random_chance'),
    path('getChance/', getChance, name='get_chance'),
    path('getRandomProfession/', getRandomProfession, name='get_random_profession'),
    path('changePlayer/', changePlayer, name='change_player'),
    path('addActionAnswer/', addActionAnswer, name='add_action_answer'),
    path('addActionChance/', addActionChance, name='addActionChance'),
    path('changeBalance/', changeBalance, name='change_balance'),
    path('checkScip/', checkScip, name='check_scip'),
    path('getAnswerOutcome/', getAnswerOutcome, name='get_answer_outcome'),
    path('getActiveGames/', getActiveGames, name='getActiveGames'),
]