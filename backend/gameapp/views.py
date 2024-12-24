from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import json
from .models import Player, Game, User, Question, Answer


@api_view(['POST'])
def createGame(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        try:
            user = User.objects.get(username=data['username'])
            player = Player.objects.create(user=user)
            game = Game.objects.create(status='newGame')
            game.players.add(player)
            return JsonResponse({'gameId': game.id, 'playerID': player.id})
        except User.DoesNotExist:
            return JsonResponse({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def createPlayer(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        try:
            user = User.objects.get(username=data['username'])
            player = Player.objects.create(user=user)
            game = Game.objects.get(id=data['id'])
            game.players.add(player)
            return JsonResponse({'gameId': game.id, 'playerID': player.id})
        except User.DoesNotExist:
            return JsonResponse({"detail": "User or game not found"}, status=status.HTTP_404_NOT_FOUND)


api_view(['Get'])
def getQuestion(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        try:
            question = Question.objects.get(id=id)
            responseData = {
                "category": question.category,
                "text": question.text,
                "type": question.type
            }
            print(responseData)
            return JsonResponse(responseData)
        except User.DoesNotExist:
            return Response({"detail": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

api_view(['Get'])
def getAnswers(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        try:
            answer = Answer.objects.get(game=id)
            responseData = {
                "text": answer.text,
                "type": answer.type
            }
            print(responseData)
            return JsonResponse(responseData)
        except User.DoesNotExist:
            return Response({"detail": "Question not found"}, status=status.HTTP_404_NOT_FOUND)
