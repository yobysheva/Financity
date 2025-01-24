from django.http import JsonResponse
from django.template.defaultfilters import random
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


api_view(['GET'])
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
        except Question.DoesNotExist:
            return Response({"detail": "Question not found"}, status=status.HTTP_404_NOT_FOUND)


api_view(['Get'])
def getAnswers(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        if not id:
            return Response({"detail": "Parameter 'id' is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            answers = Answer.objects.filter(question=id)
            responseData = []
            for answer in answers:
                responseData.append({
                    "id": answer.id,
                    "text": answer.answer_text
                })
            print(responseData)
            return JsonResponse(responseData, safe=False)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


api_view(['Get'])
def getRandomQuestion(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id', None)
        try:
            question = Question.objects.filter(category=category_id).order_by('?').first()
            responseData = {
                "id" : question.id,
                "category": question.category,
                # "text": question.text,
                "type": question.type
            }
            print(responseData)
            return JsonResponse(responseData)
        except Question.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def connectToGame(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        try:
            user = User.objects.get(username=data['username'])
            player = Player.objects.create(user=user)
            game = Game.objects.get(id=data["game_id"])
            game.players.add(player)
            print(game.players.all())
            return JsonResponse({'gameId': game.id, 'playerID': player.id})
        except User.DoesNotExist:
            return JsonResponse({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getInfoAboutGame(request):
     if request.method == 'GET':
         game_id = request.GET.get('gameId', None)
         try:
             game = Game.objects.get(id=game_id)
             players = list(game.players.all())
             print(list(players))
             return JsonResponse({'players': [player.id for player in players]})
         except Game.DoesNotExist:
             return JsonResponse({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
